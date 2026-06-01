from pathlib import Path
from datetime import date
from html import escape
import json
import re
import sys

CONTENT_PATH = Path("content.json")
OUT = Path("output")

def load_json_file(path: Path):
    if not path.exists():
        sys.exit(f"{path} not found")
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        sys.exit(f"{path} is empty")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"{path} is invalid JSON: {e}")

DATA = load_json_file(CONTENT_PATH)

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
TODAY = date.today().isoformat()

OUT.mkdir(exist_ok=True)

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
                pages.append({
                    "slug": slug,
                    "kind": "longtail",
                    "page_type": ptype,
                    "keyword": kw["head_term"],
                    "modifier": mod,
                    "title": f"{kw['head_term'].title()} {mod.title()} | Mondly USA",
                    "description": f"Learn about {kw['head_term']} {mod} with Mondly. USA visitors can compare features, benefits, and practical language-learning tips.",
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

CSS = """
:root{
  --bg:#07111f; --card:#101a2d; --text:#e5e7eb; --muted:#94a3b8; --line:#23314a;
  --accent:#22c55e; --shadow:0 24px 70px rgba(0,0,0,.35); --max:1160px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;font-family:Inter,Arial,Helvetica,sans-serif;
  background:radial-gradient(circle at top left, rgba(56,189,248,.15), transparent 30%),
             radial-gradient(circle at top right, rgba(34,197,94,.12), transparent 30%),
             linear-gradient(180deg,#07111f 0%,#08101d 100%);
  color:var(--text);line-height:1.6;text-rendering:optimizeLegibility;
}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--max);margin:0 auto;padding:18px}
.nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.nav a{padding:8px 12px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.03);color:#dbeafe}
.hero{border:1px solid var(--line);border-radius:28px;box-shadow:var(--shadow);overflow:hidden;background:linear-gradient(180deg, rgba(16,26,45,.98), rgba(10,18,34,.98))}
.hero-inner{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;padding:34px;align-items:center}
h1{margin:12px 0 14px;font-size:clamp(2rem,5vw,4.25rem);line-height:1.02;letter-spacing:-.04em}
.lead{font-size:1.08rem;color:#cbd5e1;margin:0 0 22px;max-width:62ch}
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(34,197,94,.22);background:rgba(34,197,94,.1);color:#bbf7d0;padding:7px 12px;border-radius:999px;font-size:.86rem;font-weight:800}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{min-height:52px;padding:14px 20px;border-radius:16px;font-weight:900;display:inline-flex;align-items:center;justify-content:center;border:1px solid transparent}
.primary{background:linear-gradient(135deg,var(--accent),#16a34a);color:#04120a}
.secondary{background:rgba(255,255,255,.03);border-color:var(--line)}
.grid{margin-top:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{background:rgba(16,26,45,.96);border:1px solid var(--line);border-radius:24px;padding:22px;box-shadow:0 12px 36px rgba(0,0,0,.16)}
.card p,.card li{color:var(--muted)}
.card ul{margin:0;padding-left:18px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px}
.step-num{width:36px;height:36px;border-radius:12px;display:grid;place-items:center;background:rgba(56,189,248,.12);color:#bae6fd;font-weight:900;margin-bottom:10px;border:1px solid rgba(56,189,248,.18)}
.faq-item,.page-item{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin-top:12px}
.faq-item h3{margin:0 0 8px;font-size:1.02rem}
.faq-item p{margin:0;color:var(--muted)}
.disclosure{margin-top:18px;padding:18px 20px;border-radius:20px;background:rgba(248,113,113,.08);border:1px solid rgba(248,113,113,.18);color:#fecaca;font-size:.95rem}
.footer{padding:22px 4px 8px;color:var(--muted);font-size:.9rem;text-align:center}
.sticky{position:fixed;left:0;right:0;bottom:0;background:rgba(7,17,31,.9);backdrop-filter:blur(14px);border-top:1px solid rgba(35,49,74,.9);padding:12px 16px}
.sticky .inner{max-width:var(--max);margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.mini{padding:12px 16px;border-radius:14px;background:linear-gradient(135deg,var(--accent),#16a34a);color:#04120a;font-weight:900;display:inline-flex;align-items:center;justify-content:center;min-height:46px}
.meta-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
.meta{padding:14px;border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.03);color:#cbd5e1;font-size:.95rem}
@media (max-width:900px){.hero-inner,.grid,.steps,.meta-row{grid-template-columns:1fr}.hero-inner{padding:20px}}
@media (max-width:640px){.wrap{padding:14px}h1{font-size:clamp(1.9rem,11vw,3rem)}.btns{display:grid;grid-template-columns:1fr}.btn,.mini{width:100%}.sticky .inner{flex-direction:column;align-items:stretch}}
"""

def related_links(page):
    links = [{"slug": "", "label": "Home"}]
    for hub in HUBS[:5]:
        links.append({"slug": hub["slug"], "label": hub["title"]})
    if page["kind"] == "longtail":
        links.extend([
            {"slug": "review", "label": "Mondly Review"},
            {"slug": "faq", "label": "Mondly FAQ"},
            {"slug": "alternatives", "label": "Mondly Alternatives"}
        ])
    return links[:8]

def quality_score(page, body_text, links):
    score = 0
    score += 30 if page.get("title") else 0
    score += 20 if page.get("description") else 0
    score += 20 if len(body_text.split()) >= 220 else 0
    score += 10 if len(page.get("facts", [])) >= 3 else 0
    score += 10 if len(links) >= 5 else 0
    score += 10
    return score

def render_body(page):
    if page["kind"] == "home":
        return """
        <section class="grid" id="details">
          <article class="card"><h2>What Mondly Does</h2><p>Mondly combines short lessons, speech practice, and conversation-based exercises to help people build vocabulary and confidence one session at a time.</p></article>
          <article class="card"><h2>Why Visitors Click</h2><p>The format is easy to understand: short lessons, voice practice, and a low-friction daily routine.</p></article>
          <article class="card"><h2>What You Get</h2><ul><li>Short daily lessons.</li><li>Speaking and voice practice.</li><li>Conversation-style learning.</li><li>Simple mobile-friendly flow.</li></ul></article>
        </section>
        """
    if page["kind"] == "hub":
        return """
        <section class="grid" id="details">
          <article class="card"><h2>Why this hub exists</h2><p>This hub organizes related long-tail pages and helps visitors move from a broad question to a specific answer.</p></article>
          <article class="card"><h2>How to use it</h2><p>Link this hub from long-tail pages and use it to surface the most relevant pages in the cluster.</p></article>
          <article class="card"><h2>What makes it useful</h2><p>It creates a clean topic map for crawlers and users.</p></article>
        </section>
        """
    facts = "".join(f"<li>{escape(f)}</li>" for f in page["facts"])
    links = "".join(f'<a class="btn secondary" href="{rel_url(l["slug"])}">{escape(l["label"])}</a>' for l in related_links(page))
    return f"""
    <section class="grid" id="details">
      <article class="card"><h2>Core angle</h2><p>{escape(page["keyword"])} {escape(page["modifier"])} with Mondly.</p></article>
      <article class="card"><h2>Why it matters</h2><p>This page targets a specific intent and gives users a fast answer that fits a commercial search.</p></article>
      <article class="card"><h2>Page facts</h2><ul>{facts}</ul></article>
    </section>
    <section class="card">
      <h2>Related pages</h2>
      <div class="btns">{links}</div>
    </section>
    """

def render_page(page):
    canonical = abs_url(page["slug"])
    links = related_links(page)
    body = render_body(page)
    body_text = re.sub(r"<[^>]+>", " ", body)
    score = quality_score(page, body_text, links)
    indexable = score >= 80
    robots = "index,follow" if indexable else "noindex,nofollow"

    schema_graph = [
        {"@type": "Organization", "name": SITE_NAME, "url": site_root(), "logo": BRAND["logo"]},
        {"@type": "WebSite", "name": SITE_NAME, "url": site_root()},
        {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": "en-US"}
    ]

    if page["kind"] == "hub":
        schema_graph.append({"@type": "CollectionPage", "name": page["title"], "url": canonical})
    if page["kind"] == "home":
        schema_graph.append({"@type": "FAQPage", "mainEntity": [{"@type":"Question","name":f["question"],"acceptedAnswer":{"@type":"Answer","text":f["answer"]}} for f in FAQS]})

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
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":schema_graph}, ensure_ascii=False)}</script>
</head>
<body>
  <div class="wrap">
    <nav class="nav">{''.join(f'<a href="{rel_url(h["slug"])}">{escape(h["title"])}</a>' for h in HUBS)}</nav>
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
  <div class="sticky">
    <div class="inner">
      <div><strong>Ready to try Mondly?</strong><small>Start with the offer below.</small></div>
      <a class="mini" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Mondly</a>
    </div>
  </div>
</body>
</html>"""

for page in PAGES:
    out_dir = OUT if page["slug"] == "" else OUT / page["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render_page(page), encoding="utf-8")

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
