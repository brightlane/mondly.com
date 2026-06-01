from pathlib import Path
from datetime import date
from html import escape
import json
import re

DATA = json.loads(Path("content.json").read_text(encoding="utf-8"))

BASE_URL = DATA["base_url"].rstrip("/")
AFF_URL = DATA["affiliate_url"]
SITE_NAME = DATA["site_name"]
BRAND = DATA["brand"]
HUBS = DATA["hubs"]
FAQS = DATA["faq"]
HOME = DATA["page_templates"]["home"]
HUB_TEMPLATES = DATA["page_templates"]["hub"]
PAGE_TYPES = DATA["page_types"]
KEYWORDS = DATA["keywords"]
MODIFIERS = DATA["modifiers"]

OUT = Path("output")
OUT.mkdir(exist_ok=True)
TODAY = date.today().isoformat()

def site_root():
    return BASE_URL + "/"

def abs_url(slug: str):
    return site_root() if slug == "" else f"{site_root()}{slug}/"

def rel_url(slug: str):
    return "./" if slug == "" else f"./{slug}/"

def slugify(text: str):
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def build_pages():
    pages = []
    pages.append({
        "slug": "",
        "kind": "home",
        "title": HOME["title"],
        "description": HOME["description"],
        "h1": HOME["h1"],
        "hero_badge": HOME["hero_badge"],
        "hero_lead": HOME["hero_lead"],
        "facts": [
            "Audience: USA visitors",
            "Format: Affiliate landing page",
            "Promise: Short daily practice",
            "Goal: Drive clicks"
        ]
    })

    for hub in HUBS:
        tpl = HUB_TEMPLATES[hub["slug"]]
        pages.append({
            "slug": hub["slug"],
            "kind": "hub",
            "hub_slug": hub["slug"],
            "title": tpl["title"],
            "description": tpl["description"],
            "h1": tpl["h1"],
            "hero_badge": tpl["hero_badge"],
            "hero_lead": tpl["hero_lead"],
            "facts": [
                "Focused topic hub",
                "Links to long-tail pages",
                "Built for internal navigation",
                "Targets a distinct intent"
            ]
        })

    for ptype in PAGE_TYPES:
        for kw in KEYWORDS:
            for mod in MODIFIERS:
                slug = f"{ptype}/{kw['slug']}-{slugify(mod)}"
                title = f"{kw['head_term'].title()} {mod.title()} | Mondly USA"
                description = f"Learn about {kw['head_term']} {mod} with Mondly. USA visitors can compare features, benefits, and practical language-learning tips."
                pages.append({
                    "slug": slug,
                    "kind": "longtail",
                    "page_type": ptype,
                    "keyword": kw["head_term"],
                    "modifier": mod,
                    "title": title,
                    "description": description,
                    "h1": f"{kw['head_term'].title()} {mod.title()}",
                    "hero_badge": f"{ptype.title()} page • USA visitors",
                    "hero_lead": f"This page targets {kw['head_term']} {mod} and explains how Mondly fits that use case.",
                    "facts": [
                        f"Language focus: {kw['head_term']}",
                        f"Use case: {mod}",
                        f"Intent family: {ptype}",
                        "Affiliate offer included"
                    ]
                })
    return pages

PAGES = build_pages()

def quality_score(page, body_text, links):
    score = 0
    score += 30 if page.get("title") else 0
    score += 20 if page.get("description") else 0
    score += 20 if len(body_text.split()) >= 220 else 0
    score += 10 if len(page.get("facts", [])) >= 3 else 0
    score += 10 if len(links) >= 5 else 0
    score += 10 if page.get("canonical_ok", True) else 0
    return score

def nav_html():
    return "".join(f'<a href="{rel_url(h["slug"])}">{escape(h["title"])}</a>' for h in HUBS)

def related_links(page, all_pages):
    picks = []
    seen = set()

    def add(slug, label):
        if slug and slug not in seen and slug != page["slug"]:
            seen.add(slug)
            picks.append({"slug": slug, "label": label})

    add("", "Home")
    for h in HUBS[:5]:
        add(h["slug"], h["title"])

    if page["kind"] == "longtail":
        add("review", "Mondly Review")
        add("faq", "Mondly FAQ")
        add("alternatives", "Mondly Alternatives")
    elif page["kind"] == "hub":
        for p in all_pages:
            if p["kind"] == "longtail" and len(picks) < 8:
                add(p["slug"], p["title"])

    return picks[:8]

def faq_schema():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]}
            } for item in FAQS
        ]
    }

def text_block(page):
    if page["kind"] == "home":
        return f"""
        <section class="grid" id="details">
          <article class="card"><h2>What Mondly Does</h2><p>Mondly combines short lessons, speech practice, and conversation-based exercises to help people build vocabulary and confidence one session at a time.</p></article>
          <article class="card"><h2>Why Visitors Click</h2><p>The format is easy to understand: short lessons, voice practice, and a low-friction daily routine.</p></article>
          <article class="card"><h2>What You Get</h2><ul><li>Short daily lessons.</li><li>Speaking and voice practice.</li><li>Conversation-style learning.</li><li>Simple mobile-friendly flow.</li></ul></article>
        </section>
        """
    if page["kind"] == "hub":
        return f"""
        <section class="grid" id="details">
          <article class="card"><h2>Why this hub exists</h2><p>This hub organizes related long-tail pages and helps visitors move from a broad question to a specific answer.</p></article>
          <article class="card"><h2>How to use it</h2><p>Link this hub from long-tail pages and use it to surface the most relevant pages in the cluster.</p></article>
          <article class="card"><h2>What makes it useful</h2><p>It creates a clean topic map for crawlers and users.</p></article>
        </section>
        """
    links = related_links(page, PAGES)
    facts = "".join(f"<li>{escape(x)}</li>" for x in page["facts"])
    related = "".join(f'<a class="btn secondary" href="{rel_url(l["slug"])}">{escape(l["label"])}</a>' for l in links)
    body = f"""
    <section class="grid" id="details">
      <article class="card"><h2>Core angle</h2><p>{escape(page["keyword"])} {escape(page["modifier"])} with Mondly.</p></article>
      <article class="card"><h2>Why it matters</h2><p>This page targets a specific intent and gives users a fast answer that fits a commercial search.</p></article>
      <article class="card"><h2>Page facts</h2><ul>{facts}</ul></article>
    </section>
    <section class="card">
      <h2>Related pages</h2>
      <div class="btns">{related}</div>
    </section>
    """
    return body

def render_page(page):
    canonical = abs_url(page["slug"])
    if page["kind"] == "home":
        schema = [
            {"@type": "Organization", "name": SITE_NAME, "url": site_root(), "logo": BRAND["logo"]},
            {"@type": "WebSite", "name": SITE_NAME, "url": site_root()},
            {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": "en-US"}
        ]
    else:
        schema = [
            {"@type": "Organization", "name": SITE_NAME, "url": site_root(), "logo": BRAND["logo"]},
            {"@type": "WebSite", "name": SITE_NAME, "url": site_root()},
            {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": "en-US"}
        ]
        if page["kind"] == "hub":
            schema.append({"@type": "ItemList", "name": page["title"], "itemListElement": []})
        if page["kind"] == "longtail" and page.get("page_type") == "guide":
            schema.append({"@type": "HowTo", "name": page["title"]})

    links = related_links(page, PAGES)
    body = text_block(page)
    body_text = re.sub(r"<[^>]+>", " ", body)
    score = quality_score(page, body_text, links)
    indexable = score >= 80
    robots = "index,follow" if indexable else "noindex,nofollow"

    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <base href="{site_root()}">
  <title>{escape(page["title"])}</title>
  <meta name="description" content="{escape(page["description"])}">
  <meta name="robots" content="{robots},max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_US">
  <meta property="og:site_name" content="{escape(SITE_NAME)}">
  <meta property="og:title" content="{escape(page["title"])}">
  <meta property="og:description" content="{escape(page["description"])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{site_root()}assets/mondly-og.jpg">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": schema if isinstance(schema, list) else [schema]}, ensure_ascii=False)}</script>
</head>
<body>
  <div class="wrap">
    <nav class="nav">{nav_html()}</nav>
    <main class="hero">
      <div class="hero-inner">
        <section>
          <span class="pill">{escape(page.get("hero_badge", ""))}</span>
          <h1>{escape(page["h1"])}</h1>
          <p class="lead">{escape(page.get("hero_lead", ""))}</p>
          <div class="btns">
            <a class="btn primary" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Mondly</a>
            <a class="btn secondary" href="#details">Explore the page</a>
          </div>
        </section>
        <aside class="card">
          <h2>Fast facts</h2>
          <ul>{''.join(f'<li>{escape(f)}</li>' for f in page.get("facts", []))}</ul>
          <p><strong>Quality score:</strong> {score}/100</p>
          <p><strong>Indexable:</strong> {"yes" if indexable else "no"}</p>
        </aside>
      </div>
    </main>
    {body}
    <section class="disclosure">
      <strong>Affiliate disclosure:</strong> This page contains affiliate links. If you click and make a purchase, I may earn a commission at no extra cost to you.
    </section>
    <div class="footer">© 2026 • USA-only language learning promo</div>
  </div>
  <div class="sticky" role="region" aria-label="Sticky call to action">
    <div class="inner">
      <div><strong>Ready to try Mondly?</strong><small>Start with the offer below.</small></div>
      <a class="mini" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Mondly</a>
    </div>
  </div>
</body>
</html>"""

OUT.mkdir(exist_ok=True)
for page in PAGES:
    target = OUT if page["slug"] == "" else OUT / page["slug"]
    target.mkdir(parents=True, exist_ok=True)
    (target / "index.html").write_text(render_page(page), encoding="utf-8")

(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site_root()}sitemap.xml\n", encoding="utf-8")
(OUT / "llms.txt").write_text(f"# {SITE_NAME}\n\n{DATA['site_summary']}\n", encoding="utf-8")
(OUT / "404.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex,nofollow'><meta http-equiv='refresh' content='5;url={site_root()}'></head><body><p>Page not found.</p></body></html>", encoding="utf-8")

sitemap = ["<?xml version='1.0' encoding='UTF-8'?>", "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
for page in PAGES:
    sitemap.append(f"  <url><loc>{abs_url(page['slug'])}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

print(f"Built {len(PAGES)} pages to output/")
