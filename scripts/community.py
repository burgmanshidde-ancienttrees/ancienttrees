#!/usr/bin/env python3
"""Reddit for the night run: what people said under Hidde's posts, and threads
where one of our trees is the answer.

Hidde, 2026-10-24, after the r/Lisbon post took the site from 3 to 15 people a
day: "you can refocus the nightrun on outreach and local community posts if you
find an effective way to do that". Hidde posts and replies himself from his own
account (OUTREACH_STRATEGY.md, Communities); what costs him the time is the
reading, the tips and the replies, so that is what this does. Reddit blocks our
fetches; the Arctic Shift archive (arctic-shift.photon-reddit.com, free, read
only, minutes behind Reddit) does not.

    python3 scripts/community.py --add https://www.reddit.com/r/lisbon/comments/1xci4vn/ --city lisbon
    python3 scripts/community.py --harvest          # new comments under his posts
    python3 scripts/community.py --watch            # new threads about an old tree
    python3 scripts/community.py --open             # what waits for a reply or a lead
    python3 scripts/community.py --reply <id> "text" # a drafted reply, for him to post
    python3 scripts/community.py --done <id> "lead lis_031 / not a tip / he answered"
    python3 scripts/community.py --kit <city>       # the facts for his next post
    python3 scripts/community.py --preview          # drafts/batch-community-preview.md
    python3 scripts/community.py --status

Everything lives in data/outreach-community.json and the preview file, both
private (gitignored, synced by private_store.py), because they hold strangers'
words. No Reddit username is ever stored, ours included: the author field is
read only to tell his own comments from theirs.

The archive can miss a thread's comments (r/sicily 1xda1j0 had eight tips on
Reddit and none in the archive on 2026-10-24), so an empty harvest is not proof
that nobody answered.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "data", "outreach-community.json")
PREVIEW = os.path.join(ROOT, "drafts", "batch-community-preview.md")
API = "https://arctic-shift.photon-reddit.com/api"
UA = {"User-Agent": "curl/8.7.1"}  # the archive refuses Python's default agent
PAUSE = 3  # seconds between calls; big subs time out when pushed
HARVEST_DAYS = 45  # a thread is read until it is this old

# Where people post the tree in front of them. City subs come from --add and
# the "watch_subs" list in the store, so a new city needs no code.
# r/arborists left on day one: its old trees are tree-care worries, not visits.
TREE_SUBS = ["marijuanaenthusiasts", "treeidentification", "botany", "NatureIsFuckingLit"]
OLD = re.compile(r"\b(ancient|oldest|old|centuries|century|\d{3,4}[- ]?years?|huge|giant|massive|"
                 r"biggest|largest|veteran|monumental|champion)\b", re.I)
TREE = re.compile(r"\b(trees?|oak|yew|chestnut|olive|fig|cedar|sequoia|redwood|beech|baobab|plane|"
                  r"lime|linden|ginkgo|banyan|cypress|sycamore|elm|ash|pine|willow)\b", re.I)
# In a city sub a tree must be the subject, not a word in passing.
CITY_Q = re.compile(r"\b(trees?|oldest tree|arboretum|botanical gardens?|autumn colou?rs?|fall foliage|"
                    r"árvores?|árboles?|alberi|bäume|baum|arbres?|bomen)\b", re.I)


def load():
    try:
        d = json.load(open(STORE, encoding="utf-8"))
    except (OSError, ValueError):
        d = {}
    d.setdefault("posts", [])
    d.setdefault("watch_subs", [])
    d.setdefault("seen", {})       # post id -> comment ids already queued
    d.setdefault("seen_posts", [])  # watched threads already queued or skipped
    d.setdefault("after", {})       # sub -> last utc watched
    d.setdefault("items", [])
    return d


def save(d):
    with open(STORE, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)


def get(path, **q):
    url = "%s/%s?%s" % (API, path, urllib.parse.urlencode(q))
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                body = json.load(r)
        except Exception as e:  # one bad call costs one sub, never the run
            print("  archive: %s (%s)" % (e, path), file=sys.stderr)
            return []
        if body.get("error") and attempt == 1:
            time.sleep(PAUSE * 3)
            continue
        if body.get("error"):
            print("  archive: %s (%s)" % (body["error"], path), file=sys.stderr)
        return body.get("data") or []
    return []


def day(utc):
    return time.strftime("%Y-%m-%d", time.gmtime(utc))


def cities():
    """slug -> (city name, {tree name lowercase: (id, photo status)})."""
    out = {}
    for f in glob.glob(os.path.join(ROOT, "data", "cities", "*.json")):
        try:
            c = json.load(open(f, encoding="utf-8"))
        except ValueError:
            continue
        trees = {}
        for t in c.get("trees", []):
            if t.get("name"):
                trees[t["name"].lower()] = (t["id"], (t.get("photo") or {}).get("status"))
        out[os.path.basename(f)[:-5]] = (c.get("city") or "", trees)
    return out


def our_page(text, city=None):
    """The page of ours a thread is about: a tree named in it, else the city."""
    low = text.lower()
    cs = cities()
    pool = [city] if city in cs else list(cs)
    for slug in pool:
        name, trees = cs[slug]
        for tname, (tid, _) in trees.items():
            core = re.sub(r"^the |\s*\(.*\)$", "", tname)
            if len(core) > 12 and core in low:
                return "https://ancienttrees.app/%s (%s)" % (slug, tid)
    for slug in pool:
        name = cs[slug][0]
        if name and re.search(r"\b%s\b" % re.escape(name.lower()), low):
            return "https://ancienttrees.app/%s" % slug
    return ""


def queue(d, item):
    if any(i["id"] == item["id"] for i in d["items"]):
        return False
    item.setdefault("status", "open")
    item["found"] = datetime.date.today().isoformat()
    d["items"].append(item)
    return True


def add(d, url, city):
    m = re.search(r"/r/([^/]+)/comments/([a-z0-9]+)", url)
    if not m:
        sys.exit("not a Reddit post url: %s" % url)
    sub, pid = m.group(1), m.group(2)
    if any(p["id"] == pid for p in d["posts"]):
        print("already known: %s" % pid)
        return
    p = (get("posts/ids", ids=pid, fields="title,created_utc") or [{}])[0]
    d["posts"].append({"id": pid, "sub": sub, "city": city, "title": p.get("title", ""),
                       "posted": day(p["created_utc"]) if p.get("created_utc") else ""})
    if sub.lower() not in [s.lower() for s in d["watch_subs"]]:
        d["watch_subs"].append(sub)
    print("added r/%s %s: %s" % (sub, pid, p.get("title", "?")))


def harvest(d):
    """Every comment under his posts that is not his own, once."""
    cut = time.time() - HARVEST_DAYS * 86400
    new = 0
    for p in d["posts"]:
        if p.get("posted") and time.mktime(time.strptime(p["posted"], "%Y-%m-%d")) < cut:
            continue
        op = (get("posts/ids", ids=p["id"], fields="author") or [{}])[0].get("author")
        time.sleep(PAUSE)
        cs = get("comments/search", link_id=p["id"], limit=100,
                 fields="id,body,parent_id,created_utc,author")
        time.sleep(PAUSE)
        mine = [c for c in cs if op and c.get("author") == op]
        answered = {c.get("parent_id", "")[3:] for c in mine}
        seen = set(d["seen"].get(p["id"], []))
        for c in cs:
            if c["id"] in seen or (op and c.get("author") == op):
                continue
            body = (c.get("body") or "").strip()
            if not body or body in ("[deleted]", "[removed]"):
                continue
            # The comment it answers, so a reply can be judged in context.
            parent = next((x for x in cs if "t1_" + x["id"] == c.get("parent_id")), None)
            item = {"id": c["id"], "kind": "comment", "sub": p["sub"], "city": p.get("city"),
                    "url": "https://www.reddit.com/r/%s/comments/%s/_/%s/" % (p["sub"], p["id"], c["id"]),
                    "date": day(c["created_utc"]), "text": body[:1500],
                    "in_reply_to": (parent.get("body") or "")[:300] if parent else "the post",
                    "page": our_page(body, p.get("city"))}
            if c["id"] in answered:
                item["status"] = "done"
                item["note"] = "he answered it on Reddit"
            if queue(d, item):
                new += 1
            seen.add(c["id"])
        d["seen"][p["id"]] = sorted(seen)
        print("r/%s %s: %d comments, %d by him" % (p["sub"], p["id"], len(cs), len(mine)))
    print("%d new comments queued" % new)


def watch(d):
    """New threads about an old tree (tree subs) or about trees (city subs)."""
    subs = [(s, OLD, TREE) for s in TREE_SUBS] + [(s, CITY_Q, None) for s in d["watch_subs"]]
    since = int(time.time() - 7 * 86400)
    mine = {p["id"] for p in d["posts"]}
    new = 0
    for sub, a, b in subs:
        after = max(d["after"].get(sub, 0), since)
        ps = get("posts/search", subreddit=sub, after=after, limit=100, sort="desc",
                 fields="id,title,selftext,created_utc,num_comments,score")
        time.sleep(PAUSE)
        if ps:
            d["after"][sub] = max(p["created_utc"] for p in ps)
        for p in ps:
            if p["id"] in d["seen_posts"] or p["id"] in mine:
                continue
            head = p.get("title", "")
            text = head + "\n" + (p.get("selftext") or "")
            hit = a.search(head) and (b is None or b.search(head)) if b else a.search(text)
            if not hit:
                continue
            d["seen_posts"].append(p["id"])
            city = next((x.get("city") for x in d["posts"] if x["sub"].lower() == sub.lower()), None)
            if queue(d, {"id": p["id"], "kind": "thread", "sub": sub, "city": city,
                         "url": "https://www.reddit.com/r/%s/comments/%s/" % (sub, p["id"]),
                         "date": day(p["created_utc"]), "title": head[:300],
                         "text": (p.get("selftext") or "")[:1200], "comments": p.get("num_comments"),
                         "page": our_page(text, city)}):
                new += 1
        print("r/%s: %d new posts, watched" % (sub, len(ps)))
    print("%d new threads queued" % new)


def show_open(d):
    items = [i for i in d["items"] if i["status"] == "open"]
    for i in items:
        print("\n[%s] %s r/%s %s  %s" % (i["id"], i["kind"], i["sub"], i["date"], i["url"]))
        if i.get("title"):
            print("  title: %s" % i["title"])
        if i.get("in_reply_to"):
            print("  answers: %s" % i["in_reply_to"].replace("\n", " ")[:200])
        print("  text: %s" % i["text"].replace("\n", " ")[:700])
        if i.get("page"):
            print("  ours: %s" % i["page"])
        if i.get("reply"):
            print("  drafted: %s" % i["reply"])
    print("\n%d open (%d with a drafted reply)" % (len(items), sum(1 for i in items if i.get("reply"))))


def find(d, iid):
    for i in d["items"]:
        if i["id"] == iid:
            return i
    sys.exit("no item %s" % iid)


def kit(d, slug):
    cs = cities()
    if slug not in cs:
        sys.exit("no city %s" % slug)
    name, trees = cs[slug]
    c = json.load(open(os.path.join(ROOT, "data", "cities", slug + ".json"), encoding="utf-8"))
    print("Kit for a post about %s (%d trees on https://ancienttrees.app/%s)\n" % (name, len(trees), slug))
    print("His line to write: one real memory of %s. Nothing below replaces it.\n" % name)
    for q in {name.lower().replace(" ", ""), slug.replace("-", "")}:
        s = get("subreddits/search", subreddit=q, fields="display_name,subscribers")
        time.sleep(PAUSE)
        for x in s[:1]:
            print("r/%s: %s members (Arctic Shift's last count)" % (x["display_name"], x.get("subscribers")))
    print("\nTrees without a good photograph (name two in the post):")
    for t in c["trees"]:
        if (t.get("photo") or {}).get("status") != "approved":
            print("  %s  %s (%s)" % (t["id"], t["name"], (t.get("location") or {}).get("neighbourhood") or ""))
    print("\nTrees with a photograph (for the short-list shape, one sentence each):")
    for t in c["trees"]:
        if (t.get("photo") or {}).get("status") == "approved":
            print("  %s  %s, %s" % (t["id"], t["name"], t.get("age_estimate") or "age unknown"))
    done = [p for p in d["posts"] if p.get("city") == slug]
    if done:
        print("\nAlready posted about %s: %s" % (name, ", ".join("r/%s %s" % (p["sub"], p["posted"]) for p in done)))


def preview(d):
    items = [i for i in d["items"] if i["status"] == "open"]
    lines = ["# Reddit, waiting for you (%s)" % datetime.date.today().isoformat(), "",
             "You post these yourself. Each has the comment or thread, and a reply drafted in your voice.",
             "Strangers' words stay in this private file; nothing here goes in the repo.", ""]
    for kind, head in (("comment", "Under your posts"), ("thread", "Threads where one of our trees is the answer")):
        group = [i for i in items if i["kind"] == kind and i.get("reply")]
        if not group:
            continue
        lines += ["## %s (%d)" % (head, len(group)), ""]
        for i in group:
            lines.append("- **r/%s, %s** %s" % (i["sub"], i["date"], i["url"]))
            if i.get("title"):
                lines.append("  - Thread: %s" % i["title"])
            lines.append("  - They wrote: \"%s\"" % i["text"].replace("\n", " ")[:400])
            lines.append("  - Reply: %s" % i["reply"])
            lines.append("")
    waiting = sum(1 for i in items if not i.get("reply"))
    if waiting:
        lines += ["%d more open without a drafted reply yet." % waiting, ""]
    with open(PREVIEW, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("%s: %d replies drafted" % (os.path.relpath(PREVIEW, ROOT), sum(1 for i in items if i.get("reply"))))


def status(d):
    by = {}
    for i in d["items"]:
        by.setdefault((i["kind"], i["status"]), 0)
        by[(i["kind"], i["status"])] += 1
    print("%d posts of his, %d subs watched besides %d tree subs" % (len(d["posts"]), len(d["watch_subs"]), len(TREE_SUBS)))
    for (k, s), n in sorted(by.items()):
        print("  %-8s %-5s %d" % (k, s, n))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--add")
    ap.add_argument("--city")
    ap.add_argument("--harvest", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--reply", nargs=2, metavar=("ID", "TEXT"))
    ap.add_argument("--done", nargs=2, metavar=("ID", "WHY"))
    ap.add_argument("--kit")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    d = load()
    if a.add:
        add(d, a.add, a.city)
    if a.harvest:
        harvest(d)
    if a.watch:
        watch(d)
    if a.reply:
        find(d, a.reply[0])["reply"] = a.reply[1]
    if a.done:
        i = find(d, a.done[0])
        i["status"], i["note"] = "done", a.done[1]
    save(d)
    if a.open:
        show_open(d)
    if a.kit:
        kit(d, a.kit)
    if a.preview:
        preview(d)
    if a.status or not any(vars(a).values()):
        status(d)


if __name__ == "__main__":
    main()
