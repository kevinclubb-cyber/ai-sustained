#!/usr/bin/env python3
"""Rebuild everything that helps search engines and readers find the site.

Source of truth: search-index.json (one entry per article and case study).
Run from the repo root after adding or editing an entry:

    python3 -I scripts/build-discovery.py

It is safe to run repeatedly. It writes:
  - articles/index.html        the index of every issue
  - feed.xml                   RSS feed of articles and case studies
  - sitemap.xml                adds <lastmod>, keeps order and priorities
  - llms.txt                   appends any page not yet listed
and, inside every article and case study, between marker comments:
  - a "Keep reading" block of three related pieces (before the footer)
  - breadcrumb structured data, the feed link and any missing social tags
"""
import datetime
import html
import json
import os
import re
import subprocess

HOST = "https://ai-sustained.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today().isoformat()
STOP = set(
    "the a an and or of to in is it its for on with that this what why how you your "
    "not no are was be as at by from one who now ai we us our they their than then "
    "can could would have has had will just into out up when if but so do does did".split()
)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    if os.path.exists(path) and read(path) == text:
        return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def page_file(url):
    return os.path.join(url.strip("/"), "index.html") if url != "/" else "index.html"


def esc(text):
    return html.escape(html.unescape(text), quote=True)


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def between(text, name, block, anchor_re, before=True, last=False):
    """Put `block` between <!-- name:start/end --> markers, replacing an old one."""
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    text = re.sub(re.escape(start) + r"[\s\S]*?" + re.escape(end) + r"\n?", "", text)
    if not block:
        return text
    found = list(re.finditer(anchor_re, text))
    if not found:
        raise SystemExit(f"no anchor {anchor_re!r} for {name}")
    m = found[-1] if last else found[0]
    at = m.start() if before else m.end()
    return text[:at] + f"{start}\n{block}\n{end}\n" + text[at:]


# ---------------------------------------------------------------- catalogue
index = json.loads(read("search-index.json"))["pages"]
items = [
    p
    for p in index
    if re.fullmatch(r"/(articles|case-studies)/[^/]+/", p["url"])
    and os.path.exists(page_file(p["url"]))
    and "noindex" not in read(page_file(p["url"]))[:20000]
]
items.sort(key=lambda p: p["date"], reverse=True)
by_url = {p["url"]: p for p in items}
home, cases = read("index.html"), read("case-studies/index.html")


def cover(p):
    for source in (home, cases):
        m = re.search(
            r'href="' + re.escape(p["url"]) + r'"[^>]*>[\s\S]{0,400}?<img[^>]*\bsrc="([^"]+)"[^>]*\balt="([^"]*)"',
            source,
        )
        if m:
            return m.group(1), html.unescape(m.group(2))
    return None, ""


def words(p):
    text = f"{p['title']} {p.get('tags', '')} {p.get('tags', '')} {p['summary']}".lower()
    return {w for w in re.findall(r"[a-z0-9]{3,}", text) if w not in STOP}


for p in items:
    p["words"] = words(p)
    p["cover"], p["alt"] = cover(p)
    p["kind"] = "Case study" if p["url"].startswith("/case-studies/") else "Article"


def related(p, n=3):
    def score(q):
        shared = len(p["words"] & q["words"])
        return (shared / (len(p["words"] | q["words"]) or 1), q["date"])

    ranked = sorted((q for q in items if q is not p), key=score, reverse=True)
    picks = ranked[:n]
    # Always offer one piece of the other kind, so articles feed case studies.
    if all(q["kind"] == p["kind"] for q in picks):
        other = next((q for q in ranked if q["kind"] != p["kind"]), None)
        if other:
            picks[-1] = other
    return picks


# ------------------------------------------------- per-page blocks and tags
MORE_CSS = (
    ".ais-more{box-sizing:border-box;width:100%;clear:both;background:#143326;color:#F2ECD9;"
    "border-top:1px solid rgba(242,236,217,.18);padding:44px 24px 40px;text-align:left}"
    ".ais-more *{box-sizing:border-box}"
    ".ais-more-in{max-width:1100px;margin:0 auto}"
    ".ais-more-k{font:600 11px/1.4 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;"
    "color:#E8FF3A;margin:0 0 18px}"
    ".ais-more-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}"
    ".ais-more-g a{display:flex;flex-direction:column;gap:10px;padding:20px;border:1px solid rgba(242,236,217,.18);"
    "border-radius:6px;background:rgba(242,236,217,.05);color:#F2ECD9;text-decoration:none;"
    "transition:border-color .15s,transform .15s}"
    ".ais-more-g a:hover,.ais-more-g a:focus-visible{border-color:#E8FF3A;transform:translateY(-2px)}"
    ".ais-more-r{font:500 10.5px/1.4 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;"
    "color:rgba(242,236,217,.62)}"
    ".ais-more-t{font:600 20px/1.25 'Fraunces',Georgia,serif;color:#F2ECD9}"
    ".ais-more-s{font:400 14px/1.55 'Inter',system-ui,sans-serif;color:#D8F3DC}"
    ".ais-more-all{margin:22px 0 0;font:500 12px/1.6 'JetBrains Mono',monospace;letter-spacing:.06em}"
    ".ais-more-all a{color:#E8FF3A;text-decoration:none;border-bottom:1px solid transparent;margin-right:22px}"
    ".ais-more-all a:hover,.ais-more-all a:focus-visible{border-bottom-color:#E8FF3A}"
    "@media(max-width:820px){.ais-more-g{grid-template-columns:1fr}.ais-more{padding:36px 18px 32px}}"
)


def more_block(p):
    cards = "\n".join(
        f'    <a href="{q["url"]}"><span class="ais-more-r">{esc(q["ref"])} &middot; {nice_date(q["date"])}</span>'
        f'<span class="ais-more-t">{esc(q["title"])}</span>'
        f'<span class="ais-more-s">{esc(q["summary"])}</span></a>'
        for q in related(p)
    )
    return (
        f'<aside class="ais-more" aria-label="Keep reading">\n<style>{MORE_CSS}</style>\n'
        f'  <div class="ais-more-in">\n    <p class="ais-more-k">Keep reading</p>\n'
        f'    <div class="ais-more-g">\n{cards}\n    </div>\n'
        f'    <p class="ais-more-all"><a href="/articles/">All articles &rarr;</a>'
        f'<a href="/case-studies/">All case studies &rarr;</a></p>\n  </div>\n</aside>'
    )


FEED_LINK = '<link rel="alternate" type="application/rss+xml" title="AI Sustained" href="/feed.xml">'


def meta_of(text, pattern):
    m = re.search(pattern, text, re.S | re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def head_block(text, url, title, desc, image, kind, crumbs, article=None):
    lines = [FEED_LINK]
    have = lambda key: re.search(r'(property|name)="' + re.escape(key) + '"', text)
    wanted = [
        ("property", "og:title", title),
        ("property", "og:description", desc),
        ("property", "og:type", kind),
        ("property", "og:url", HOST + url),
        ("property", "og:image", image),
        ("property", "og:site_name", "AI Sustained"),
        ("name", "twitter:card", "summary_large_image"),
        ("name", "twitter:title", title),
        ("name", "twitter:description", desc),
        ("name", "twitter:image", image),
    ]
    lines += [f'<meta {attr}="{key}" content="{esc(value)}">' for attr, key, value in wanted if not have(key)]
    if crumbs and "BreadcrumbList" not in text:
        data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": name, "item": HOST + path}
                for i, (name, path) in enumerate(crumbs)
            ],
        }
        lines.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>")
    if article and not re.search(r'"@type"\s*:\s*"(Article|NewsArticle|BlogPosting)"', text):
        lines.append('<script type="application/ld+json">' + json.dumps(article, ensure_ascii=False) + "</script>")
    return "\n".join(lines)


def strip_markers(text):
    return re.sub(r"<!-- ais-(head|more):start -->[\s\S]*?<!-- ais-\1:end -->\n?", "", text)


changed = []
for p in items:
    path = page_file(p["url"])
    text = strip_markers(read(path))
    # The page's published date also stands as its modified date until edited.
    if '"dateModified"' not in text:
        text = re.sub(
            r'("datePublished"\s*:\s*"([^"]+)")', r'\1,\n  "dateModified": "\2"', text, count=1
        )
    title = meta_of(text, r'property="og:title"\s+content="([^"]*)"') or p["title"]
    desc = meta_of(text, r'name="description"\s+content="([^"]*)"') or p["summary"]
    image = meta_of(text, r'property="og:image"\s+content="([^"]*)"')
    if not image:
        folder = os.path.dirname(path)
        local = next((f for f in ("cover.jpg", "og.jpg") if os.path.exists(os.path.join(folder, f))), None)
        image = HOST + p["url"] + local if local else HOST + "/og-card.png"
    section = ("Case studies", "/case-studies/") if p["kind"] == "Case study" else ("Articles", "/articles/")
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["title"],
        "description": desc,
        "image": image,
        "datePublished": p["date"],
        "dateModified": p["date"],
        "mainEntityOfPage": HOST + p["url"],
        "author": {"@type": "Person", "name": "Kevin Clubb", "url": HOST + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "AI Sustained",
            "logo": {"@type": "ImageObject", "url": HOST + "/ai_sustained_logo.png"},
        },
    }
    head = head_block(
        text, p["url"], title, desc, image, "article", [("Home", "/"), section, (p["title"], p["url"])], article
    )
    text = between(text, "ais-head", head, r"</head>")
    text = between(text, "ais-more", more_block(p), r"<footer\b", last=True)
    if write(path, text):
        changed.append(path)

# Other indexable pages: feed link and any missing social tags.
for url in ("/", "/case-studies/", "/learn/", "/learn/score/", "/learn/programme/", "/learn/terms/", "/ledger/", "/advertise/", "/privacy/"):
    path = page_file(url)
    text = strip_markers(read(path))
    title = meta_of(text, r"<title>(.*?)</title>")
    desc = meta_of(text, r'name="description"\s+content="([^"]*)"')
    image = meta_of(text, r'property="og:image"\s+content="([^"]*)"') or HOST + "/og-card.png"
    text = between(text, "ais-head", head_block(text, url, title, desc, image, "website", None), r"</head>")
    if write(path, text):
        changed.append(path)

# ------------------------------------------------------------ articles index
articles = [p for p in items if p["kind"] == "Article"]
head_end = cases.index("<body")
shell_head = strip_markers(cases[:head_end])
style = re.search(r"<style>[\s\S]*?</style>", shell_head[shell_head.index('rel="stylesheet"'):]).group(0)
scripts = shell_head[: shell_head.index('<meta name="viewport"')]
topbar = re.search(r'<body>[\s\S]*?</header>\s*</div>', cases).group(0).replace(' class="active"', "")
topbar = topbar.replace('<a href="/#editorial">Editorial</a>', '<a href="/articles/" class="active">Editorial</a>')
tail = strip_markers(cases[cases.rindex('<footer class="brand-footer"'):]).replace(
    "AI Sustained · Case studies · 2026", "AI Sustained · Editorial · 2026"
)
A_TITLE = "All AI Sustained articles: plain-English AI for UK business"
A_DESC = (
    f"Every AI Sustained issue in one place: {len(articles)} plain-English articles on AI adoption, new models, "
    "safety, costs and what they mean for UK businesses. Newest first."
)
listing = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "AI Sustained articles",
    "url": HOST + "/articles/",
    "description": A_DESC,
    "isPartOf": {"@type": "WebSite", "name": "AI Sustained", "url": HOST},
    "breadcrumb": {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": HOST + "/"},
            {"@type": "ListItem", "position": 2, "name": "Articles", "item": HOST + "/articles/"},
        ],
    },
    "mainEntity": {
        "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": HOST + p["url"], "name": p["title"]}
            for i, p in enumerate(articles)
        ],
    },
}
cards = "\n".join(
    f'  <a class="cs-card" href="{p["url"]}">\n'
    + (
        f'    <div class="c-img"><img src="{p["cover"]}" alt="{esc(p["alt"])}" loading="{"eager" if i < 2 else "lazy"}">'
        f'<span class="c-num">{esc(p["ref"])}</span></div>\n'
        if p["cover"]
        else ""
    )
    + f'    <div class="c-body">\n      <div class="c-meta"><span>{esc(p["ref"])}</span><span class="dot"></span>'
    f'<span class="muted"><time datetime="{p["date"]}">{nice_date(p["date"])}</time></span></div>\n'
    f'      <h2>{esc(p["title"])}</h2>\n      <p class="blurb">{esc(p["summary"])}</p>\n'
    f'      <span class="c-cta">Read the article</span>\n    </div>\n  </a>'
    for i, p in enumerate(articles)
)
page = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
{scripts[scripts.index('<meta charset="UTF-8">') + len('<meta charset="UTF-8">'):].strip()}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Generated by scripts/build-discovery.py from search-index.json. Do not edit by hand. -->
<title>{esc(A_TITLE)}</title>
<meta name="description" content="{esc(A_DESC)}">
<meta name="author" content="Kevin Clubb">
<link rel="canonical" href="{HOST}/articles/">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{esc(A_TITLE)}">
<meta property="og:description" content="{esc(A_DESC)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{HOST}/og-card.png">
<meta property="og:url" content="{HOST}/articles/">
<meta property="og:site_name" content="AI Sustained">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(A_TITLE)}">
<meta name="twitter:description" content="{esc(A_DESC)}">
<meta name="twitter:image" content="{HOST}/og-card.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<link rel="icon" type="image/png" sizes="512x512" href="/favicon-512.png">
<meta name="theme-color" content="#1B4332">
{FEED_LINK}
<script type="application/ld+json">{json.dumps(listing, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500;1,9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
{style}
<style>.hero.all-articles{{grid-template-columns:minmax(0,1fr)}}.cs-card .c-img img{{aspect-ratio:16/9;object-fit:cover;width:100%;height:auto;display:block}}</style>
</head>
{topbar}
<header class="hero all-articles">
  <div class="hero-copy">
    <div class="breadcrumb"><a href="/">Home</a> &nbsp;/&nbsp; Articles</div>
    <div class="hero-kicker">Editorial · Every issue</div>
    <h1>Every issue, <em>newest first</em>.</h1>
    <p class="deck">{len(articles)} plain-English pieces on what AI is doing, what it costs and what it changes for people at work in the UK. For the builds behind the arguments, see the <a href="/case-studies/" style="color:var(--acid)">case studies</a>.</p>
  </div>
</header>
<section class="cs-grid">
{cards}
</section>
{tail}"""
if write("articles/index.html", page):
    changed.append("articles/index.html")

# ---------------------------------------------------------------------- feed
def rfc822(iso):
    d = datetime.datetime.fromisoformat(iso + "T08:00:00+00:00")
    return d.strftime("%a, %d %b %Y %H:%M:%S +0000")


feed_items = "\n".join(
    f"  <item>\n    <title>{html.escape(html.unescape(p['title']))}</title>\n    <link>{HOST}{p['url']}</link>\n"
    f"    <guid isPermaLink=\"true\">{HOST}{p['url']}</guid>\n    <pubDate>{rfc822(p['date'])}</pubDate>\n"
    f"    <category>{p['kind']}</category>\n"
    f"    <description>{html.escape(html.unescape(p['summary']))}</description>\n  </item>"
    for p in items
)
feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>AI Sustained</title>
  <link>{HOST}/</link>
  <atom:link href="{HOST}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>AI that survives Monday morning. Plain-English articles and real case studies on AI at work in the UK, by Kevin Clubb.</description>
  <language>en-gb</language>
  <lastBuildDate>{rfc822(items[0]['date'])}</lastBuildDate>
{feed_items}
</channel>
</rss>
"""
if write("feed.xml", feed):
    changed.append("feed.xml")

# ------------------------------------------------------------------- sitemap
def last_changed(path):
    dirty = subprocess.run(["git", "status", "--porcelain", "--", path], capture_output=True, text=True).stdout
    if dirty.strip():
        return TODAY
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], capture_output=True, text=True).stdout
    return out.strip() or TODAY


sitemap = read("sitemap.xml")
entries = re.findall(r"<url>([\s\S]*?)</url>", sitemap)
rows, seen = [], set()
for entry in entries:
    loc = re.search(r"<loc>([^<]+)</loc>", entry).group(1)
    freq = re.search(r"<changefreq>([^<]+)", entry)
    prio = re.search(r"<priority>([^<]+)", entry)
    rows.append((loc, freq.group(1) if freq else "monthly", prio.group(1) if prio else "0.7"))
    seen.add(loc)
for loc, freq, prio in ((HOST + "/articles/", "weekly", "0.9"),):
    if loc not in seen:
        rows.insert(2, (loc, freq, prio))
        seen.add(loc)
for p in items:
    if HOST + p["url"] not in seen:
        rows.append((HOST + p["url"], "monthly", "0.8"))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, freq, prio in rows:
    out += [
        "  <url>",
        f"    <loc>{loc}</loc>",
        f"    <lastmod>{last_changed(page_file(loc[len(HOST):]))}</lastmod>",
        f"    <changefreq>{freq}</changefreq>",
        f"    <priority>{prio}</priority>",
        "  </url>",
    ]
out.append("</urlset>\n")
if write("sitemap.xml", "\n".join(out)):
    changed.append("sitemap.xml")

# ------------------------------------------------------------------ llms.txt
llms = read("llms.txt")
missing = [p for p in items if HOST + p["url"] not in llms]
if missing or "/feed.xml" not in llms:
    extra = []
    if missing:
        extra.append("\n## More from the archive")
        extra += [f"- [{html.unescape(p['title'])}]({HOST}{p['url']}): {html.unescape(p['summary'])}" for p in missing]
    if "/feed.xml" not in llms:
        extra += [
            "\n## Find everything",
            f"- [All articles]({HOST}/articles/): every issue, newest first.",
            f"- [RSS feed]({HOST}/feed.xml): articles and case studies as they are published.",
            f"- [Sitemap]({HOST}/sitemap.xml)",
        ]
    if write("llms.txt", llms.rstrip("\n") + "\n" + "\n".join(extra) + "\n"):
        changed.append("llms.txt")

print(f"{len(items)} pieces ({len(articles)} articles); {len(changed)} files written")
for path in changed:
    print("  ", path)
