#!/usr/bin/env python3
"""Generate the Medine Mobilya district landing pages, the sitemap, the redirects
and the homepage area list — all from tools/districts.json.

    python3 tools/make-district-pages.py            # write everything
    python3 tools/make-district-pages.py --check    # verify only, change nothing

Why a generator: 40 district pages that differ only in a find-and-replace of the
district name are thin/duplicate content and Google treats them as such. Each page
here gets its own intro (the district's housing and commercial profile) and its own
"Why Medine Mobilya <district>?" paragraph built from the real neighbouring
districts, so the visible text is genuinely unique per page.

The pages already shipped by hand (status "existing") are never overwritten.
"""
import glob as glob_module
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

WA = "905386467971"
PHONE_DISPLAY = "+90 538 646 79 71"
PHONE_TEL = "+905386467971"
ADDRESS = "Mehterçeşme, Cumhuriyet Cd No:28, 34515 Esenyurt/İstanbul"
ORIGIN = "https://spotcuistanbul.com"
GTAG = "AW-609406158"

ITEMS = [
    "İkinci El Koltuk Takımı, L Koltuk ve Chester Koltuklar",
    "İkinci El Yatak Odası Takımı, Gardırop ve Bazalar",
    "İkinci El Buzdolabı, Çamaşır ve Bulaşık Makineleri",
    "İkinci El Yemek Masası ve Sandalye Takımları",
    "Ofis ve Büro Mobilyaları",
]


def data():
    with open("tools/districts.json", encoding="utf-8") as fh:
        raw = json.load(fh)
    existing = [dict(d, status="existing") for d in raw["already_shipped_examples"]]
    generated = [dict(d, status="generated") for d in raw["districts"]]
    legacy = raw.get("legacy", [])
    return existing, generated, legacy


def nearby_of(d, all_d):
    """The districts this one borders, resolved from its own adjacency sentence.

    Derived rather than stored: the sentence is the fact, the slug list is just a
    view of it, so the two can never disagree.
    """
    names = sorted((x["name"] for x in all_d), key=len, reverse=True)
    to_slug = {x["name"]: x["slug"] for x in all_d}
    found, rest = [], d.get("neighbors", "")
    for n in names:
        if n == d["name"]:
            continue
        if re.search(r"(?<![\wçğıöşüÇĞİÖŞÜ])" + re.escape(n) + r"(?![\wçğıöşüÇĞİÖŞÜ])", rest):
            found.append(to_slug[n])
            rest = rest.replace(n, "·")
    return found


def nearby_block(d, all_d):
    slugs = nearby_of(d, all_d)
    if not slugs:
        return ""
    by_slug = {x["slug"]: x["name"] for x in all_d}
    links = "\n".join(
        f'        <li><a href="/{s}" style="color: #7b4f2c; font-weight: bold;">'
        f'{by_slug[s]} İkinci El Eşya Alım Satım</a></li>'
        for s in slugs
    )
    return f"""      <h2 style="margin-top: 40px; text-align: left;">Yakın Bölgeler</h2>
      <ul style="line-height: 2; font-size: 16px; margin-left: 20px; margin-top: 15px; list-style: none;">
{links}
      </ul>

"""


def page_html(d, all_d):
    name, slug = d["name"], d["slug"]
    title = f"{name} İkinci El Eşya Alım Satım — Medine Mobilya"
    desc = (
        f"{name} ikinci el eşya alanlar — Medine Mobilya. {d['profile']} "
        "Aynı gün adresinizden nakit alım; WhatsApp ile 5 dakikada fiyat teklifi."
    )
    keywords = (
        f"{name} ikinci el eşya alanlar, {name} spotçu, {name} mobilya alım satım, "
        f"{name} beyaz eşya alan yerler, Medine Mobilya"
    )
    # The district name goes into a URL query: percent-encode it, otherwise names
    # with Turkish characters (Bağcılar, Çekmeköy) land raw in the href.
    wa_text = f"Merhaba,%20{quote(name)}%20b%C3%B6lgesinde%20ikinci%20el%20e%C5%9Fya%20satmak%20istiyorum"
    items = "\n".join(f"        <li>{i}</li>" for i in ITEMS)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <!-- Google tag (gtag.js) for Google Ads Conversion Tracking -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GTAG}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GTAG}');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">

  <link rel="canonical" href="{ORIGIN}/{slug}">
  <link rel="stylesheet" href="/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="logo">
      <a href="/" style="text-decoration: none; color: inherit;">MEDİNE MOBİLYA</a>
      <span class="logo-sub">Medine Mobilya — {name} İkinci El Eşya Alım Satım</span>
    </div>

    <nav class="nav-links" aria-label="Ana Menü">
      <a href="/">Ana Sayfa</a>
      <a href="/#about">Hakkımızda</a>
      <a href="/#features">Hizmetlerimiz</a>
      <a href="https://wa.me/{WA}?text={wa_text}" class="nav-cta" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp Teklif</a>
    </nav>
  </header>

  <main style="padding-top: 100px; max-width: 900px; margin: auto; padding-left: 20px; padding-right: 20px;">
    <section class="about" style="margin-top: 20px;">
      <h1>{name} İkinci El Eşya Alanlar — Medine Mobilya</h1>
      <p style="font-size: 18px; line-height: 1.8; color: #444; margin-top: 15px;">
        <strong>Medine Mobilya</strong> olarak <strong>{name}</strong> bölgesinde ikinci el mobilya, beyaz eşya, koltuk takımı, yatak odası takımı ve televizyon gibi tüm ev eşyalarınızı adresinizden nakit ödeme ile satın alıyoruz. {d['profile']}
      </p>

      <div style="background: #f1e7dc; padding: 25px; border-radius: 12px; margin-top: 25px; text-align: center;">
        <h3 style="color: #5a3921; font-size: 22px;">{name} Bölgesinde 5 Dakikada Fiyat Teklifi Alın</h3>
        <p style="margin-top: 10px; font-size: 16px;">Eşyalarınızın fotoğrafını WhatsApp ile gönderin, anında fiyat teklifi sunalım.</p>
        <a href="https://wa.me/{WA}?text={wa_text}" target="_blank" class="hero-btn" style="margin-top: 15px; display: inline-block;">
          <i class="fab fa-whatsapp"></i> WhatsApp ile Fiyat Al
        </a>
        <a href="tel:{PHONE_TEL}" class="hero-btn" style="margin-top: 15px; display: inline-block; margin-left: 10px;">
          <i class="fas fa-phone"></i> Hemen Ara
        </a>
      </div>

      <h2 style="margin-top: 40px; text-align: left;">{name} Bölgesinde Satın Aldığımız Eşyalar</h2>
      <ul style="line-height: 2; font-size: 16px; margin-left: 20px; color: #333; margin-top: 15px;">
{items}
      </ul>

      <h2 style="margin-top: 40px; text-align: left;">Neden Medine Mobilya {name}?</h2>
      <p style="font-size: 16px; line-height: 1.8; color: #444; margin-top: 10px;">
        Kendi nakliye araçlarımızla aynı gün adresinize geliyoruz. {d['neighbors']} Ödemeyi eşyalarınız aracımıza yüklenmeden önce nakit veya banka havalesi ile kapıda yapıyoruz.
      </p>

{nearby_block(d, all_d)}
      <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="font-weight: bold; color: #5a3921;">
          <i class="fas fa-map-marker-alt"></i> Merkez Mağaza Adresimiz: {ADDRESS}
        </p>
        <p style="margin-top: 8px;">
          <a href="/" style="color: #7b4f2c; font-weight: bold; text-decoration: underline;">← Ana Sayfaya Dön</a>
        </p>
      </div>
    </section>
  </main>

  <footer>
    <p><strong>MEDİNE MOBİLYA</strong> — {name} İkinci El Eşya Alım Satım</p>
    <p>© 2026 Medine Mobilya | Tel: <a href="tel:{PHONE_TEL}" style="color: inherit; text-decoration: underline;">{PHONE_DISPLAY}</a> | WhatsApp: 05386467971</p>
  </footer>

  <!-- lead tracking: WhatsApp/call conversion events + gclid/utm attribution -->
  <script src="/tracking.js" defer></script>

</body>
</html>
"""


def last_commit_date():
    """The date a crawler should compare: the last commit that touched the site.

    A hardcoded or build-time date would claim a change on every run and Google
    ignores a lastmod that does not match the real content.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", "."],
            capture_output=True, text=True, check=True, cwd=ROOT,
        ).stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", out):
            return out
    except Exception:
        pass
    return __import__("datetime").date.today().isoformat()


def sitemap(all_d):
    stamp = last_commit_date()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url>",
        f"    <loc>{ORIGIN}/</loc>",
        f"    <lastmod>{stamp}</lastmod>",
        "    <changefreq>weekly</changefreq>",
        "    <priority>1.0</priority>",
        "  </url>",
    ]
    for d in all_d:
        lines += [
            "  <url>",
            f"    <loc>{ORIGIN}/{d['slug']}</loc>",
            f"    <lastmod>{stamp}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            "    <priority>0.8</priority>",
            "  </url>",
        ]
    lines += ["</urlset>", ""]
    return "\n".join(lines)


def redirects(all_d, legacy):
    out = [
        "# Netlify redirects — Medine Mobilya (spotcuistanbul.com)",
        "#",
        "# 1) The .html copy of every district page 301s to the clean URL that the",
        "#    canonical tag and sitemap.xml both declare (/x), so Google consolidates",
        "#    the duplicate instead of choosing one, and old links keep working.",
        "# 2) /index.html 301s to / so the homepage has a single address.",
        "# 3) URLs that were live before the May-2026 file rename (avcilar.html,",
        "#    basaksehir.html, Buyukcekmece.html, …) 301 to the district that answers the",
        "#    same intent. Search Console listed them as \"Not found (404)\" and kept",
        "#    re-crawling them. Both the bare path Netlify's pretty URLs used to serve",
        "#    and the .html path are covered.",
        "# 4) The catch-all rewrite to /index.html (200) that used to be here was",
        "#    removed: it answered EVERY unknown URL with the homepage and HTTP 200,",
        "#    which is a soft 404 — Google can index it and it hides real 404s.",
        "#    Unmatched paths now fall through to /404.html with a real 404 status.",
        "#",
        '#    The trailing "!" is required: Netlify serves an existing static file in',
        "#    preference to a redirect rule (shadowing), so without it the .html copies",
        "#    keep returning 200 and the rule is ignored.",
        "",
    ]
    known = {d["slug"] for d in all_d}
    for d in all_d:
        out.append(f"/{d['slug']}.html    /{d['slug']}    301!")
    out.append("/index.html    /    301!")

    if legacy:
        out.append("")
        out.append("# Pre-rename URLs (see note 3)")
        for l in legacy:
            if l["to"] not in known:
                # a typo here would aim an old inbound link at a 404
                raise SystemExit(f"legacy target {l['to']} is not a known district")
            out.append(f"/{l['from']}    /{l['to']}    301!")
            out.append(f"/{l['from']}.html    /{l['to']}    301!")
    out.append("")
    return "\n".join(out)


def home_areas(all_d):
    rows = "\n".join(
        f'        <div class="area-item"><a href="/{d["slug"]}">{d["name"]} İkinci El Eşya Alım Satım</a></div>'
        for d in all_d
    )
    return f'      <div class="area-list">\n{rows}\n      </div>'


def inject_nearby_into_existing(all_d):
    """The 8 hand-written pages predate the generator, so the nearby-districts block
    is inserted into them here (idempotently) to keep internal linking uniform."""
    by_slug = {d["slug"]: d for d in all_d}
    anchor = '      <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">'
    touched = 0
    for d in all_d:
        if d.get("status") != "existing":
            continue
        for path in (f"{d['slug']}.html", os.path.join(d["slug"], "index.html")):
            if not os.path.exists(path):
                continue
            body = open(path, encoding="utf-8").read()
            if "Yakın Bölgeler" in body or anchor not in body:
                continue
            block = nearby_block(by_slug[d["slug"]], all_d)
            open(path, "w", encoding="utf-8").write(body.replace(anchor, block + anchor, 1))
            touched += 1
    return touched


def inject_tracking(tag='  <script src="/tracking.js" defer></script>'):
    """Every page must load the lead-tracking script. Generated pages get it from the
    template; the hand-written ones and 404.html are patched here, idempotently."""
    touched = []
    for path in sorted(glob_module.glob("*.html")) + sorted(glob_module.glob("*/index.html")):
        if path.startswith("tools/"):
            continue
        body = open(path, encoding="utf-8").read()
        if "tracking.js" in body or "</body>" not in body:
            continue
        open(path, "w", encoding="utf-8").write(body.replace("</body>", tag + "\n</body>", 1))
        touched.append(path)
    return touched


def add_call_links():
    """A lead-generation site with no tappable phone number throws away calls — and
    the call_click conversion in tracking.js can never fire. Every page gets a "Hemen
    Ara" button beside its WhatsApp button plus a tel: link in the footer, idempotently.
    """
    call_btn = (
        '<a href="tel:{tel}" class="hero-btn" '
        'style="margin-top: 15px; display: inline-block; margin-left: 10px;">'
        '<i class="fas fa-phone"></i> Hemen Ara</a>'
    ).format(tel=PHONE_TEL)
    plain = f"Tel: {PHONE_DISPLAY}"
    linked = f'Tel: <a href="tel:{PHONE_TEL}" style="color: inherit; text-decoration: underline;">{PHONE_DISPLAY}</a>'
    touched = []

    for path in sorted(glob_module.glob("*.html")) + sorted(glob_module.glob("*/index.html")):
        if path.startswith("tools/"):
            continue
        body = open(path, encoding="utf-8").read()
        new = body

        # 1) beside the WhatsApp CTA in the price-quote box / hero
        if 'class="hero-btn"' in new and 'tel:' not in new:
            new = re.sub(
                r'(<a\s+href="https://wa\.me/[^"]*"[^>]*class="hero-btn"[^>]*>.*?</a>)',
                lambda m: m.group(1) + "\n        " + call_btn,
                new, count=1, flags=re.S,
            )

        # 2) the footer phone number becomes tappable
        if plain in new:
            new = new.replace(plain, linked, 1)
        elif 'tel:' not in new:
            new = new.replace("</footer>", f"  <p>{linked}</p>\n  </footer>", 1)

        if new != body:
            open(path, "w", encoding="utf-8").write(new)
            touched.append(path)
    return touched


def main():
    check = "--check" in sys.argv
    existing, generated, legacy = data()
    all_d = sorted(existing + generated, key=lambda d: d["name"])
    rule_count = len(all_d) + 1 + 2 * len(legacy)

    if check:
        problems = []
        for d in generated:
            for p in (f"{d['slug']}.html", os.path.join(d["slug"], "index.html")):
                if not os.path.exists(p):
                    problems.append(f"missing page: {p}")
                else:
                    body = open(p, encoding="utf-8").read()
                    if f"{ORIGIN}/{d['slug']}" not in body:
                        problems.append(f"wrong canonical in {p}")
        if open("sitemap.xml", encoding="utf-8").read().count("<loc>") != len(all_d) + 1:
            problems.append("sitemap URL count does not match the district list")
        if open("_redirects", encoding="utf-8").read().count("301!") != rule_count:
            problems.append("redirect rule count does not match the district/legacy list")
        home = open("index.html", encoding="utf-8").read()
        if home.count('class="area-item"') != len(all_d):
            problems.append("homepage area list out of sync")
        for d in all_d:
            body = open(f"{d['slug']}.html", encoding="utf-8").read()
            if "Yakın Bölgeler" not in body:
                problems.append(f"missing nearby block: {d['slug']}")
        print("\n".join(problems) if problems else f"check ok: {len(all_d)} districts, all files in sync")
        return 1 if problems else 0

    written = 0
    for d in generated:
        html = page_html(d, all_d)
        for p in (f"{d['slug']}.html", os.path.join(d["slug"], "index.html")):
            os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
            open(p, "w", encoding="utf-8").write(html)
            written += 1
        print(f"  + {d['name']:16} -> {d['slug']}.html + /{d['slug']}/index.html")

    open("sitemap.xml", "w", encoding="utf-8").write(sitemap(all_d))
    open("_redirects", "w", encoding="utf-8").write(redirects(all_d, legacy))

    home = open("index.html", encoding="utf-8").read()
    new_home, n = re.subn(r'      <div class="area-list">.*?\n      </div>', home_areas(all_d), home, flags=re.S)
    if n != 1:
        raise SystemExit(f"could not update the homepage area list (matched {n} times)")
    open("index.html", "w", encoding="utf-8").write(new_home)

    subprocess.run([sys.executable, "tools/make-404.py"], check=True)
    print(f"nearby block added to {inject_nearby_into_existing(all_d)} hand-written page copy(ies)")
    print(f"call links added to {len(add_call_links())} page(s)")
    touched = inject_tracking()
    if touched:
        print(f"tracking script added to {len(touched)} page(s)")
    missing = [f for f in sorted(glob_module.glob("*.html")) + sorted(glob_module.glob("*/index.html"))
               if "tracking.js" not in open(f, encoding="utf-8").read()]
    if missing:
        raise SystemExit(f"pages without the tracking script: {missing}")
    print(f"\n{written} page(s) written, sitemap {len(all_d) + 1} URLs, {rule_count} redirect rules "
          f"({len(all_d) + 1} district + {2 * len(legacy)} pre-rename), homepage list updated")


if __name__ == "__main__":
    sys.exit(main() or 0)
