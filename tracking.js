/* Medine Mobilya — lead tracking
 * ================================
 * The site already carried the Google Ads base tag (AW-609406158) but fired NO
 * conversion event: Ads could see clicks and nothing else, so Smart Bidding had
 * nothing to optimise towards and no campaign could be judged profitable or not.
 *
 * This file adds three things, all of them dependency-free:
 *
 *   1. Attribution capture — gclid/wbraid/gbraid and utm_* from the landing URL are
 *      kept (first touch wins, 90 days) and appended to every WhatsApp deep link as
 *      a short "Ref:" line, so the message that arrives in WhatsApp says which ad,
 *      keyword or district page produced it. This is what closes the loop when you
 *      have no CRM.
 *   2. Conversion events — whatsapp_click and call_click are the real conversions for
 *      this business (nobody fills in forms to sell a sofa); engaged is a soft signal
 *      used for remarketing audiences.
 *   3. Safety — every call is guarded, nothing blocks the click, and if the page is
 *      opened from file:// the script does nothing.
 *
 * CONVERSION LABELS ARE SET (13 Oct 2026) — Google Ads action "Contact" (Website),
 * label 5JK6CPmqn6ocEM6Zy6IC. Both whatsapp_click and call_click fire that ONE
 * action on purpose, so Smart Bidding optimises towards "any contact", which is
 * the real business goal. To split channels later, create a second Website action
 * in Google Ads (Goals > Conversions) and paste its label into the matching slot.
 * `engaged` stays empty — it is a reach signal for remarketing, not a lead.
 */
(function () {
  "use strict";

  // ---- configuration -------------------------------------------------------
  var AW_ID = "AW-609406158"; // the Ads tag already present in every page
  // GA4 is installed as a second gtag destination in the <head> of every page.
  // Never call gtag("config", GA4) here too — a second config counts a second page_view.
  var GA4_ID = "";
  var STORE_KEY = "medine_attr";
  var STORE_DAYS = 90;

  // Ads conversion labels, format "AW-609406158/AbC-D_efGh".
  // Taken from Google Ads > Goals > Conversions > Contacts > Contact > Tag setup.
  // One action serves BOTH lead channels for now: Smart Bidding then optimises
  // for "any contact" (WhatsApp click OR phone tap), which is the real business
  // goal. Split into two actions later if per-channel reporting is wanted.
  var CONV = {
    whatsapp_click: "AW-609406158/5JK6CPmqn6ocEM6Zy6IC", // Contact (Website)
    call_click: "AW-609406158/5JK6CPmqn6ocEM6Zy6IC", //     Contact (Website) — same action on purpose
    engaged: "" //         leave empty unless you want a soft conversion action
  };

  var PARAMS = ["gclid", "wbraid", "gbraid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];

  function isFile() {
    return location.protocol !== "http:" && location.protocol !== "https:";
  }

  // ---- 1. attribution capture ---------------------------------------------
  function readStored() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (!raw) return null;
      var d = JSON.parse(raw);
      if (!d || !d.t) return null;
      if (Date.now() - d.t > STORE_DAYS * 864e5) return null;
      return d.v;
    } catch (e) {
      return null;
    }
  }

  function writeStored(v) {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({ t: Date.now(), v: v }));
    } catch (e) {
      /* private mode — attribution is a nicety, not a requirement */
    }
  }

  function fromQuery() {
    var q = new URLSearchParams(location.search);
    var out = {};
    for (var i = 0; i < PARAMS.length; i++) {
      var val = q.get(PARAMS[i]);
      if (val) out[PARAMS[i]] = String(val).slice(0, 120);
    }
    return Object.keys(out).length ? out : null;
  }

  var stored = readStored();
  var fresh = fromQuery();
  // First touch wins: a later internal pageview must not overwrite the ad that
  // actually brought the visitor in.
  var attr = stored || fresh || null;
  if (fresh && !stored) writeStored(fresh);

  function refLine() {
    if (!attr) return "";
    var bits = [];
    if (attr.utm_source) bits.push(attr.utm_source);
    if (attr.utm_medium) bits.push(attr.utm_medium);
    if (attr.utm_campaign) bits.push(attr.utm_campaign);
    if (attr.utm_term) bits.push(attr.utm_term);
    var click = attr.gclid || attr.wbraid || attr.gbraid;
    if (click) bits.push("gclid:" + click.slice(0, 24));
    if (!bits.length) return "";
    return "\n(Ref: " + bits.join(" / ") + ")";
  }

  // ---- 2. events -----------------------------------------------------------
  function send(name, params) {
    if (typeof window.gtag !== "function") return;
    try {
      var payload = params || {};
      payload.event_category = "lead";
      window.gtag("event", name, payload);
      if (CONV[name]) window.gtag("event", "conversion", { send_to: CONV[name] });
    } catch (e) {
      /* never let tracking break the page */
    }
  }

  function decorateWhatsAppLinks() {
    var ref = refLine();
    if (!ref) return;
    var links = document.querySelectorAll('a[href*="wa.me/"]');
    for (var i = 0; i < links.length; i++) {
      try {
        var url = new URL(links[i].href);
        var text = url.searchParams.get("text") || "Merhaba, ikinci el eşya satmak istiyorum";
        if (text.indexOf("(Ref:") === -1) {
          url.searchParams.set("text", text + ref);
          links[i].href = url.toString();
        }
      } catch (e) {
        /* malformed link — leave it alone */
      }
    }
  }

  function onClick(ev) {
    var el = ev.target;
    while (el && el !== document) {
      if (el.tagName === "A") {
        var href = el.getAttribute("href") || "";
        if (href.indexOf("wa.me/") !== -1) {
          send("whatsapp_click", {
            link_text: (el.textContent || "").trim().slice(0, 60),
            page: location.pathname,
            campaign: attr ? attr.utm_campaign || "" : ""
          });
        } else if (href.indexOf("tel:") === 0) {
          send("call_click", { page: location.pathname, phone: href.slice(4) });
        }
        return;
      }
      el = el.parentNode;
    }
  }

  function watchEngagement() {
    var sent = false;
    var started = Date.now();
    function maybe() {
      if (sent) return;
      var doc = document.documentElement;
      var scrolled = (window.pageYOffset + window.innerHeight) / Math.max(doc.scrollHeight, 1);
      if (Date.now() - started > 45000 && scrolled > 0.5) {
        sent = true;
        send("engaged", { seconds: Math.round((Date.now() - started) / 1000), page: location.pathname });
        window.removeEventListener("scroll", maybe);
      }
    }
    window.addEventListener("scroll", maybe, { passive: true });
    setTimeout(maybe, 45000);
  }

  // ---- 3. boot -------------------------------------------------------------
  function boot() {
    if (isFile()) return;
    // GA4 is configured by the page <head> snippet — configuring it again here
    // would send a duplicate page_view to GA4.
    decorateWhatsAppLinks();
    document.addEventListener("click", onClick, true);
    watchEngagement();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  // exposed for debugging from the console: medineAttr()
  window.medineAttr = function () {
    return attr;
  };
})();
