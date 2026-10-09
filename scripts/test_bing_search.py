#!/usr/bin/env python3
"""Unit tests for scripts/bing_search.py, offline.

    python3 scripts/test_bing_search.py

The subject is the shape of the digest's Bing table and its watchdog, fed
with rows in the exact form Bing's JSON API returns them ("/Date(ms)/"),
so none of this needs the key or the network. The watchdog is what these
guard most: it exists so a Bing demotion shows in DATA.md within days, and a
watchdog that fires on a missing crawl row, or stays quiet on a halving, is
worse than none.
"""
import datetime
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bing_search import (daily_rows, lines, parse_date, query_rows,  # noqa: E402
                         split_window, watchdog)


def ms(day):
    """2026-10-01 -> Bing's '/Date(ms)/' string for UTC midnight."""
    d = datetime.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    return "/Date(%d)/" % int(d.timestamp() * 1000)


def traffic(days, clicks, impressions):
    return [{"Date": ms(d), "Clicks": c, "Impressions": i} for d, c, i in zip(days, clicks, impressions)]


def crawl(days, crawled, in_index):
    return [{"Date": ms(d), "CrawledPages": c, "InIndex": i, "Code2xx": c, "AllOtherCodes": 0}
            for d, c, i in zip(days, crawled, in_index)]


DAYS = ["2026-09-%02d" % d for d in range(24, 31)] + ["2026-10-%02d" % d for d in range(1, 8)]


class TestParsing(unittest.TestCase):
    def test_bing_date_string_becomes_iso_day(self):
        self.assertEqual(parse_date("/Date(1696204800000)/"), "2023-10-02")

    def test_garbage_date_is_none(self):
        self.assertIsNone(parse_date("soon"))

    def test_traffic_and_crawl_join_on_the_day(self):
        rows = daily_rows(traffic(DAYS[:2], [1, 2], [10, 20]), crawl(DAYS[:2], [100, 110], [3000, 3010]))
        self.assertEqual(rows[0], {"date": DAYS[0], "clicks": 1, "impressions": 10,
                                   "crawled": 100, "in_index": 3000})
        self.assertEqual(rows[1]["in_index"], 3010)

    def test_a_day_missing_from_crawl_keeps_none_not_zero(self):
        rows = daily_rows(traffic(DAYS[:2], [1, 2], [10, 20]), crawl(DAYS[:1], [100], [3000]))
        self.assertIsNone(rows[1]["crawled"])
        self.assertIsNone(rows[1]["in_index"])

    def test_queries_sort_by_clicks_then_impressions(self):
        q = query_rows([{"Query": "b", "Clicks": 0, "Impressions": 50, "AvgImpressionPosition": 9},
                        {"Query": "a", "Clicks": 2, "Impressions": 5, "AvgImpressionPosition": 3},
                        {"Query": " ", "Clicks": 9, "Impressions": 9}])
        self.assertEqual([r["query"] for r in q], ["a", "b"])


class TestWindow(unittest.TestCase):
    def test_window_is_rows_not_calendar_days(self):
        rows = daily_rows(traffic(DAYS, [1] * 14, [10] * 14))
        this_week, last_week = split_window(rows, 7)
        self.assertEqual([r["date"] for r in this_week], DAYS[7:])
        self.assertEqual([r["date"] for r in last_week], DAYS[:7])

    def test_short_history_has_an_empty_previous_week(self):
        rows = daily_rows(traffic(DAYS[:5], [1] * 5, [10] * 5))
        this_week, last_week = split_window(rows, 7)
        self.assertEqual(len(this_week), 5)
        self.assertEqual(last_week, [])


class TestWatchdog(unittest.TestCase):
    def weeks(self, imp_then, imp_now, idx_then, idx_now):
        rows = daily_rows(traffic(DAYS, [1] * 14, [imp_then] * 7 + [imp_now] * 7),
                          crawl(DAYS, [100] * 14, [idx_then] * 7 + [idx_now] * 7))
        return split_window(rows, 7)

    def test_quiet_when_nothing_moved(self):
        self.assertIsNone(watchdog(*self.weeks(30, 28, 3800, 3790)))

    def test_fires_when_impressions_halve(self):
        line = watchdog(*self.weeks(30, 12, 3800, 3800))
        self.assertIn("BING WATCHDOG", line)
        self.assertIn("impressions fell from 210 to 84", line)

    def test_exactly_half_is_not_under_half(self):
        self.assertIsNone(watchdog(*self.weeks(30, 15, 3800, 3800)))

    def test_fires_when_index_drops_a_fifth(self):
        line = watchdog(*self.weeks(30, 30, 3800, 3000))
        self.assertIn("pages in Bing's index fell from 3800 to 3000", line)

    def test_a_fifth_exactly_does_not_fire(self):
        self.assertIsNone(watchdog(*self.weeks(30, 30, 3800, 3040)))

    def test_both_alarms_share_one_line(self):
        line = watchdog(*self.weeks(30, 5, 3800, 100))
        self.assertEqual(line.count("BING WATCHDOG"), 1)
        self.assertIn("impressions fell", line)
        self.assertIn("index fell", line)

    def test_no_previous_week_means_no_alarm(self):
        rows = daily_rows(traffic(DAYS[7:], [1] * 7, [0] * 7), crawl(DAYS[7:], [1] * 7, [0] * 7))
        self.assertIsNone(watchdog(*split_window(rows, 7)))

    def test_missing_crawl_rows_never_count_as_zero(self):
        # Traffic for both weeks, crawl stats only for the first: the index
        # column has no "now", so the index alarm must stay silent.
        rows = daily_rows(traffic(DAYS, [1] * 14, [30] * 14), crawl(DAYS[:7], [100] * 7, [3800] * 7))
        self.assertIsNone(watchdog(*split_window(rows, 7)))


class TestLines(unittest.TestCase):
    def test_table_has_the_four_columns_and_a_totals_row(self):
        rows = daily_rows(traffic(DAYS, [1] * 14, [10] * 14), crawl(DAYS, [100] * 14, [3800] * 14))
        out = lines(*split_window(rows, 7), [])
        self.assertEqual(out[0], "| Day | Impressions | Clicks | CTR | Pages crawled | Pages in index |")
        self.assertEqual(len([l for l in out if l.startswith("| 10-") or l.startswith("| 09-")]), 7)
        self.assertIn("| **7 days** | **70** | **7** | **10.0%** | **700** | **3800** |", out)
        self.assertTrue(any("No Bing demotion in sight" in l for l in out))

    def test_missing_crawl_prints_a_dash(self):
        rows = daily_rows(traffic(DAYS[7:], [1] * 7, [10] * 7))
        out = lines(*split_window(rows, 7), [])
        self.assertIn("| 10-07 | 10 | 1 | 10.0% | - | - |", out)

    def test_no_rows_is_one_line_no_table(self):
        out = lines([], [], [])
        self.assertEqual(len(out), 1)
        self.assertNotIn("|", out[0])

    def test_never_a_bot_column(self):
        rows = daily_rows(traffic(DAYS, [1] * 14, [10] * 14))
        for l in lines(*split_window(rows, 7), []):
            self.assertNotIn("bot", l.lower())


if __name__ == "__main__":
    unittest.main()
