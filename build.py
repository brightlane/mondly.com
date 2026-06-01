from pathlib import Path
from datetime import date
import json
from html import escape

DATA = json.loads(Path("content.json").read_text(encoding="utf-8"))

BASE_URL = DATA["base_url"].rstrip("/")
AFF_URL = DATA["affiliate_url"]
SITE_NAME = DATA["site_name"]
BRAND = DATA["brand"]
PAGES = DATA["pages"]
FAQ_ITEMS = DATA["faq"]
ALT_ITEMS = DATA["alternatives"]
NAV = DATA["nav"]

OUT = Path("output")
OUT.mkdir(exist_ok=True)
TODAY = date.today().isoformat()

CSS = """
:root{
  --bg:#07111f;
  --card:#101a2d;
  --text:#e5e7eb;
  --muted:#94a3b8;
  --line:#23314a;
  --accent:#22c55e;
  --accent2:#38bdf8;
  --shadow:0 24px 70px rgba(0,0,0,.35);
  --max:1160px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  font-family:Inter,Arial,Helvetica,sans-serif;
  background:
    radial-gradient(circle at top left, rgba(56,189,248,.15), transparent 30%),
    radial-gradient(circle at top right, rgba(34,197,94,.12), transparent 30%),
    linear-gradient(180deg,#07111f 0%,#08101d 100%);
  color:var(--text);
  line-height:1.6;
  text-rendering:optimizeLegibility;
}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--max);margin:0 auto;padding:18px}
.nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.nav a{
  padding:8px 12px;
  border:1px solid var(--line);
  border-radius:999px;
  background:rgba(255,255,255,.03);
  color:#dbeafe;
}
.hero{
  border:1px solid var(--line);
  border-radius:28px;
  box-shadow:var(--shadow);
  overflow:hidden;
  background:linear-gradient(180deg, rgba(16,26,45,.98), rgba(10,18,34,.98));
}
.hero-inner{
  display:grid;
  grid-template-columns:1.1fr .9fr;
  gap:24px;
  padding:34px;
  align-items:center;
}
h1{
  margin:12px 0 14px;
  font-size:clamp(2rem,5vw,4.25rem);
  line-height:1.02;
  letter-spacing:-.04em;
}
.lead{
  font-size:1.08rem;
  color:#cbd5e1;
  margin:0 0 22px;
  max-width:62ch;
}
.pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  border:1px solid rgba(34,197,94,.22);
  background:rgba(34,197,94,.1);
  color:#bbf7d0;
  padding:7px 12px;
  border-radius:999px;
  font-size:.86rem;
  font-weight:800;
}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{
  min-height:52px;
  padding:14px 20px;
  border-radius:16px;
  font-weight:900;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  border:1px solid transparent;
}
.primary{
  background:linear-gradient(135deg,var(--accent),#16a34a);
  color:#04120a;
}
.secondary{
  background:rgba(255,255,255,.03);
  border-color:var(--line);
}
.grid{
  margin-top:22px;
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:18px;
}
.card{
  background:rgba(16,26,45,.96);
  border:1px solid var(--line);
  border-radius:24px;
  padding:22px;
  box-shadow:0 12px 36px rgba(0,0,0,.16);
}
.card p,.card li{color:var(--muted)}
.card ul{margin:0;padding-left:18px}
.steps{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:18px;
  margin-top:18px;
}
.step-num{
  width:36px;
  height:36px;
  border-radius:12px;
  display:grid;
  place-items:center;
  background:rgba(56,189,248,.12);
  color:#bae6fd;
  font-weight:900;
  margin-bottom:10px;
  border:1px solid rgba(56,189,248,.18);
}
.faq details,.alt-item{
  background:rgba(255,255,255,.03);
  border:1px solid var(--line);
  border-radius:16px;
  padding:14px 16px;
  margin-top:12px;
}
.faq summary{
  cursor:pointer;
  font-weight:800;
  color:#fff;
}
.faq p{margin:10px 0 0}
.disclosure{
  margin-top:18px;
  padding:18px 20px;
  border-radius:20px;
  background:rgba(248,113,113,.08);
  border:1px solid rgba(248,113,113,.18);
  color:#fecaca;
  font-size:.95rem;
}
.footer{
  padding:22px 4px 8px;
  color:var(--muted);
  font-size:.9rem;
  text-align:center;
}
.sticky{
  position:fixed;
  left:0;
  right:0;
  bottom:0;
  background:rgba(7,17,31,.9);
  backdrop-filter:blur(14px);
  border-top:1px solid rgba(35,49,74,.9);
  padding:12px 16px;
}
.sticky .inner{
  max-width:var(--max);
  margin:0 auto;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:12px;
  flex-wrap:wrap;
}
.mini{
  padding:12px 16px;
  border-radius:14px;
  background:linear-gradient(135deg,var(--accent),#16a34a);
  color:#04120a;
  font-weight:900;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-height:46px;
}
.meta-row{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:12px;
  margin-top:14px;
}
.meta{
  padding:14px;
  border-radius:18px;
  border:1px solid var(--line);
  background:rgba(255,255,255,.03);
  color:#cbd5e1;
  font-size:.95rem;
}
@media (max-width:900px){
  .hero-inner,.grid,.steps,.meta-row{grid-template-columns:1fr}
  .hero-inner{padding:20px}
}
@media (max-width:640px){
  .wrap{padding:14px}
  h1{font-size:clamp(1.9rem,11vw,3rem)}
  .btns{display:grid;grid-template-columns:1fr}
  .btn,.mini{width:100%}
  .sticky .inner{flex-direction:column;align-items:stretch}
}
"""

def abs_url(slug: str) -> str:
    return f"{BASE_URL}/" if slug == "" else f"{BASE_URL}/{slug}/"

def nav_html():
    return "".join(
        f'<a href="{abs_url(item["slug"])[len(BASE_URL):]}">{escape(item["label"])}</a>'
        for item in NAV
    )

def faq_schema():
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]}
            } for item in FAQ_ITEMS
        ]
    }

def render_faq():
    blocks = [
        f"<details><summary>{escape(item['question'])}</summary><p>{escape(item['answer'])}</p></details>"
        for item in FAQ_ITEMS
    ]
    return f'<section class="card faq" id="faq"><h2>Frequently Asked Questions</h2>{"".join(blocks)}</section>'

def render_alternatives():
    blocks = [
        f'<div class="alt-item"><strong>{escape(item["name"])}</strong><p>{escape(item["summary"])}</p></div>'
        for item in ALT_ITEMS
    ]
    return f'<section class="card" id="details"><h2>Mondly Alternatives</h2>{"".join(blocks)}</section>'

def render_page_body(page):
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
        <section class="steps" id="how" aria-label="How it works">
          <article class="card"><div class="step-num">1</div><h3>Choose your language</h3><p>Pick the language you want to learn and start with a manageable daily routine.</p></article>
          <article class="card"><div class="step-num">2</div><h3>Practice speaking</h3><p>Use conversation-style exercises and voice practice to build confidence.</p></article>
          <article class="card"><div class="step-num">3</div><h3>Keep the streak going</h3><p>Short sessions make it easier to return every day and keep progress moving.</p></article>
        </section>
        {render_faq()}
        """
    if page["type"] == "review":
        return """
        <section class="grid" id="details">
          <article class="card"><h2>Quick verdict</h2><p>Mondly is a strong fit if you want short sessions, speech practice, and a simple app-based language routine.</p></article>
          <article class="card"><h2>Best for</h2><p>Beginners, casual learners, travelers, and busy adults who need a lightweight daily learning habit.</p></article>
          <article class="card"><h2>Watch out for</h2><p>As with most language apps, results depend on consistency. Short daily use matters more than occasional long sessions.</p></article>
        </section>
        """
    if page["type"] == "faq":
        return render_faq()
    if page["type"] == "alternatives":
        return render_alternatives()
    return """
    <section class="card">
      <p>This page is provided for informational and promotional purposes only.</p>
      <p>Affiliate links may generate a commission without additional cost to you.</p>
    </section>
    """

def build_page(page):
    slug = page["slug"]
    out_dir = OUT if slug == "" else OUT / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    canonical = abs_url(slug)
    schema_graph = [
        {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL, "logo": BRAND["logo"]},
        {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL},
        {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": "en-US"}
    ]
    if page["type"] in ("home", "faq"):
        schema_graph.append(faq_schema())

    html = f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
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
  <meta property="og:image" content="{abs_url('')}assets/mondly-og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(page["title"])}">
  <meta name="twitter:description" content="{escape(page["description"])}">
  <meta name="twitter:image" content="{abs_url('')}assets/mondly-og.jpg">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":schema_graph}, ensure_ascii=False)}</script>
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
          <div class="proof" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;color:#dbeafe;font-size:.92rem">
            {''.join(f'<span>{escape(t)}</span>' for t in page.get("trust", []))}
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
    {render_page_body(page)}
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
</html>
"""
    (out_dir / "index.html").write_text(html, encoding="utf-8")

for page in PAGES:
    build_page(page)

(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
sitemap = ["<?xml version='1.0' encoding='UTF-8'?>", "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
for page in PAGES:
    sitemap.append(f"  <url><loc>{abs_url(page['slug'])}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
(OUT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

(OUT / "llms.txt").write_text(
    f"""# {SITE_NAME}

{DATA["site_summary"]}

## Key pages
- [Home]({abs_url("")})
- [Review]({abs_url("review")})
- [FAQ]({abs_url("faq")})
- [Alternatives]({abs_url("alternatives")})
- [Privacy]({abs_url("privacy")})
- [Terms]({abs_url("terms")})

## Brand
- Name: {BRAND["name"]}
- Official site: {BRAND["official_url"]}

## Guidance
- This site is written for USA visitors.
- The main action is the affiliate link to Mondly.
- Use the FAQ page for concise answers.
- Use the review page for decision support.
""",
    encoding="utf-8"
)

(OUT / "404.html").write_text(f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Not Found | {SITE_NAME}</title>
  <meta name="robots" content="noindex,nofollow">
  <meta http-equiv="refresh" content="5;url={abs_url('')}">
  <style>
    body{{margin:0;font-family:Arial,sans-serif;background:#07111f;color:#e5e7eb;display:grid;place-items:center;min-height:100vh;padding:24px}}
    .box{{max-width:720px;background:#101a2d;border:1px solid #23314a;border-radius:24px;padding:32px}}
    a{{color:#38bdf8}}
    .btn{{display:inline-block;margin-top:18px;padding:12px 18px;border-radius:14px;background:#22c55e;color:#04120a;text-decoration:none;font-weight:800}}
  </style>
</head>
<body>
  <div class="box">
    <h1>Page not found</h1>
    <p>The page you requested does not exist. You will be redirected home shortly.</p>
    <a class="btn" href="{abs_url('')}">Go home</a>
  </div>
</body>
</html>""", encoding="utf-8")

(OUT / ".nojekyll").write_text("", encoding="utf-8")
print("Built subpath-safe site to output/")
