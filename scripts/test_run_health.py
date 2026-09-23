#!/usr/bin/env python3
"""Unit tests for the denial record in scripts/run_health.py.

    python3 scripts/test_run_health.py
    python3 -m unittest scripts.test_run_health -v

The subject is command_shape(), which decides what a refused command is called
in data/run-health.json. That file is committed to a public repository and the
runs that fill it handle reader submissions, so half of these tests are about
what must NOT come out: an argument, a path, a URL, an environment value.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_health import command_shape, _denial_label  # noqa: E402


class TestShape(unittest.TestCase):
    def test_plain_command_is_its_own_name(self):
        self.assertEqual(command_shape("python3 scripts/qa.py"), "python3")

    def test_chained_command_names_every_segment(self):
        # The whole point: `python3` alone was the old answer, and it is the one
        # word on this line that the allowlist already permits.
        self.assertEqual(command_shape("python3 x.py && git commit -m hi"),
                         "python3 && git")

    def test_pipe_is_a_chain_too(self):
        self.assertEqual(command_shape("python3 x.py | head -5"), "python3 | head")

    def test_subshell_is_named(self):
        # The shape that silently stopped every night run for a day, 2026-08.
        self.assertEqual(command_shape("(cd site && npm ci)"),
                         "subshell cd && npm")

    def test_semicolon_and_or(self):
        self.assertEqual(command_shape("ls; wc -l"), "ls ; wc")
        self.assertEqual(command_shape("test -f x || echo no"), "test || echo")

    def test_shell_keyword_keeps_its_name(self):
        # `for` and `if` show up in the record as refused binaries. They are not
        # binaries, and no Bash(x:*) entry has ever matched one.
        self.assertTrue(command_shape("for f in a b; do echo $f; done")
                        .startswith("for"))

    def test_long_chain_is_truncated_not_dropped(self):
        shape = command_shape("a && b && c && d && e && f")
        self.assertTrue(shape.endswith("..."), shape)
        self.assertIn("a && b", shape)

    def test_empty_is_none(self):
        self.assertIsNone(command_shape(""))
        self.assertIsNone(command_shape("   "))
        self.assertIsNone(command_shape(None))

    def test_trailing_operator_leaves_no_dangling_join(self):
        self.assertEqual(command_shape("python3 x.py &&"), "python3")
        self.assertEqual(command_shape("| grep x"), "grep")


class TestNothingLeaks(unittest.TestCase):
    """Whatever else changes here, none of these may ever appear in the output."""

    def test_no_path_survives(self):
        shape = command_shape("python3 scripts/photo_apply.py data/cities/utrecht.json")
        self.assertEqual(shape, "python3")

    def test_no_url_survives(self):
        shape = command_shape("curl -m 20 https://example.org/secret?token=abc123")
        self.assertEqual(shape, "curl")

    def test_no_url_survives_a_chain(self):
        shape = command_shape("curl -m 20 https://example.org/a | jq .name")
        self.assertEqual(shape, "curl | jq")
        self.assertNotIn("example.org", shape)

    def test_env_assignment_is_not_reported_as_a_command(self):
        # FOO=bar cmd: the assignment carries the value, so it must not be the
        # word that gets recorded.
        shape = command_shape("SUPABASE_SERVICE_KEY=sk-live-1234 python3 x.py")
        self.assertEqual(shape, "python3")
        self.assertNotIn("1234", shape)

    def test_unparseable_head_becomes_a_question_mark(self):
        shape = command_shape('"/opt/some path/bin" --flag')
        self.assertEqual(shape, "?")
        self.assertNotIn("some path", shape)

    def test_quoted_argument_containing_an_operator_does_not_leak(self):
        # The split is naive about quoting, which is allowed to produce a
        # slightly wrong SHAPE and is never allowed to produce an argument.
        shape = command_shape('grep "a && b" data/cities/paris.json')
        for leak in ("paris", "data/", ".json"):
            self.assertNotIn(leak, shape)


class TestLabel(unittest.TestCase):
    def test_bash_denial_gets_a_shape(self):
        d = {"tool_name": "Bash",
             "tool_input": {"command": "cd site && npx astro build"}}
        self.assertEqual(_denial_label(d), "Bash(cd && npx)")

    def test_non_bash_tool_is_named_plainly(self):
        self.assertEqual(_denial_label({"tool_name": "WebFetch",
                                        "tool_input": {"url": "https://x.test"}}),
                         "WebFetch")

    def test_missing_input_does_not_raise(self):
        self.assertEqual(_denial_label({"tool_name": "Bash"}), "Bash")
        self.assertEqual(_denial_label({}), "?")


if __name__ == "__main__":
    unittest.main(verbosity=2)
