from pathlib import Path
from datetime import date
from html import escape
import json
import shutil
import itertools

DATA = json.loads(Path("content.json").read_text(encoding="utf-8"))

BASE_URL = DATA["base_url"].rstrip("/")
AFF_URL = DATA["affiliate_url"]
SITE_NAME = DATA["site_name"]
BRAND = DATA["brand"]
HOME = DATA["page_templates"]["home"]
HUBS = DATA["hubs"]
FAQS = DATA["faq"]
KEYWORDS = DATA["keywords"]
MODIFIERS = DATA["modifiers"]
PAGE_TYPES = DATA["page_types"]
HUB_TEMPLATES = DATA["page_templates"]["hub"]

ROOT = Path(".")
OUT = Path("output")
OUT.mkdir(exist_ok=True)
TODAY = date.today().isoformat()

def site_root():
    return BASE_URL + "/"

def abs_url(slug: str) -> str:
    return site_root() if slug == "" else f"{site_root()}{slug}/"

def rel_url(slug: str) -> str:
    return "./" if slug == "" else f"./{slug}/"

def slugify(text: str) -> str:
    return text.lower().replace("&", "and").replace("/", "-").replace(" ", "-").replace("--", "-")

def build_page_list():
    pages = []
    pages.append({"slug": "", "type": "home", **HOME})
    for hub in HUBS:
        pages.append({
            "slug": hub["slug"],
            "type": hub["slug"],
            "title": HUB_TEMPLATES[hub["slug"]]["title"],
            "description": HUB_TEMPLATES[hub["slug"]]["description"],
            "h1": HUB_TEMPLATES[hub["slug"]]["h1"],
            "hero_badge": HUB_TEMPLATES[hub["slug"]]["hero_badge"],
            "hero_lead": HUB_TEMPLATES[hub["slug"]]["hero_lead"]
        })
    count = 0
    for kw in KEYWORDS:
        for mod in MODIFIERS:
            for ptype in PAGE_TYPES:
                if count >= 1000:
                    return pages
                slug = f"{ptype}/{kw['slug']}-{slugify(mod)}"
                title = f"{kw['head_term'].title()} {mod.title()} | Mondly USA"
                desc = f"Learn about {kw['head_term']} {mod} with Mondly. USA visitors can compare features, benefits, and practical language-learning tips."
                h1 = f"{kw['head_term'].title()} {mod.title()}"
                pages.append({
                    "slug": slug,
                    "type": ptype,
                    "keyword": kw["head_term"],
                    "modifier": mod,
                    "title": title,
                    "description": desc,
                    "h1": h1,
                    "hero_badge": f"{ptype.title()} page • USA visitors",
                    "hero_lead": f"This page targets {kw['head_term']} {mod} and explains how Mondly fits that use case."
                })
                count += 1
    return pages

PAGES = build_page_list()

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
.faq-item,.alt-item,.page-item{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin-top:12px}
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

def faq_schema():
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]}
            } for item in FAQS
        ]
    }

def nav_html():
    items = [('<a href="./">Home</a>')] + [f'<a href="./{hub["slug"]}/">{hub["slug"].title()}</a>' for hub in HUBS]
    return "".join(items)

def render_faq():
    blocks = []
    for item in FAQS:
        blocks.append(f'<article class="faq-item"><h3>{escape(item["question"])}</h3><p>{escape(item["answer"])}</p></article>')
    return f'<section class="card" id="faq"><h2>Frequently Asked Questions</h2>{"".join(blocks)}</section>'

def render_list_page(title, items):
    blocks = []
    for item in items[:24]:
        blocks.append(f'<article class="page-item"><strong>{escape(item.get("title", item.get("name", "Page")))}</strong><p>{escape(item.get("description", item.get("summary", "")))}</p></article>')
    return f'<section class="card" id="details"><h2>{escape(title)}</h2>{"".join(blocks)}</section>'

def render_body(page):
    if page["type"] == "home":
        return f"""
        <section class="meta-row" aria-label="Key facts">
          <div class="meta"><strong>Audience</strong><br>USA visitors</div>
          <div class="meta"><strong>Format</strong><br>Affiliate landing page</div>
          <div class="meta"><strong>Promise</strong><br>Short daily practice</div>
          <div class="meta"><strong>Goal</strong><br>Drive clicks</div>
        </section>
        <section class="grid" id="details">
          <article class="card"><h2>What Mondly Does</h2><p>Mondly combines short lessons, speech practice, and conversation-based exercises to help people build vocabulary and confidence one session at a time.</p></article>
          <article class="card"><h2>Why Visitors Click</h2><p>The format is easy to understand: short lessons, voice practice, and a low-friction daily routine.</p></article>
          <article class="card"><h2>What You Get</h2><ul><li>Short daily lessons.</li><li>Speaking and voice practice.</li><li>Conversation-style learning.</li><li>Simple mobile-friendly flow.</li></ul></article>
        </section>
        <section class="steps" aria-label="How it works">
          <article class="card"><div class="step-num">1</div><h3>Choose a topic</h3><p>Select a language, use case, or comparison page.</p></article>
          <article class="card"><div class="step-num">2</div><h3>Read the guide</h3><p>Each page gives a focused answer for one search intent.</p></article>
          <article class="card"><div class="step-num">3</div><h3>Click the offer</h3><p>The CTA always leads to the Mondly affiliate offer.</p></article>
        </section>
        {render_faq()}
        """
    if page["type"] in PAGE_TYPES:
        return render_list_page(page["h1"], PAGES)
    return f"""
    <section class="card">
      <p>This page is provided for informational and promotional purposes only.</p>
      <p>Affiliate links may generate a commission without additional cost to you.</p>
    </section>
    """

def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def build_page(page):
    slug = page["slug"]
    out_dir = OUT if slug == "" else OUT / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    canonical = abs_url(slug)

    schema = [
        {"@type": "Organization", "name": SITE_NAME, "url": site_root(), "logo": BRAND["logo"]},
        {"@type": "WebSite", "name": SITE_NAME, "url": site_root()},
        {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": "en-US"}
    ]
    if page["type"] == "faq":
        schema.append(faq_schema())

    html = f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <base href="{site_root()}">
  <title>{escape(page["title"])}</title>
  <meta name="description" content="{escape(page["description"])}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_US">
  <meta property="og:site_name" content="{escape(SITE_NAME)}">
  <meta property="og:title" content="{escape(page["title"])}">
  <meta property="og:description" content="{escape(page["description"])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{site_root()}assets/mondly-og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(page["title"])}">
  <meta name="twitter:description" content="{escape(page["description"])}">
  <meta name="twitter:image" content="{site_root()}assets/mondly-og.jpg">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":schema}, ensure_ascii=False)}</script>
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
          <ul>
            <li>Short daily lessons.</li>
            <li>Speaking and voice practice.</li>
            <li>Built for easy daily use.</li>
            <li>Optimized for USA traffic.</li>
          </ul>
        </aside>
      </div>
    </main>
    {render_body(page)}
    <section class="disclosure">
      <strong>Affiliate disclosure:</strong> This page contains affiliate links. If you click and make a purchase, I may earn a commission at no extra cost to you.
    </section>
    <div class="footer">© 2026 • USA-only language learning promo</div>
  </div>
  <div class="sticky"><div class="inner"><div><strong>Ready to try Mondly?</strong><small>Start with the offer below.</small></div><a class="mini" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Mondly</a></div></div>
</body>
</html>"""
    write(out_dir / "index.html", html)

for page in PAGES:
    build_page(page)

robots = f"User-agent: *\nAllow: /\nSitemap: {site_root()}sitemap.xml\n"
write(OUT / "robots.txt", robots)
write(OUT / "llms.txt", f"# {SITE_NAME}\n\n{DATA['site_summary']}\n")
write(OUT / "404.html", f"<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex,nofollow'><meta http-equiv='refresh' content='5;url={site_root()}'></head><body><p>Page not found.</p></body></html>")

sitemap = ["<?xml version='1.0' encoding='UTF-8'?>", "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
for page in PAGES:
    sitemap.append(f"  <url><loc>{abs_url(page['slug'])}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
write(OUT / "sitemap.xml", "\n".join(sitemap))

write(OUT / ".nojekyll", "")
print(f"Built {len(PAGES)} pages to output/")
