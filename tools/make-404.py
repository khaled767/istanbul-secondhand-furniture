#!/usr/bin/env python3
"""Generate 404.html for the Medine Mobilya site (served by Netlify for every
unmatched path, with a real 404 status).

The district list comes from tools/districts.json, so adding a district page and
regenerating (tools/make-district-pages.py does both) keeps this page in sync.

Run from the project root:  python3 tools/make-404.py
"""
import json
import os

with open("tools/districts.json", encoding="utf-8") as fh:
    _raw = json.load(fh)
DISTRICTS = [
    (d["slug"], d["name"]) for d in sorted(_raw["already_shipped_examples"] + _raw["districts"], key=lambda d: d["name"])
]

WA = "905386467971"
PHONE_DISPLAY = "+90 538 646 79 71"
ADDRESS = "Mehterçeşme, Cumhuriyet Cd No:28, 34515 Esenyurt/İstanbul"

links = "\n".join(
    f'          <a href="/{slug}" style="color: #7b4f2c; font-weight: bold;">'
    f"{name} İkinci El Eşya Alım Satım</a>"
    for slug, name in DISTRICTS
)

html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <!-- Google tag (gtag.js) for Google Ads Conversion Tracking -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=AW-609406158"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'AW-609406158');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>Sayfa Bulunamadı (404) — Medine Mobilya</title>
  <meta name="robots" content="noindex, follow">
  <!-- A 404 must never be indexed: the page exists to route visitors back, not to
       rank. Asset paths are absolute so they resolve from any URL depth. -->
  <link rel="stylesheet" href="/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>

  <!-- NAVBAR -->
  <header class="navbar">
    <div class="logo">
      <a href="/" style="text-decoration: none; color: inherit;">MEDİNE MOBİLYA</a>
      <span class="logo-sub">Medine Mobilya — İstanbul İkinci El Eşya Alım Satım</span>
    </div>

    <nav class="nav-links" aria-label="Ana Menü">
      <a href="/">Ana Sayfa</a>
      <a href="/#about">Hakkımızda</a>
      <a href="/#features">Hizmetlerimiz</a>
      <a href="https://wa.me/{WA}?text=Merhaba,%20ikinci%20el%20e%C5%9Fya%20satmak%20istiyorum" class="nav-cta" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp Teklif</a>
    </nav>
  </header>

  <main style="padding-top: 120px; max-width: 900px; margin: auto; padding-left: 20px; padding-right: 20px; text-align: center;">
    <p style="font-size: 64px; font-weight: bold; color: #5a3921; margin: 0;">404</p>
    <h1 style="margin-top: 10px;">Aradığınız Sayfa Bulunamadı</h1>
    <p style="font-size: 18px; line-height: 1.8; color: #444; margin-top: 15px;">
      Bu adres taşınmış veya hiç var olmamış olabilir. Aşağıdan bölgenizi seçebilir ya da
      doğrudan bize ulaşabilirsiniz — ikinci el eşyalarınız için hemen fiyat teklifi alın.
    </p>

    <div style="background: #f1e7dc; padding: 25px; border-radius: 12px; margin-top: 30px; text-align: center;">
      <h3 style="color: #5a3921; font-size: 22px;">5 Dakikada Fiyat Teklifi Alın</h3>
      <p style="margin-top: 10px; font-size: 16px;">Eşyalarınızın fotoğrafını WhatsApp ile gönderin, anında teklif sunalım.</p>
      <a href="https://wa.me/{WA}?text=Merhaba,%20ikinci%20el%20e%C5%9Fya%20satmak%20istiyorum" target="_blank" class="hero-btn" style="margin-top: 15px; display: inline-block;">
        <i class="fab fa-whatsapp"></i> WhatsApp ile Fiyat Al
      </a>
      <p style="margin-top: 15px;"><a href="tel:{PHONE_DISPLAY.replace(' ', '')}" style="color: #7b4f2c; font-weight: bold;"><i class="fas fa-phone"></i> {PHONE_DISPLAY}</a></p>
    </div>

    <h2 style="margin-top: 45px; text-align: left;">Hizmet Verdiğimiz Bölgeler</h2>
    <ul style="line-height: 2.2; font-size: 16px; margin-left: 20px; margin-top: 15px; text-align: left; list-style: none;">
{links}
    </ul>

    <p style="margin-top: 30px;">
      <a href="/" class="hero-btn" style="display: inline-block;">← Ana Sayfaya Dön</a>
    </p>

    <div style="margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px;">
      <p style="font-weight: bold; color: #5a3921;">
        <i class="fas fa-map-marker-alt"></i> Merkez Mağaza Adresimiz: {ADDRESS}
      </p>
    </div>
  </main>

  <footer>
    <p><strong>MEDİNE MOBİLYA</strong> — İstanbul İkinci El Eşya Alım Satım</p>
    <p>© 2026 Medine Mobilya | Tel: {PHONE_DISPLAY} | WhatsApp: 05386467971</p>
  </footer>

</body>
</html>
"""

with open("404.html", "w", encoding="utf-8") as fh:
    fh.write(html)

print(f"wrote 404.html ({len(html)} bytes, {len(DISTRICTS)} bölge bağlantısı)")
