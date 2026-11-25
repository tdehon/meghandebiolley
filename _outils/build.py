#!/usr/bin/env python3
"""Generates every HTML page of the site (FR + EN) from the content below.

Usage, from the repository root:
    python3 _outils/build.py

Edit prices, texts or reviews in this file, run it, then commit the
regenerated .html files. Any change made by hand directly in an .html
file is overwritten the next time this script runs.
"""
import json
import re
import os
import sys
from html import escape
from urllib.parse import quote

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CALENDLY = "https://calendly.com/meghandebiolley"
EMAIL = "meghandebly@gmail.com"
PHONE_DISPLAY = "+32 491 36 80 36"
PHONE_TEL = "+32491368036"
WHATSAPP = "https://wa.me/32491368036"
INSTAGRAM = "https://www.instagram.com/meghandebiolley/"
LINKEDIN = "https://www.linkedin.com/in/meghan-de-biolley/"
ADDRESS_1 = "Avenue Hamoir 32"          # legal notice only
ADDRESS_STREET = "Avenue Hamoir"          # public pages: no house number
ADDRESS_2 = "1180 Uccle, Bruxelles"
MAPS = "https://www.google.com/maps/search/?api=1&query=Avenue%20Hamoir%2C%201180%20Uccle"
SITE = "https://meghandebiolley.com"
PODCAST = "https://open.spotify.com/episode/2sFDcMZM7nunfuoGwr982U"

FILES = {
    "fr": {"home": "index.html", "soins": "soins.html", "ateliers": "ateliers.html",
           "about": "a-propos.html", "contact": "contact.html", "legal": "mentions-legales.html",
           "gifts": "bons-cadeaux.html", "quiz": "quel-soin.html"},
    "en": {"home": "index.html", "soins": "treatments.html", "ateliers": "workshops.html",
           "about": "about.html", "contact": "contact.html", "legal": "legal-notice.html",
           "gifts": "gift-vouchers.html", "quiz": "which-treatment.html"},
}

T = {
    "fr": {
        "skip": "Aller au contenu", "menu": "Ouvrir le menu", "nav_label": "Navigation principale",
        "nav": [("soins", "Les soins"), ("ateliers", "EVJF, ateliers & entreprises"), ("gifts", "Bons cadeaux"), ("about", "À propos"), ("contact", "Contact")],
        "book": "Réserver", "tagline": "Massages & soins · Uccle",
        "footer_text": "Massages, soins du visage et sound healing à Uccle, sur rendez-vous.",
        "explore": "Explorer", "contact_h": "Me contacter", "legal": "Mentions légales",
        "book_online": "Réserver en ligne", "faq": "Questions fréquentes", "quiz": "Quel soin pour moi ?",
    },
    "en": {
        "skip": "Skip to content", "menu": "Open menu", "nav_label": "Main navigation",
        "nav": [("soins", "Treatments"), ("ateliers", "Bachelorette & corporate"), ("gifts", "Gift vouchers"), ("about", "About"), ("contact", "Contact")],
        "book": "Book", "tagline": "Massage & care · Uccle",
        "footer_text": "Massage, facials and sound healing in Uccle, Brussels, by appointment.",
        "explore": "Explore", "contact_h": "Get in touch", "legal": "Legal notice",
        "book_online": "Book online", "faq": "FAQ", "quiz": "Which treatment for me?",
    },
}

ICONS = {
    "ear": '<path d="M7 9a5 5 0 0 1 10 0c0 3-3 4-3 7a3 3 0 0 1-5.6 1.5M10 9a2 2 0 0 1 4 0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>',
    "leaf": '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14Zm0 0 7-7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
    "hands": '<path d="M12 20s-7-4.3-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.7-7 10-7 10Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/>',
    "pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11Z" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="12" cy="10" r="2" stroke="currentColor" stroke-width="1.5" fill="none"/>',
    "clock": '<circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M12 8v4l2.5 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>',
    "card": '<rect x="3.5" y="6" width="17" height="12" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M3.5 10h17" stroke="currentColor" stroke-width="1.5"/>',
    "calendar": '<rect x="4" y="5.5" width="16" height="14" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "phone": '<path d="M6.5 4h3l1.5 4-2 1.5a10 10 0 0 0 5.5 5.5l1.5-2 4 1.5v3a2 2 0 0 1-2 2A15 15 0 0 1 4.5 6a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="m4 7 8 6 8-6" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/>',
    "insta": '<rect x="4" y="4" width="16" height="16" rx="4.5" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="12" cy="12" r="3.5" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="16.8" cy="7.2" r="1" fill="currentColor"/>',
    "linkedin": '<rect x="4" y="4" width="16" height="16" rx="3" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M8.5 10.5v5M8.5 8v.01M12 15.5v-5m0 2.5a2.5 2.5 0 0 1 5 0v2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    "sound": '<path d="M5 15a7 7 0 0 0 14 0H5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/><path d="M9 10c0-1.5 1-1.5 1-3M14 10c0-1.5 1-1.5 1-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>',
}


def icon(name):
    return f'<span class="card-icon" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'


def photo(src, alt, placeholder, cls="", eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="photo {cls}" data-placeholder="{escape(placeholder)}">'
            f'<img src="{{IMG}}{src}" alt="{escape(alt)}" {loading}></div>')


def video(src, poster, label):
    return (f'<div class="photo photo--arch"><video src="{{IMG}}{src}" poster="{{IMG}}{poster}" '
            f'autoplay muted loop playsinline preload="metadata" aria-label="{escape(label)}"></video></div>')


def wa(message):
    """WhatsApp link that opens a chat with Meghan, message pre-filled."""
    return WHATSAPP + "?text=" + quote(message)


def contact_buttons(lang, wa_message, email_subject):
    """WhatsApp (main), Instagram and email. No phone button: for a chat,
    people can book a 15-minute call on Calendly."""
    return (
        ext(wa(wa_message), S(lang, "Envoyer un message sur WhatsApp", "Send a WhatsApp message"))
        + "\n          " + ext(INSTAGRAM, "Instagram", "button button--outline")
        + f'\n          <a class="button button--outline" href="mailto:{EMAIL}?subject={quote(email_subject)}">'
        + S(lang, "Envoyer un e-mail", "Send an email") + "</a>"
    )


def ext(url, label, cls="button"):
    return f'<a class="{cls}" href="{url}" target="_blank" rel="noopener">{label}</a>'


# --------------------------------------------------------------------------
# Treatments
# --------------------------------------------------------------------------

NOTE_NO_EXTRACTION = {
    "fr": "Ce n’est pas un soin visage esthétique traditionnel (pas d’extraction), mais un massage relaxant et sculptant.",
    "en": "This is not a traditional beauty facial (no extractions) but a relaxing, sculpting massage.",
}
NOTE_HAIR = {
    "fr": "Le massage du visage et du cuir chevelu peut légèrement huiler les cheveux&nbsp;: évitez de prévoir un événement important juste après.",
    "en": "The face and scalp massage may leave your hair slightly oily, so avoid planning anything important straight afterwards.",
}

SOINS = [
    dict(id="soin-visage", cal="soin-massage-du-visage", img="soin-visage.jpg", price="90 €", dur={"fr": "1 h", "en": "1 hr"},
         fr=dict(name="Soin signature visage", tag="Visage",
                 short="Un massage du visage relaxant et liftant, pour un vrai glow et un effet lifté.",
                 desc=["Le soin qu’il vous faut si vous souhaitez vous offrir un moment de détente absolue.",
                       "Pendant une heure, je travaille le haut du corps&nbsp;: le visage, le cuir chevelu, la nuque, le décolleté, les bras et les mains. Un massage du visage relaxant <em>et</em> liftant, qui vous apporte un magnifique glow et un effet lifté.",
                       "La séance dure une heure complète, avec en plus un moment d’accueil et d’échange pour adapter le massage à vos besoins."],
                 notes=["Pour des résultats plus visibles dans le temps&nbsp;: cure de 5 séances à tarif avantageux, sur demande.",
                        NOTE_NO_EXTRACTION["fr"], NOTE_HAIR["fr"]]),
         en=dict(name="Signature facial", tag="Face",
                 short="A relaxing, lifting facial massage for a real glow and a lifted look.",
                 desc=["The treatment for you if you’d like to treat yourself to a moment of complete relaxation.",
                       "For one hour I work on the upper body: face, scalp, neck, décolleté, arms and hands. A facial massage that is both relaxing <em>and</em> lifting, leaving you with a beautiful glow and a lifted look.",
                       "The session lasts a full hour, plus time beforehand to talk so I can adapt the massage to your needs."],
                 notes=["For longer-lasting results: a course of 5 sessions at a reduced rate, on request.",
                        NOTE_NO_EXTRACTION["en"], NOTE_HAIR["en"]])),
    dict(id="massage-drainant", cal="massage-lymphatique-1h-75", img="massage-drainant.jpg", price="90 €", dur={"fr": "1 h", "en": "1 hr"},
         fr=dict(name="Massage corps drainant", tag="Corps",
                 short="Un massage lymphatique pour stimuler la circulation et retrouver une sensation de légèreté.",
                 desc=["Le massage lymphatique est idéal pour stimuler la circulation, réduire la rétention d’eau et apporter une sensation de légèreté incomparable.",
                       "En plus de ses bienfaits détoxifiants, il aide à diminuer les gonflements et à raffermir les tissus, tout en offrant un moment de détente profonde.",
                       "Selon chaque corps, ce soin peut parfois être un peu plus sensible que les autres. Avant de commencer, nous prenons le temps d’analyser vos besoins et de définir ensemble la meilleure façon d’aborder le massage."],
                 notes=[]),
         en=dict(name="Lymphatic drainage massage", tag="Body",
                 short="A lymphatic massage to boost circulation and leave you feeling light.",
                 desc=["Lymphatic massage is ideal for stimulating circulation, reducing water retention and bringing an incomparable feeling of lightness.",
                       "Alongside its detoxifying benefits, it helps reduce swelling and firm the tissues, while offering a moment of deep relaxation.",
                       "Depending on your body, this treatment can feel a little more intense than others. Before we start, we take time to look at your needs and agree together on the best approach."],
                 notes=[])),
    dict(id="massage-relaxant", cal="massage-relaxant", img="massage-relaxant.jpg", price="90 €", dur={"fr": "1 h", "en": "1 hr"},
         fr=dict(name="Massage relaxant", tag="Corps",
                 short="Un massage complet à l’huile chaude, des pieds jusqu’au cuir chevelu.",
                 desc=["Un massage complet du corps, des pieds jusqu’au cuir chevelu, conçu pour vous détendre profondément et libérer les tensions accumulées.",
                       "Ce rituel est réalisé avec de l’huile chaude, pour une expérience encore plus enveloppante et apaisante."],
                 notes=[]),
         en=dict(name="Relaxing massage", tag="Body",
                 short="A full-body warm-oil massage, from your feet to your scalp.",
                 desc=["A full-body massage, from your feet to your scalp, designed to relax you deeply and release built-up tension.",
                       "This ritual uses warm oil for an even more enveloping and soothing experience."],
                 notes=[])),
    dict(id="corps-visage", cal="corps-visage-1h30", img="corps-visage.jpg", price="120 €", dur={"fr": "1 h 30", "en": "1 hr 30"},
         fr=dict(name="Corps + visage", tag="Rituel complet",
                 short="Un massage du corps enveloppant et un massage du visage sculptant, en un seul soin.",
                 desc=["Vous avez du mal à vous détendre&nbsp;? Votre corps accumule les tensions et votre esprit a du mal à ralentir&nbsp;? Alors, offrez-vous un massage corps + visage de 1&nbsp;h&nbsp;30.",
                       "J’associe un massage du corps relaxant et enveloppant à un massage du visage aux vertus apaisantes et sculptantes. Un soin complet qui aide à relâcher les tensions, stimuler la circulation et apporter une sensation de légèreté et de bien-être global.",
                       "La séance inclut un moment d’accueil et d’échange afin d’adapter chaque geste à vos besoins du moment."],
                 notes=[NOTE_NO_EXTRACTION["fr"], NOTE_HAIR["fr"]]),
         en=dict(name="Body + face", tag="Full ritual",
                 short="An enveloping body massage and a sculpting facial massage, in one treatment.",
                 desc=["Finding it hard to relax? Is your body holding on to tension while your mind struggles to slow down? Then treat yourself to a 90-minute body + face massage.",
                       "I combine a relaxing, enveloping body massage with a soothing, sculpting facial massage. A complete treatment that helps release tension, boost circulation and bring a feeling of lightness and overall wellbeing.",
                       "The session includes time to talk beforehand so I can adapt every movement to what you need on the day."],
                 notes=[NOTE_NO_EXTRACTION["en"], NOTE_HAIR["en"]])),
    dict(id="duo-corps-visage", cal="duo-corps-visage", img="duo-corps-visage.jpg", price="150 €", dur={"fr": "2 h", "en": "2 hrs"},
         fr=dict(name="Duo corps + visage", tag="Rituel long",
                 short="Deux heures pour faire le vide, relâcher les tensions et révéler un glow naturel.",
                 desc=["Vous avez du mal à vous détendre&nbsp;? Il vous faut beaucoup de temps pour faire le vide et ne plus avoir mille et une pensées en tête&nbsp;? Alors, optez pour le soin corps + visage de 2&nbsp;heures.",
                       "Pendant deux heures complètes, j’associe un massage du corps relaxant et enveloppant à un massage du visage aux vertus relaxantes et sculptantes. Un soin holistique qui libère les tensions, relance la circulation et redonne éclat, fermeté et légèreté à tout votre être.",
                       "La séance inclut un moment d’accueil et d’échange afin d’adapter chaque geste à vos besoins du moment."],
                 notes=[NOTE_NO_EXTRACTION["fr"]]),
         en=dict(name="Body + face duo", tag="Long ritual",
                 short="Two hours to switch off, release tension and reveal a natural glow.",
                 desc=["Finding it hard to relax? Do you need plenty of time to clear your mind and quiet the thousand thoughts in your head? Then choose the 2-hour body + face treatment.",
                       "For two full hours I combine a relaxing, enveloping body massage with a relaxing, sculpting facial massage. A holistic treatment that releases tension, revives circulation and restores radiance, firmness and lightness to your whole being.",
                       "The session includes time to talk beforehand so I can adapt every movement to what you need on the day."],
                 notes=[NOTE_NO_EXTRACTION["en"]])),
    dict(id="visage-sonotherapie", cal="massage-du-visage-sonotherapie-130", img="visage-sonotherapie.jpg", price="140 €", dur={"fr": "1 h 30", "en": "1 hr 30"},
         fr=dict(name="Massage du visage + sonothérapie", tag="Sonothérapie",
                 short="Un massage du visage sculptant, porté par les vibrations des bols tibétains.",
                 desc=["Vous ressentez des tensions au niveau du visage, de la mâchoire ou un mental toujours en mouvement&nbsp;? Offrez-vous un véritable moment de relâchement avec ce soin visage combiné à la sonothérapie.",
                       "Je travaille le visage en profondeur à travers un massage sculptant, liftant et relaxant, en y intégrant les vibrations des bols tibétains. Les gestes lissent les traits, relâchent les tensions, notamment au niveau de la mâchoire et du front, et redonnent de l’éclat, tandis que les sons apaisent le système nerveux et calment l’esprit.",
                       "La sonothérapie permet un lâcher-prise plus rapide et amplifie les bienfaits du massage&nbsp;: un soin qui agit à la fois sur la beauté du visage et sur l’apaisement intérieur."],
                 notes=[NOTE_NO_EXTRACTION["fr"], NOTE_HAIR["fr"]]),
         en=dict(name="Facial massage + sound therapy", tag="Sound therapy",
                 short="A sculpting facial massage, carried by the vibrations of Tibetan singing bowls.",
                 desc=["Do you feel tension in your face or jaw, or a mind that never stops? Give yourself a moment of true release with this facial treatment combined with sound therapy.",
                       "I work deeply on the face with a sculpting, lifting and relaxing massage, weaving in the vibrations of Tibetan singing bowls. The movements smooth the features, release tension, especially in the jaw and forehead, and restore radiance, while the sounds soothe the nervous system and calm the mind.",
                       "Sound therapy helps you let go faster and amplifies the benefits of the massage: a treatment for both the beauty of your face and your inner calm."],
                 notes=[NOTE_NO_EXTRACTION["en"], NOTE_HAIR["en"]])),
    dict(id="corps-sonotherapie", cal="massage-du-corps-sonotherapie-130", img="corps-sonotherapie.jpg", price="140 €", dur={"fr": "1 h 30", "en": "1 hr 30"},
         fr=dict(name="Massage du corps + sonothérapie", tag="Sonothérapie",
                 short="Un voyage sensoriel où le toucher et le son se rencontrent.",
                 desc=["Vous ressentez le besoin de vous recentrer et d’apaiser votre esprit en profondeur&nbsp;? Laissez-vous envelopper par les sons et les vibrations des bols tibétains.",
                       "Pendant 1&nbsp;h&nbsp;30, j’associe un massage du corps lent, enveloppant et profondément relaxant à l’utilisation de bols tibétains. Leurs vibrations résonnent à travers le corps et aident à relâcher les tensions, calmer le système nerveux et apaiser le mental.",
                       "Un véritable voyage sensoriel, où le toucher et le son se rencontrent pour vous offrir un moment hors du temps."],
                 notes=[]),
         en=dict(name="Body massage + sound therapy", tag="Sound therapy",
                 short="A sensory journey where touch and sound meet.",
                 desc=["Feel the need to re-centre and deeply calm your mind? Let yourself be enveloped by the sounds and vibrations of Tibetan singing bowls.",
                       "For 90 minutes I combine a slow, enveloping and deeply relaxing body massage with Tibetan singing bowls. Their vibrations resonate through the body, helping release tension, calm the nervous system and quiet the mind.",
                       "A true sensory journey where touch and sound meet, for a moment outside of time."],
                 notes=[])),
]


def meta(s, lang):
    parts = []
    if s["dur"]:
        parts.append(f'<span>{s["dur"][lang]}</span>')
    parts.append(f'<span>{s["price"]}</span>')
    return f'<p class="meta">{"".join(parts)}</p>'


def soin_card(s, lang):
    d = s[lang]
    href = f'{FILES[lang]["soins"]}#{s["id"]}'
    return f'''
        <a class="soin-card" href="{href}">
          {photo(s["img"], d["name"], "Photo : images/" + s["img"] if lang == "fr" else "Photo: images/" + s["img"], "photo--arch")}
          <span class="eyebrow">{d["tag"]}</span>
          <h3>{d["name"]}</h3>
          {meta(s, lang)}
          <p>{d["short"]}</p>
        </a>'''


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def clean_urls(html):
    """Links without ".html": GitHub Pages serves /soins.html at /soins.
    index.html becomes the folder itself ("./", "../", "en/")."""
    html = re.sub(r'"index\.html(?=["#])', '"./', html)
    html = re.sub(r'/index\.html(?=["#])', '/', html)
    return re.sub(r'\.html(?=["#])', '', html)


def layout(lang, key, title, description, body, extra_head=""):
    t = T[lang]
    files = FILES[lang]
    other = "en" if lang == "fr" else "fr"
    prefix = "" if lang == "fr" else "../"
    other_href = ("en/" if lang == "fr" else "../") + FILES[other][key]
    page_href = ("" if lang == "fr" else "en/") + files[key]
    alt_fr = SITE + "/" + FILES["fr"][key].replace("index.html", "")
    alt_en = SITE + "/en/" + FILES["en"][key].replace("index.html", "")

    nav_items = "".join(
        f'<li><a href="{files[k]}"{" aria-current=\"page\"" if k == key else ""}>{label}</a></li>'
        for k, label in t["nav"])

    lang_switch = (
        f'<a href="{files[key] if lang == "fr" else other_href}" lang="fr"{" aria-current=\"true\"" if lang == "fr" else ""}>FR</a>'
        '<span aria-hidden="true">/</span>'
        f'<a href="{other_href if lang == "fr" else files[key]}" lang="en"{" aria-current=\"true\"" if lang == "en" else ""}>EN</a>')

    full_title = title if key == "home" else f"{title} | Meghan de Biolley"

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#faf6f1">
  <link rel="canonical" href="{SITE}/{page_href.replace("index.html", "")}">
  <link rel="alternate" hreflang="fr" href="{alt_fr}">
  <link rel="alternate" hreflang="en" href="{alt_en}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Meghan de Biolley">
  <meta property="og:title" content="{escape(full_title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{SITE}/images/og-image.jpg">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="{prefix}images/favicon.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="{prefix}images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/style.css">
  <script src="{prefix}js/main.js" defer></script>{extra_head}
</head>
<body>

<a class="skip-link" href="#main">{t["skip"]}</a>

<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{files["home"]}">
      <span class="monogram" aria-hidden="true">MB</span>
      <span class="brand-name">Meghan de Biolley<small>{t["tagline"]}</small></span>
    </a>

    <div class="header-tools">
      <nav class="lang-switch" aria-label="Langue / Language">{lang_switch}</nav>
      <a class="button header-book" href="{CALENDLY}" target="_blank" rel="noopener">{t["book"]}</a>
      <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="main-navigation" aria-label="{t["menu"]}">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      </button>
    </div>

    <nav class="primary-nav" id="main-navigation" data-navigation aria-label="{t["nav_label"]}">
      <ul>
        {nav_items}
        <li class="nav-lang lang-switch">{lang_switch}</li>
        <li class="nav-book"><a class="button" href="{CALENDLY}" target="_blank" rel="noopener">{t["book"]}</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="footer-brand" href="{files["home"]}">Meghan de Biolley</a>
        <p>{t["footer_text"]}</p>
        <a class="button button--ghost-light" href="{CALENDLY}" target="_blank" rel="noopener">{t["book_online"]}</a>
      </div>
      <div>
        <h2 class="footer-heading">{t["explore"]}</h2>
        <ul class="footer-links">
          {"".join(f'<li><a href="{files[k]}">{label}</a></li>' for k, label in t["nav"])}
          <li><a href="{files["quiz"]}">{t["quiz"]}</a></li>
          <li><a href="{files["contact"]}#faq">{t["faq"]}</a></li>
        </ul>
      </div>
      <div>
        <h2 class="footer-heading">{t["contact_h"]}</h2>
        <ul class="footer-links">
          <li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Meghan de Biolley · Uccle, Bruxelles</span>
      <a href="{files["legal"]}">{t["legal"]}</a>
    </div>
  </div>
</footer>

</body>
</html>
'''
    html = html.replace("{IMG}", prefix + "images/")
    html = clean_urls(html)
    out_dir = ROOT if lang == "fr" else os.path.join(ROOT, "en")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, files[key]), "w", encoding="utf-8") as f:
        f.write(html)


def S(lang, fr, en):
    return fr if lang == "fr" else en


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

# Client messages, quoted as written (from her "Vos retours" Instagram highlight).
REVIEWS = {
    "jambes": dict(text="Je voulais juste te remercier beaucoup pour hier car c’était incroyable et surtout je sens et je vois un effet sur mes jambes 😍 je suis trop contente",
                   fr="Après un massage drainant", en="After a lymphatic drainage massage"),
    "drainage-visage": dict(text="Encore un immense merci pour le drainage et le soin du visage !! J’ai vrmt adoré ! 🥰 je reviendrai c’est sûr !!",
                            fr="Après un drainage et un soin visage", en="After a drainage massage and a facial"),
    "souches": dict(text="On a commencé par une session de sound healing chez Meghan et mamma mia c’était incroyable !!! On s’est toutes les deux endormies comme des souches & on s’est réveillées ultra détendues et souriantes",
                    fr="Après une séance de sound healing", en="After a sound healing session"),
    "weekend": dict(text="J’ai oublié de t’écrire pour te remercier… tu as fait mon week-end, c’était génial et ça m’a fait un bien INCROYABLE 😍 je reviendrai asap",
                    fr="Après un massage", en="After a massage"),
    "copines": dict(text="Merci mille fois pour le sound healing la semaine passée, c’était vraiment un super moment ! Mes copines ont adoré ton accueil et ta douceur 🥰",
                    fr="Après un sound healing entre amies", en="After a sound healing session with friends"),
    "recommander": dict(text="Encore merci pour le massage d’hier, t’as super bien fait ça ;)) je vais le recommander à mes copines !!",
                        fr="Après un massage", en="After a massage"),
    "tonifiant": dict(text="Encore merci pour ce moment de bonheur hier ! C’était hyper relaxant et tonifiant ! Je ne manquerai pas de parler de toi autour de moi 😘",
                      fr="Après un soin", en="After a treatment"),
}


def reviews(keys, lang):
    items = "".join(
        f'<figure class="review"><blockquote><p>{REVIEWS[k]["text"]}</p></blockquote>'
        f'<figcaption>{REVIEWS[k][lang]}</figcaption></figure>' for k in keys)
    note = "" if lang == "fr" else '<p class="muted small">Messages from clients, left in their original French.</p>'
    return f'<div class="reviews" lang="fr">{items}</div>{note}'


def price_menu(lang, link_prefix=""):
    return "".join(
        f'<li><a href="{link_prefix}#{s["id"]}"><span class="menu-name">{s[lang]["name"]}</span>'
        f'<span class="menu-duration">{s["dur"][lang]}</span>'
        f'<span class="menu-price">{s["price"]}</span></a></li>' for s in SOINS)


def facts(lang):
    f = FILES[lang]
    return f'''<ul class="facts">
        <li><a class="text-link" href="{f["contact"]}">{S(lang, "Avenue Hamoir, Uccle", "Avenue Hamoir, Uccle")}</a></li>
        <li>{S(lang, "Parking gratuit dans la rue", "Free street parking")}</li>
        <li>{S(lang, "Toute séance annulée moins de 48 h à l’avance reste due", "Sessions cancelled less than 48 hours in advance are charged")}</li>
        <li>{S(lang, "Cash, QR code ou facture", "Cash, QR code or invoice")}</li>
      </ul>'''


# Instagram block on the homepage. Photos are images/instagram/1.jpg to 6.jpg (4:5, like Instagram)
# and profil.jpg. To refresh them, replace the files; no code change needed.
# The alt texts below describe the current photos: update them if the subject changes a lot.
INSTAGRAM_ALTS = [
    ("Massage du visage, avec le texte « Book ce moment pour toi »", "Facial massage, with the words “Book ce moment pour toi”"),
    ("Portrait de Meghan, « Meghan, 27 ans, passionnée par le bien-être »", "Portrait of Meghan, “Meghan, 27 ans, passionnée par le bien-être”"),
    ("Coucher de soleil sur une plage, traces de pas dans le sable", "Sunset over a beach, footprints in the sand"),
    ("Meghan avec son matériel d’atelier skincare, « October & november so far »", "Meghan carrying her skincare workshop kit, “October & november so far”"),
    ("Mains posées sur le haut du buste pendant un massage", "Hands resting on the upper chest during a massage"),
    ("Table préparée pour un atelier skincare, avec une note sur les mantras", "Table set for a skincare workshop, with a note about mantras"),
]


def instagram_block(lang):
    tiles = "".join(
        f'\n        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">'
        f'<img src="{{IMG}}instagram/{i}.jpg" alt="{escape(S(lang, fr, en))}" loading="lazy" width="320" height="400"></a></li>'
        for i, (fr, en) in enumerate(INSTAGRAM_ALTS, 1))
    return f'''<section class="section section--tight insta">
    <div class="container">
      <div class="insta-head">
        <a class="insta-profile" href="{INSTAGRAM}" target="_blank" rel="noopener">
          <img src="{{IMG}}instagram/profil.jpg" alt="" width="64" height="64" loading="lazy">
          <span><strong>@meghandebiolley</strong><span class="muted small">{S(lang, "Suivez-moi sur Instagram", "Follow me on Instagram")}</span></span>
        </a>
        {ext(INSTAGRAM, S(lang, "Suivre", "Follow"), "button button--outline")}
      </div>
      <ul class="insta-grid">{tiles}
      </ul>
    </div>
  </section>'''


def page_home(lang):
    f = FILES[lang]
    P = lambda name: S(lang, "Photo : images/", "Photo: images/") + name
    body = f'''
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <p class="tagline">Disconnect to connect</p>
        <h1>{S(lang, "Massages et soins du visage à Uccle", "Massage and facials in Uccle, Brussels")}</h1>
        <p class="lead">{S(lang,
            "Je m’appelle Meghan. Depuis trois ans, je vous reçois chez moi pour des massages du corps, des soins du visage et du sound healing. Prenez un moment pour vous ✨",
            "I’m Meghan. For three years I’ve been welcoming people at home for body massage, facials and sound healing. Take a moment for yourself ✨")}</p>
        <div class="button-group">
          {ext(CALENDLY, S(lang, "Réserver", "Book a session"))}
          <a class="button button--outline" href="{f["soins"]}">{S(lang, "Voir les soins et les prix", "Treatments & prices")}</a>
        </div>
      </div>
      {photo("hero.jpg", S(lang, "Meghan pendant un massage dans son espace de soin", "Meghan giving a massage in her treatment room"), P("hero.jpg"), "photo--arch", eager=True)}
    </div>
  </section>

  <section class="section section--sand">
    <div class="container split split--top">
      <div>
        <h2>{S(lang, "Les soins", "Treatments")}</h2>
        <p>{S(lang,
            "Massage relaxant à l’huile chaude, drainage lymphatique, massage du visage liftant, ou les deux combinés pour ceux qui ont vraiment besoin de décrocher. Chaque séance commence par un petit moment d’échange pour adapter le soin à ce dont vous avez besoin ce jour-là.",
            "Warm-oil relaxing massage, lymphatic drainage, a lifting facial massage, or a combination of both for when you really need to switch off. Every session starts with a short chat so I can adapt the treatment to what you need that day.")}</p>
        <p class="muted">{S(lang,
            "Vous hésitez&nbsp;? Répondez à quatre petites questions et je vous propose le soin le plus adapté.",
            "Not sure? Answer four short questions and I’ll suggest the treatment that suits you best.")}</p>
        <div class="button-group">
          <a class="button" href="{f["quiz"]}">{S(lang, "Quel soin est fait pour moi&nbsp;?", "Which treatment is right for me?")}</a>
          <a class="button button--outline" href="{f["soins"]}">{S(lang, "Le détail de chaque soin", "Details of every treatment")}</a>
        </div>
      </div>
      <ul class="menu menu--compact">{price_menu(lang, f["soins"])}</ul>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>{S(lang, "Vos retours 🤎", "What clients say 🤎")}</h2>
      {reviews(["jambes", "souches", "weekend", "drainage-visage", "tonifiant"], lang)}
    </div>
  </section>

  <section class="section section--sand gift-band">
    <div class="container split split--reverse">
      {photo("bon-cadeau.jpg", S(lang, "Bons cadeaux « Un massage pour toi ! » par Meghan de Biolley, posés à côté de tulipes jaunes", "“Un massage pour toi !” gift vouchers by Meghan de Biolley, next to yellow tulips"), P("bon-cadeau.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Offrez un massage", "Give a massage")}</h2>
        <p class="price-tag"><span>{S(lang, "À partir de", "From")}</span><strong>90 €</strong></p>
        <p>{S(lang,
            "Pour Noël, un anniversaire, une naissance ou juste pour dire merci&nbsp;: un bon cadeau pour le soin de votre choix, en version papier ou électronique.",
            "For Christmas, a birthday, a new baby or just to say thank you: a gift voucher for the treatment of your choice, printed or electronic.")}</p>
        <p class="muted">{S(lang,
            "Ils se commandent directement auprès de moi sur WhatsApp et sont valables 6&nbsp;mois.",
            "Order directly from me on WhatsApp. Vouchers are valid for 6 months.")}</p>
        <div class="button-group">
          <a class="button" href="{f["gifts"]}">{S(lang, "Offrir un bon cadeau", "Give a gift voucher")}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container split">
      {photo("portrait.jpg", S(lang, "Portrait de Meghan de Biolley", "Portrait of Meghan de Biolley"), P("portrait.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Un mot sur moi", "A little about me")}</h2>
        <p>{S(lang,
            "J’ai appris le massage à Koh Samui, en Thaïlande, puis j’ai quitté mon job en agence de communication pour en faire mon métier. Depuis, je me suis aussi formée au sound healing, et je mélange volontiers les deux.",
            "I learned massage in Koh Samui, Thailand, then left my job at a communications agency to make it my profession. Since then I’ve also trained in sound healing, and I love combining the two.")}</p>
        <p>{S(lang,
            "Je parle français, néerlandais et anglais.",
            "I speak French, Dutch and English.")}</p>
        <a class="text-link" href="{f["about"]}">{S(lang, "Mon parcours", "My story")}</a>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">
      <div class="gallery">
        {photo("en-seance-1.jpg", S(lang, "Grange préparée pour une retraite Éclosion, tapis et briques de yoga", "Barn set up for an Éclosion retreat, with mats and yoga blocks"), P("en-seance-1.jpg"))}
        {photo("en-seance-2.jpg", S(lang, "Table préparée pour un atelier skincare, miroirs et produits", "Table set for a skincare workshop, with mirrors and products"), P("en-seance-2.jpg"))}
        {photo("en-seance-3.jpg", S(lang, "Meghan, souriante, face à un cercle de participantes assises", "Meghan smiling in front of a circle of seated participants"), P("en-seance-3.jpg"))}
      </div>
    </div>
  </section>

  <section class="section section--sand">
    <div class="container split split--reverse">
      {photo("sonotherapie.jpg", S(lang, "Meghan assise devant ses bols tibétains, un carillon à la main", "Meghan sitting by her Tibetan bowls, holding a chime"), P("sonotherapie.jpg"), "photo--wide")}
      <div>
        <h2>{S(lang, "EVJF, ateliers et entreprises", "Bachelorette parties, workshops and companies")}</h2>
        <p>{S(lang,
            "J’anime aussi des EVJF et des anniversaires (atelier auto-massage ou sound healing), des séances de sound healing chez moi (6 personnes max) ou partout en Belgique, et des moments bien-être pour les équipes et les marques.",
            "I also host bachelorette parties and birthdays (self-massage workshop or sound healing), sound healing sessions at my place (up to 6 people) or anywhere in Belgium, and wellbeing moments for teams and brands.")}</p>
        <ul class="link-list">
          <li><a href="{f["ateliers"]}#evjf">{S(lang, "Pour un EVJF", "For a bachelorette party")}</a></li>
          <li><a href="{f["ateliers"]}#entreprises">{S(lang, "Pour les entreprises", "For companies")}</a></li>
          <li><a href="{f["ateliers"]}#sonotherapie-groupe">{S(lang, "Sound healing en groupe", "Group sound healing")}</a></li>
          <li><a href="{f["ateliers"]}#auto-massage">{S(lang, "Atelier auto-massage", "Self-massage workshop")}</a></li>
        </ul>
      </div>
    </div>
  </section>

  {instagram_block(lang)}

  <section class="section section--tight">
    <div class="container text-center">
      {facts(lang)}
      <div class="button-group button-group--center">
        {ext(CALENDLY, S(lang, "Voir les disponibilités", "See availability"))}
      </div>
    </div>
  </section>
'''
    title = S(lang, "Meghan de Biolley | Massages et soins du visage à Uccle",
              "Meghan de Biolley | Massage and facials in Uccle, Brussels")
    desc = S(lang, "Meghan de Biolley, massothérapeute à Uccle (Bruxelles) : massage relaxant, drainage lymphatique, soin signature visage et sound healing. EVJF, ateliers et entreprises. Réservation en ligne.",
             "Meghan de Biolley, massage therapist in Uccle, Brussels: relaxing massage, lymphatic drainage, signature facial and sound healing. Bachelorette parties, workshops and companies. Book online.")
    identity = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Meghan de Biolley",
         "alternateName": "Meghan de Biolley, massages et soins", "url": SITE + "/",
         "inLanguage": ["fr", "en"]},
        {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness", "name": "Meghan de Biolley",
         "url": SITE + "/", "logo": SITE + "/images/favicon.png", "image": SITE + "/images/og-image.jpg",
         "description": desc, "telephone": PHONE_TEL, "priceRange": "90 € - 150 €",
         "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET, "postalCode": "1180",
                     "addressLocality": "Uccle", "addressRegion": "Bruxelles", "addressCountry": "BE"},
         "founder": {"@type": "Person", "name": "Meghan de Biolley", "jobTitle": S(lang, "Massothérapeute", "Massage therapist")},
         "sameAs": [INSTAGRAM, LINKEDIN, CALENDLY]},
    ]
    extra = "".join(f'\n  <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in identity)
    layout(lang, "home", title, desc, body, extra)


def soin_text(d, lang):
    """Opening of the description stays visible; the rest folds away on phones."""
    paras = d["desc"]
    shown, chars = [], 0
    for para in paras:
        if shown and chars >= 180:
            break
        shown.append(para)
        chars += len(para)
    rest = paras[len(shown):]
    html = "".join(f"<p>{x}</p>" for x in shown)
    more = "".join(f"<p>{x}</p>" for x in rest)
    if d["notes"]:
        more += '<ul class="soin-notes">' + "".join(f"<li>{n}</li>" for n in d["notes"]) + "</ul>"
    if more:
        html += (f'<details class="soin-more" data-open-desktop><summary>{S(lang, "Lire la suite", "Read more")}</summary>'
                 f'{more}</details>')
    return html


def page_soins(lang):
    f = FILES[lang]
    P = lambda name: S(lang, "Photo : images/", "Photo: images/") + name
    details = ""
    for i, s in enumerate(SOINS):
        d = s[lang]
        rev = " split--reverse" if i % 2 else ""
        dur = f'<span>{s["dur"][lang]}</span>' if s["dur"] else ""
        details += f'''
      <article class="treatment" id="{s["id"]}">
        <div class="split{rev}">
          {photo(s["img"], d["name"], P(s["img"]), "photo--arch")}
          <div class="treatment-info">
            <div class="treatment-head">
              <h2>{d["name"]}</h2>
              <p class="price-tag">{dur}<strong>{s["price"]}</strong></p>
              {ext(CALENDLY + "/" + s["cal"], S(lang, "Réserver", "Book"), "button treatment-book--phone")}
            </div>
            <div class="treatment-body">
              {soin_text(d, lang)}
              <div class="button-group treatment-book--desktop">
                {ext(CALENDLY + "/" + s["cal"], S(lang, "Réserver ce soin", "Book this treatment"))}
              </div>
            </div>
          </div>
        </div>
      </article>'''

    body = f'''
  <section class="page-hero">
    <div class="container container--narrow">
      <h1>{S(lang, "Soins et prix", "Treatments and prices")}</h1>
      <p class="lead">{S(lang,
          "Tous les soins ont lieu chez moi, avenue Hamoir à Uccle. Ils incluent un petit moment d’accueil pour parler de vos besoins avant de commencer.",
          "All treatments take place at my home on Avenue Hamoir in Uccle. Each one includes a short chat beforehand about what you need.")}</p>
      <p><a class="button button--outline" href="{f["quiz"]}">{S(lang, "Vous hésitez&nbsp;? Trouvez votre soin en 4 questions", "Not sure? Find your treatment in 4 questions")}</a></p>
      <ul class="menu">{price_menu(lang)}</ul>
      <p class="muted small" style="margin-top:1.5rem">{S(lang,
          "Toute séance annulée moins de 48&nbsp;h à l’avance reste due. Paiement en cash, par QR code ou sur facture. <a class='text-link' href='bons-cadeaux.html'>Bons cadeaux</a> disponibles.",
          "Sessions cancelled less than 48 hours in advance are charged. Payment by cash, QR code or invoice. <a class='text-link' href='gift-vouchers.html'>Gift vouchers</a> available.")}</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container">{details}
    </div>
  </section>

  <section class="section section--sand" id="appel">
    <div class="container split">
      <div>
        <h2>{S(lang, "Vous ne savez pas quoi choisir&nbsp;?", "Not sure which to choose?")}</h2>
        <p>{S(lang,
            "Faites le petit questionnaire, ou réservez un appel de 15&nbsp;minutes et on en discute ensemble. Vous pouvez aussi m’écrire sur Instagram.",
            "Try the short questionnaire, or book a 15-minute call and we’ll talk it through. You can also message me on Instagram.")}</p>
        <div class="button-group">
          <a class="button" href="{f["quiz"]}">{S(lang, "Le questionnaire", "The questionnaire")}</a>
          {ext(CALENDLY + "/30min", S(lang, "Réserver un appel", "Book a call"))}
          {ext(INSTAGRAM, "@meghandebiolley", "button button--outline")}
        </div>
      </div>
      {reviews(["recommander", "drainage-visage"], lang)}
    </div>
  </section>
'''
    layout(lang, "soins", S(lang, "Soins et prix", "Treatments and prices"),
           S(lang, "Les soins de Meghan de Biolley à Uccle : massage relaxant, drainage lymphatique, soin signature visage, rituels corps + visage et sonothérapie. Durées, prix et réservation en ligne.",
             "Meghan de Biolley’s treatments in Uccle, Brussels: relaxing massage, lymphatic drainage, signature facial, body + face rituals and sound therapy. Durations, prices and online booking."),
           body)


def page_ateliers(lang):
    f = FILES[lang]
    P = lambda name: S(lang, "Photo : images/", "Photo: images/") + name
    q = lambda t: t.replace(" ", "%20").replace("’", "%27")
    wa_evjf = wa(S(lang, "Bonjour Meghan, je voudrais organiser un EVJF. Date, lieu et nombre de participantes : ", "Hi Meghan, I’d like to plan a bachelorette party. Date, place and number of guests: "))
    wa_sound = wa(S(lang, "Bonjour Meghan, je voudrais organiser une séance de sound healing. Date, lieu et nombre de personnes : ", "Hi Meghan, I’d like to plan a sound healing session. Date, place and number of people: "))
    wa_atelier = wa(S(lang, "Bonjour Meghan, je voudrais organiser un atelier auto-massage. Date, lieu et nombre de personnes : ", "Hi Meghan, I’d like to plan a self-massage workshop. Date, place and number of people: "))
    mailto_corp = f"mailto:{EMAIL}?subject={q(S(lang, 'Demande de devis entreprise', 'Corporate quote request'))}"
    body = f'''
  <section class="page-hero">
    <div class="container container--narrow">
      <h1>{S(lang, "EVJF, ateliers et bien-être en entreprise", "Bachelorette parties, workshops and corporate wellbeing")}</h1>
      <p class="lead">{S(lang,
          "Un EVJF qui sort de l’ordinaire, un team building, une pause bien-être au bureau ou une animation pour une marque&nbsp;: je viens chez vous, partout en Belgique, ou je vous reçois chez moi à Uccle.",
          "A bachelorette party with a difference, team building, a wellbeing break at the office or a brand event: I come to you anywhere in Belgium, or welcome you at my place in Uccle.")}</p>
      <div class="button-group">
        <a class="button" href="#evjf">{S(lang, "EVJF", "Bachelorette")}</a>
        <a class="button button--outline" href="#entreprises">{S(lang, "Entreprises", "Companies")}</a>
        <a class="button button--outline" href="#sonotherapie-groupe">{S(lang, "Entre amis ou en famille", "Friends & family")}</a>
      </div>
    </div>
  </section>

  <section class="section section--sand" id="evjf">
    <div class="container split">
      {photo("evjf.jpg", S(lang, "Longue table préparée pour un atelier entre amies, avec miroirs et produits de soin", "Long table set for a workshop with friends, with mirrors and skincare products"), P("evjf.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Pour un EVJF", "For a bachelorette (hen) party")}</h2>
        <p>{S(lang,
            "Offrez à la future mariée et à ses amies un vrai moment de détente, à partager. Je viens dans le lieu de votre choix, partout en Belgique, avec tout le matériel.",
            "Give the bride-to-be and her friends a truly relaxing moment to share. I come to the venue of your choice, anywhere in Belgium, with everything needed.")}</p>
        <p>{S(lang, "Deux formules au choix&nbsp;:", "Two options:")}</p>
        <ul class="link-list">
          <li><a href="#auto-massage">{S(lang, "Atelier auto-massage", "Self-massage workshop")}</a></li>
          <li><a href="#sonotherapie-groupe">{S(lang, "Sound healing en groupe", "Group sound healing")}</a></li>
        </ul>
        <p class="muted" style="margin-top:1.25rem">{S(lang,
            "Dites-moi la date, le lieu et le nombre de participantes, et je vous envoie une proposition.",
            "Tell me the date, the place and the number of guests, and I’ll send you a proposal.")}</p>
        <div class="button-group">
          {ext(wa_evjf, S(lang, "Organiser un EVJF sur WhatsApp", "Plan it on WhatsApp"))}
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="entreprises">
    <div class="container">
      <div class="split split--top">
        <div>
          <h2>{S(lang, "Pour les entreprises et les marques", "For companies and brands")}</h2>
          <p>{S(lang,
              "J’ai travaillé plusieurs années en agence de communication avant de devenir massothérapeute, donc je connais bien les journées derrière un écran. Un moment bien-être, c’est une vraie pause pour vos équipes, et une façon simple de leur montrer que leur bien-être compte.",
              "I spent several years in a communications agency before becoming a massage therapist, so I know all about long days at a screen. A wellbeing break gives your team a real pause, and is a simple way to show that their wellbeing matters.")}</p>
          <p>{S(lang,
              "Ce que je propose le plus souvent&nbsp;:",
              "What I’m most often asked for:")}</p>
          <ul class="check-list">
            <li>{S(lang, "des massages relaxants dans une salle aménagée pour l’occasion", "relaxing massages in a room set up for the day")}</li>
            <li>{S(lang, "des massages mains et avant-bras de 10 à 15&nbsp;minutes pendant la pause de midi", "10 to 15 minute hand and forearm massages over lunch")}</li>
            <li>{S(lang, "un atelier d’auto-massage ou une séance de sound healing en team building", "a self-massage workshop or a sound healing session as team building")}</li>
            <li>{S(lang, "des ateliers skincare et des animations lors d’événements presse, sportifs ou de lancement", "skincare workshops and wellbeing moments at press, sports or launch events")}</li>
          </ul>
          <p class="muted">{S(lang,
              "Tout se fait sur devis, selon votre espace, votre timing et votre budget. Facture possible, en français, néerlandais ou anglais.",
              "Everything is quoted to fit your space, schedule and budget. Invoicing available, in French, Dutch or English.")}</p>
          <div class="button-group">
            <a class="button" href="{mailto_corp}">{S(lang, "Demander un devis", "Request a quote")}</a>
          </div>
        </div>
        <aside>
          {photo("entreprises.jpg", S(lang, "Meghan pendant un atelier de massage du visage pour Delbôve", "Meghan during a facial massage workshop for Delbôve"), P("entreprises.jpg"), "photo--arch")}
          <div class="note" style="margin-top:1.5rem">
          <p><strong>{S(lang, "Elles m’ont fait confiance", "Brands I’ve worked with")}</strong></p>
          <p>Sisley Paris, Avène, Delbôve, {S(lang, "et Arvesta pour son Ladies Day à l’Abbaye de Floreffe, où j’ai animé un atelier skincare pour des agricultrices.", "and Arvesta for its Ladies Day at Floreffe Abbey, where I ran a skincare workshop for women farmers.")}</p>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="section section--sand" id="sonotherapie-groupe">
    <div class="container split">
      {photo("atelier-sonotherapie.jpg", S(lang, "Séance de sound healing en groupe : Meghan joue d’un bol au-dessus des participantes allongées", "Group sound healing: Meghan plays a bowl above participants lying down"), P("atelier-sonotherapie.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Sound healing en groupe", "Group sound healing")}</h2>
        <p>{S(lang,
            "On s’allonge, on ferme les yeux, et on laisse les bols tibétains faire le reste. Beaucoup de gens s’endorment, et c’est très bien comme ça&nbsp;!",
            "You lie down, close your eyes and let the Tibetan bowls do the rest. Lots of people fall asleep, and that’s perfectly fine!")}</p>
        <p>{S(lang,
            "Chez moi à Uccle pour 6 personnes maximum, ou je me déplace partout en Belgique (frais de déplacement en plus). Une chouette idée pour un team building, un EVJF, un week-end en famille ou un anniversaire.",
            "At my place in Uccle for up to 6 people, or I travel anywhere in Belgium (plus travel costs). A great idea for team building, a bachelorette party, a family weekend or a birthday.")}</p>
        {reviews(["souches", "copines"], lang)}
        <div class="button-group">
          {ext(wa_sound, S(lang, "Demander une date sur WhatsApp", "Ask for a date on WhatsApp"))}
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="auto-massage">
    <div class="container split split--reverse">
      {photo("atelier-auto-massage.jpg", S(lang, "Meghan montre un geste de massage du visage pendant un atelier", "Meghan showing a facial massage technique during a workshop"), P("atelier-auto-massage.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Atelier auto-massage", "Self-massage workshop")}</h2>
        <p>{S(lang,
            "Je vous apprends quelques gestes simples pour détendre le visage, la nuque et les épaules, que vous pourrez refaire à la maison.",
            "I teach you a few simple techniques to relax your face, neck and shoulders that you can keep using at home.")}</p>
        <p>{S(lang,
            "Parfait pour un EVJF, un anniversaire ou un après-midi entre amies. En entreprise, ça marche très bien en team building.",
            "Perfect for a bachelorette party, a birthday or an afternoon with friends. It also works really well as a company team building.")}</p>
        <div class="button-group">
          {ext(wa_atelier, S(lang, "Organiser un atelier sur WhatsApp", "Plan a workshop on WhatsApp"))}
        </div>
      </div>
    </div>
  </section>

  <section class="section section--sand" id="eclosion">
    <div class="container split">
      <div>
        <h2>{S(lang, "Éclosion, ma retraite d’un jour", "Éclosion, my one-day retreat")}</h2>
        <p>{S(lang,
            "Une journée pour une douzaine de femmes, à une heure de Bruxelles, pour faire un vrai reset. La première édition était complète en quelques jours, et je prépare les suivantes.",
            "A day for around twelve women, an hour from Brussels, for a proper reset. The first edition sold out within days, and I’m planning the next ones.")}</p>
        <blockquote class="quote">{S(lang, "« J’ai l’impression d’être partie une semaine en vacances. »", "“It feels like I’ve been on holiday for a week.”")}</blockquote>
        <p class="muted small">{S(lang, "Une participante", "A participant")}</p>
        <div class="button-group">
          {ext(INSTAGRAM, S(lang, "Les prochaines dates sont annoncées sur Instagram", "Next dates are announced on Instagram"), "button button--outline")}
        </div>
      </div>
      {photo("eclosion.jpg", S(lang, "Meghan avec le tote bag Éclosion", "Meghan with the Éclosion tote bag"), P("eclosion.jpg"), "photo--arch")}
    </div>
  </section>

  <section class="section section--tight">
    <div class="container container--narrow text-center">
      <p class="lead">{S(lang,
          "Dites-moi la date, le lieu et le nombre de personnes, et je vous envoie une proposition.",
          "Tell me the date, the place and how many people, and I’ll send you a proposal.")}</p>
      <div class="button-group button-group--center">
        {ext(wa(S(lang, "Bonjour Meghan, ", "Hi Meghan, ")), S(lang, "Écrire sur WhatsApp", "Message me on WhatsApp"))}
        <a class="button button--outline" href="{mailto_corp}">{S(lang, "Entreprises&nbsp;: par e-mail", "Companies: by email")}</a>
      </div>
    </div>
  </section>
'''
    layout(lang, "ateliers", S(lang, "EVJF, ateliers et bien-être en entreprise", "Bachelorette parties, workshops and corporate wellbeing"),
           S(lang, "Meghan de Biolley anime des EVJF bien-être (atelier auto-massage, sound healing), des team buildings et massages en entreprise, des ateliers skincare et événements de marque, partout en Belgique.",
             "Meghan de Biolley hosts wellbeing bachelorette and hen parties (self-massage workshop, sound healing), team building and massages for companies, skincare workshops and brand events, anywhere in Belgium."),
           body)


def page_about(lang):
    f = FILES[lang]
    P = lambda name: S(lang, "Photo : images/", "Photo: images/") + name
    body = f'''
  <section class="page-hero">
    <div class="container split split--top">
      <div>
        <h1>{S(lang, "Bonjour, moi c’est Meghan", "Hi, I’m Meghan")}</h1>
        <p>{S(lang,
            "Avant le massage, j’ai travaillé plusieurs années en agence de communication. J’ai suivi mes formations en massage il y a environ quatre ans à Koh Samui, en Thaïlande, et c’est devenu une évidence&nbsp;: c’est ça que j’avais envie de faire.",
            "Before massage, I spent several years in a communications agency. About four years ago I trained in massage in Koh Samui, Thailand, and it quickly became clear: this was what I wanted to do.")}</p>
        <p>{S(lang,
            "En 2025, je me suis lancée comme indépendante. Aujourd’hui, je reçois chez moi à Uccle pour des massages du corps et du visage, j’anime des ateliers et des séances de sound healing, et j’organise des retraites d’un jour avec Éclosion.",
            "In 2025 I went independent. Today I welcome people at home in Uccle for body and facial massage, run workshops and sound healing sessions, and organise one-day retreats with Éclosion.")}</p>
        <p>{S(lang,
            "Ce que j’aime le plus&nbsp;? Les petits messages que je reçois après une séance. Ils me font toujours tellement plaisir 🤎",
            "What I love most? The little messages I get after a session. They always make my day 🤎")}</p>
      </div>
      {photo("portrait.jpg", S(lang, "Portrait de Meghan de Biolley", "Portrait of Meghan de Biolley"), P("portrait.jpg"), "photo--arch", eager=True)}
    </div>
  </section>

  <section class="section section--sand">
    <div class="container split split--reverse">
      {video("espace.mp4", "espace-poster.jpg", S(lang, "Courte vidéo de l’espace de soin à Uccle", "Short video of the treatment room in Uccle"))}
      <div>
        <h2>{S(lang, "Formations et expériences", "Training and experience")}</h2>
        <ul class="check-list">
          <li>{S(lang, "Formations en massage à Koh Samui, Thaïlande", "Massage training in Koh Samui, Thailand")}</li>
          <li>{S(lang, "Certification en sound healing", "Sound healing certification")}</li>
          <li>{S(lang, "Ateliers et événements pour Sisley Paris, Avène, Delbôve et Arvesta", "Workshops and events for Sisley Paris, Avène, Delbôve and Arvesta")}</li>
          <li>{S(lang, "Fondatrice d’Éclosion, retraites bien-être d’un jour", "Founder of Éclosion, one-day wellbeing retreats")}</li>
          <li>{S(lang, "Français, néerlandais et anglais", "French, Dutch and English")}</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container container--narrow">
      <h2>{S(lang, "Mon histoire en podcast", "My story in a podcast")}</h2>
      <p>{S(lang,
          "J’ai raconté ma reconversion dans l’épisode 38 du podcast de Pop Corn Studio&nbsp;: les doutes, la prise de risque, et pourquoi je ne regrette rien.",
          "I talked about my career change in episode 38 of the Pop Corn Studio podcast (in French): the doubts, the risk, and why I have no regrets.")}</p>
      {ext(PODCAST, S(lang, "Écouter sur Spotify", "Listen on Spotify"), "button button--outline")}
    </div>
  </section>
'''
    layout(lang, "about", S(lang, "À propos", "About"),
           S(lang, "Meghan de Biolley, massothérapeute à Uccle formée en Thaïlande et certifiée en sound healing.",
             "Meghan de Biolley, massage therapist in Uccle, Brussels, trained in Thailand and certified in sound healing."),
           body)


def page_gifts(lang):
    f = FILES[lang]
    P = lambda name: S(lang, "Photo : images/", "Photo: images/") + name
    gift_contact = contact_buttons(lang,
                                   S(lang, "Bonjour Meghan, je voudrais commander un bon cadeau pour ", "Hi Meghan, I’d like to order a gift voucher for "),
                                   S(lang, "Bon cadeau", "Gift voucher"))
    mailto_corp = f"mailto:{EMAIL}?subject=" + quote(S(lang, "Bons cadeaux entreprise", "Corporate gift vouchers"))
    body = f'''
  <section class="page-hero">
    <div class="container split">
      <div>
        <h1>{S(lang, "Bons cadeaux", "Gift vouchers")}</h1>
        <p class="lead">{S(lang,
            "Pour un anniversaire, une naissance, la fête des mères ou juste pour dire merci&nbsp;: tous les soins peuvent être offerts.",
            "For a birthday, a new baby, Mother’s Day or just to say thank you: every treatment can be given as a gift.")}</p>
        <p>{S(lang,
            "Les bons se commandent directement auprès de moi, de préférence sur WhatsApp, ou via Instagram ou par e-mail. Dites-moi quel soin vous voulez offrir et si vous préférez un bon papier ou un bon électronique (pratique pour les cadeaux de dernière minute). Paiement en cash, par QR code ou sur facture.",
            "Vouchers are ordered directly from me, preferably on WhatsApp, or via Instagram or email. Tell me which treatment you’d like to give and whether you prefer a printed voucher or an electronic one (handy for last-minute gifts). Payment by cash, QR code or invoice.")}</p>
        <p class="price-tag"><span>{S(lang, "Valable", "Valid for")}</span><strong>{S(lang, "6 mois", "6 months")}</strong></p>
        <div class="button-group">
          {gift_contact}
        </div>
      </div>
      {photo("bon-cadeau.jpg", S(lang, "Bons cadeaux « Un massage pour toi ! » par Meghan de Biolley, posés à côté de tulipes jaunes", "“Un massage pour toi !” gift vouchers by Meghan de Biolley, next to yellow tulips"), P("bon-cadeau.jpg"), "photo--arch", eager=True)}
    </div>
  </section>

  <section class="section section--sand">
    <div class="container split split--reverse">
      {photo("bon-cadeau-enveloppes.jpg", S(lang, "Bons cadeaux dans des enveloppes kraft fermées par un ruban", "Gift vouchers in kraft envelopes tied with a ribbon"), P("bon-cadeau-enveloppes.jpg"), "photo--arch")}
      <div>
        <h2>{S(lang, "Prêt à offrir", "Ready to give")}</h2>
        <p>{S(lang,
            "En version papier, le bon est présenté dans une jolie enveloppe kraft fermée par un ruban. Il n’y a plus qu’à le glisser sous le sapin ou à le donner en main propre.",
            "The printed voucher comes in a pretty kraft envelope tied with a ribbon. All that’s left is to slip it under the tree or hand it over in person.")}</p>
        <p class="muted">{S(lang,
            "Pour une surprise de dernière minute, la version électronique est aussi possible.",
            "For a last-minute surprise, an electronic version is also available.")}</p>
        <div class="button-group">
          {gift_contact}
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container container--narrow">
      <h2>{S(lang, "Les soins à offrir", "Treatments to give")}</h2>
      <ul class="menu">{price_menu(lang, f["soins"])}</ul>
      <p class="muted small" style="margin-top:1.5rem">{S(lang,
          "Vous voulez offrir des bons à votre équipe ou à vos clients&nbsp;? C’est possible aussi, avec facture&nbsp;: <a class='text-link' href='" + mailto_corp + "'>écrivez-moi par e-mail</a>.",
          "Want to give vouchers to your team or clients? That works too, with an invoice: <a class='text-link' href='" + mailto_corp + "'>email me</a>.")}</p>
    </div>
  </section>
'''
    layout(lang, "gifts", S(lang, "Bons cadeaux", "Gift vouchers"),
           S(lang, "Offrez un massage ou un soin du visage à Uccle : bons cadeaux papier ou électroniques, à commander directement auprès de Meghan de Biolley.",
             "Give a massage or facial in Uccle, Brussels: printed or electronic gift vouchers, ordered directly from Meghan de Biolley."),
           body)


QUIZ_TEXT = {
    "fr": {
        "progress": "Question {n} sur {total}",
        "back": "← Retour",
        "restart": "Recommencer",
        "result_eyebrow": "Mon conseil pour vous",
        "book": "Réserver ce soin",
        "details": "Voir le détail",
        "up_title": "Envie de prolonger le moment&nbsp;?",
        "up_line": "Pour vous faire encore plus plaisir&nbsp;:",
        "down_title": "Envie de quelque chose de plus court&nbsp;?",
        "down_line": "Une version plus courte, tout aussi douce&nbsp;:",
        "book_short": "Réserver",
        "call": "Encore un doute&nbsp;? Réservez un appel de 15&nbsp;minutes et on en parle.",
        "call_btn": "Réserver un appel",
        "questions": {
            "reason": {"q": "Qu’est-ce qui vous amène&nbsp;?", "options": [
                ["relax", "Envie de me détendre, tout simplement"],
                ["legs", "Jambes lourdes, rétention d’eau, besoin de légèreté"],
                ["face", "Des tensions au visage ou à la mâchoire, envie d’un coup d’éclat"],
                ["mind", "Un mental qui tourne en boucle, du mal à lâcher prise"]]},
            "zone": {"q": "Sur quelle zone avez-vous envie que je travaille&nbsp;?", "options": [
                ["body", "Le corps"], ["face", "Le visage"], ["both", "Les deux"]]},
            "time": {"q": "Combien de temps pouvez-vous vous accorder&nbsp;?", "options": [
                ["60", "1 heure"], ["90", "1 h 30"], ["120", "2 heures"]]},
            "sound": {"q": "Les sons et vibrations des bols tibétains, ça vous tente&nbsp;?", "options": [
                ["yes", "Oui, j’ai envie d’essayer"], ["maybe", "Pourquoi pas"], ["no", "Pas cette fois"]]},
        },
    },
    "en": {
        "progress": "Question {n} of {total}",
        "back": "← Back",
        "restart": "Start again",
        "result_eyebrow": "My suggestion for you",
        "book": "Book this treatment",
        "details": "See details",
        "up_title": "Want to make it last a little longer?",
        "up_line": "To treat yourself even more:",
        "down_title": "Prefer something shorter?",
        "down_line": "A shorter version, just as gentle:",
        "book_short": "Book",
        "call": "Still not sure? Book a 15-minute call and we’ll talk it through.",
        "call_btn": "Book a call",
        "questions": {
            "reason": {"q": "What brings you here?", "options": [
                ["relax", "I simply want to relax"],
                ["legs", "Heavy legs, water retention, I want to feel lighter"],
                ["face", "Tension in my face or jaw, I’d like a radiance boost"],
                ["mind", "My mind keeps racing, I find it hard to let go"]]},
            "zone": {"q": "Which area would you like me to focus on?", "options": [
                ["body", "My body"], ["face", "My face"], ["both", "Both"]]},
            "time": {"q": "How much time can you give yourself?", "options": [
                ["60", "1 hour"], ["90", "1 hr 30"], ["120", "2 hours"]]},
            "sound": {"q": "Do the sounds and vibrations of Tibetan singing bowls appeal to you?", "options": [
                ["yes", "Yes, I’d love to try"], ["maybe", "Why not"], ["no", "Not this time"]]},
        },
    },
}


def page_quiz(lang):
    f = FILES[lang]
    prefix = "" if lang == "fr" else "../"
    data = {
        "text": QUIZ_TEXT[lang],
        "treatments": {
            s["id"]: {
                "name": s[lang]["name"], "short": s[lang]["short"],
                "meta": (s["dur"][lang] + " · " if s["dur"] else "") + s["price"],
                "img": prefix + "images/" + s["img"],
                "book": CALENDLY + "/" + s["cal"],
                "details": f["soins"] + "#" + s["id"],
                "minutes": {"1 h": 60, "1 h 30": 90, "2 h": 120}[s["dur"]["fr"]],
                "euros": int(s["price"].split()[0]),
            } for s in SOINS
        },
        "call": CALENDLY + "/30min",
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    body = f'''
  <section class="page-hero">
    <div class="container container--narrow">
      <h1>{S(lang, "Quel soin est fait pour moi&nbsp;?", "Which treatment is right for me?")}</h1>
      <p class="lead">{S(lang,
          "Quatre petites questions au maximum, et je vous propose le soin le plus adapté. Vos réponses ne sont enregistrées nulle part.",
          "Four short questions at most, and I’ll suggest the treatment that suits you best. Your answers aren’t stored anywhere.")}</p>

      <div class="quiz" data-quiz aria-live="polite">
        <noscript>
          <p>{S(lang,
              "Ce questionnaire a besoin de JavaScript. Vous pouvez aussi consulter <a class='text-link' href='soins.html'>tous les soins</a> ou réserver un appel de 15&nbsp;minutes.",
              "This questionnaire needs JavaScript. You can also browse <a class='text-link' href='treatments.html'>all treatments</a> or book a 15-minute call.")}</p>
        </noscript>
      </div>

      <p class="muted small" style="margin-top:2rem">{S(lang,
          "C’est une première piste&nbsp;: au début de chaque séance, on prend toujours le temps d’adapter le soin à ce dont vous avez besoin ce jour-là.",
          "It’s a first idea: at the start of every session we always take time to adapt the treatment to what you need that day.")}</p>
    </div>
  </section>
'''
    extra = (f'\n  <script type="application/json" id="quiz-data">{payload}</script>'
             f'\n  <script src="{prefix}js/quiz.js" defer></script>')
    layout(lang, "quiz", S(lang, "Quel soin est fait pour moi ?", "Which treatment is right for me?"),
           S(lang, "Répondez à quatre questions et Meghan de Biolley vous conseille le massage ou le soin du visage le plus adapté à vos envies, à Uccle.",
             "Answer four questions and Meghan de Biolley suggests the massage or facial that suits you best, in Uccle, Brussels."),
           body, extra)


FAQ = {
    "fr": [
        ("Quel soin choisir&nbsp;?", "Le <a class=\"text-link\" href=\"quel-soin.html\">petit questionnaire</a> vous propose un soin en quatre questions, et les descriptions de la page <a class=\"text-link\" href=\"soins.html\">Les soins</a> vous aideront à y voir plus clair. Si vous hésitez encore, réservez un appel questions-réponses ou écrivez-moi sur Instagram&nbsp;: nous trouverons ensemble le soin le plus adapté."),
        ("Comment réserver&nbsp;?", f"Les soins individuels se réservent en ligne via <a class=\"text-link\" href=\"{CALENDLY}\" target=\"_blank\" rel=\"noopener\">mon calendrier Calendly</a>. Pour un atelier, un EVJF ou une séance de groupe, écrivez-moi sur WhatsApp (ou par e-mail pour les entreprises)."),
        ("Comment me préparer à la séance&nbsp;?", "Le parking est gratuit dans la rue. Les soins qui incluent le visage et le cuir chevelu peuvent légèrement huiler les cheveux&nbsp;: mieux vaut ne pas prévoir d’événement important juste après."),
        ("Le soin visage est-il un soin esthétique&nbsp;?", "Non&nbsp;: il n’y a pas d’extraction. Il s’agit d’un massage du visage relaxant, liftant et sculptant, qui apporte un bel éclat et un effet lifté. Pour des résultats plus durables, une cure de 5 séances à tarif avantageux est possible."),
        ("Puis-je offrir un soin&nbsp;?", "Oui&nbsp;! Les bons cadeaux existent en version papier ou électronique et sont valables 6&nbsp;mois. Tout est expliqué sur la page <a class=\"text-link\" href=\"bons-cadeaux.html\">Bons cadeaux</a>."),
        ("Dans quelles langues se déroulent les soins&nbsp;?", "En français, en néerlandais ou en anglais, selon votre préférence."),
        ("Puis-je annuler ou déplacer mon rendez-vous&nbsp;?", "Oui, en me prévenant au moins 48&nbsp;heures à l’avance. Toute séance annulée moins de 48&nbsp;h à l’avance reste due."),
        ("Quels sont les moyens de paiement&nbsp;?", "Vous pouvez régler en espèces, par QR code ou sur facture."),
        ("Y a-t-il des contre-indications&nbsp;?", "Si vous êtes enceinte, suivez un traitement médical ou avez un problème de santé particulier, signalez-le avant la séance. En cas de doute, demandez l’avis de votre médecin. Les soins proposés sont des soins de bien-être et ne remplacent pas un suivi médical."),
    ],
    "en": [
        ("Which treatment should I choose?", "The <a class=\"text-link\" href=\"which-treatment.html\">short questionnaire</a> suggests a treatment in four questions, and the descriptions on the <a class=\"text-link\" href=\"treatments.html\">Treatments</a> page will help. If you’re still unsure, book a Q&amp;A call or message me on Instagram and we’ll find the right treatment together."),
        ("How do I book?", f"One-to-one treatments are booked online through <a class=\"text-link\" href=\"{CALENDLY}\" target=\"_blank\" rel=\"noopener\">my Calendly page</a>. For a workshop, a bachelorette party or a group session, message me on WhatsApp (or by email for companies)."),
        ("How should I prepare?", "Street parking is free. Treatments that include the face and scalp may leave your hair slightly oily, so it’s best not to plan anything important straight afterwards."),
        ("Is the facial a beauty treatment?", "No extractions are involved: it’s a relaxing, lifting and sculpting facial massage that leaves you with a lovely glow and a lifted look. For longer-lasting results, a course of 5 sessions at a reduced rate is available."),
        ("Can I give a treatment as a gift?", "Yes! Gift vouchers come in printed or electronic form and are valid for 6 months. See the <a class=\"text-link\" href=\"gift-vouchers.html\">Gift vouchers</a> page for details."),
        ("Which languages do you speak?", "French, Dutch and English: whichever you prefer."),
        ("Can I cancel or reschedule?", "Yes, with at least 48 hours’ notice. Sessions cancelled less than 48 hours in advance are charged in full."),
        ("How can I pay?", "Cash, QR code or invoice."),
        ("Are there any contraindications?", "If you are pregnant, receiving medical treatment or have a particular health condition, please let me know before your session. If in doubt, ask your doctor. These are wellbeing treatments and do not replace medical care."),
    ],
}


def page_contact(lang):
    jsonld = {
        "@context": "https://schema.org", "@type": "HealthAndBeautyBusiness",
        "name": "Meghan de Biolley", "url": SITE + "/", "telephone": PHONE_TEL, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS_STREET, "postalCode": "1180",
                    "addressLocality": "Uccle", "addressRegion": "Bruxelles", "addressCountry": "BE"},
        "sameAs": [INSTAGRAM, LINKEDIN], "paymentAccepted": "Cash, QR code, Invoice",
    }
    extra = f'\n  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
    faq = "".join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in FAQ[lang])
    body = f'''
  <section class="page-hero">
    <div class="container split split--top">
      <div>
        <h1>Contact</h1>
        <p class="lead">{S(lang, "Le plus simple pour réserver, c’est en ligne. Pour une question, un atelier ou un bon cadeau, écrivez-moi sur WhatsApp. Pour les entreprises, l’e-mail est parfait.",
                           "The easiest way to book is online. For a question, a workshop or a gift voucher, message me on WhatsApp. For companies, email works best.")}</p>
        <ul class="contact-list">
          <li><span>{S(lang, "Réserver", "Book")}</span><a href="{CALENDLY}" target="_blank" rel="noopener">calendly.com/meghandebiolley</a></li>
          <li><span>WhatsApp</span><a href="{WHATSAPP}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></li>
          <li><span>{S(lang, "Entreprises", "Companies")}</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span>Instagram</span><a href="{INSTAGRAM}" target="_blank" rel="noopener">@meghandebiolley</a></li>
          <li><span>LinkedIn</span><a href="{LINKEDIN}" target="_blank" rel="noopener">Meghan de Biolley</a></li>
        </ul>
      </div>
      <div class="card">
        <h2 class="h3">{S(lang, "Où me trouver", "Where to find me")}</h2>
        <address>{ADDRESS_STREET}<br>{ADDRESS_2}</address>
        <p class="muted small">{S(lang, "Le numéro exact figure dans votre réservation.", "The exact house number is included in your booking.")}</p>
        <p><a class="text-link" href="{MAPS}" target="_blank" rel="noopener">{S(lang, "Ouvrir dans Google Maps", "Open in Google Maps")}</a></p>
        <p class="muted">{S(lang,
            "Uniquement sur rendez-vous. Parking gratuit dans la rue. Toute séance annulée moins de 48&nbsp;h à l’avance reste due. Paiement en cash, par QR code ou sur facture.",
            "By appointment only. Free street parking. Sessions cancelled less than 48 hours in advance are charged. Payment by cash, QR code or invoice.")}</p>
      </div>
    </div>
  </section>

  <section class="section section--sand" id="faq">
    <div class="container">
      <div class="section-heading section-heading--center">
        <h2>{S(lang, "Questions fréquentes", "Frequently asked questions")}</h2>
      </div>
      <div class="faq">{faq}</div>
    </div>
  </section>
'''
    layout(lang, "contact", S(lang, "Contact", "Contact"),
           S(lang, "Contactez Meghan de Biolley, praticienne en massage à Uccle : réservation en ligne, téléphone, e-mail, adresse et questions fréquentes.",
             "Contact Meghan de Biolley, massage practitioner in Uccle, Brussels: online booking, phone, email, address and FAQ."),
           body, extra)


def page_legal(lang):
    bce = "BE 1021.898.760"
    if lang == "fr":
        content = f'''
      <h2>Éditrice du site</h2>
      <p>Meghan de Biolley, praticienne indépendante en massages et soins bien-être<br>
      {ADDRESS_1}, {ADDRESS_2}, Belgique<br>
      Numéro d’entreprise (BCE)&nbsp;: {bce}<br>
      E-mail&nbsp;: <a href="mailto:{EMAIL}">{EMAIL}</a><br>
      Téléphone&nbsp;: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>

      <h2>Hébergement</h2>
      <p>Ce site est hébergé par GitHub Pages, un service de GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>

      <h2>Nature des soins</h2>
      <p>Les massages et soins proposés sont des soins de bien-être, à visée de détente. Ils ne constituent ni un acte médical ni un traitement thérapeutique et ne remplacent pas l’avis d’un professionnel de santé.</p>

      <h2>Propriété intellectuelle</h2>
      <p>Les textes, photographies et éléments graphiques de ce site sont la propriété de Meghan de Biolley, sauf mention contraire. Toute reproduction sans autorisation préalable est interdite.</p>

      <h2>Données personnelles</h2>
      <p>Ce site ne contient aucun formulaire et ne dépose aucun cookie de suivi. Les données que vous transmettez par WhatsApp, e-mail, téléphone ou Instagram sont utilisées uniquement pour répondre à votre demande et organiser votre rendez-vous, et ne sont jamais cédées à des tiers.</p>
      <p>La prise de rendez-vous en ligne s’effectue sur Calendly, service tiers soumis à sa propre politique de confidentialité. Les polices de caractères du site sont chargées depuis Google Fonts.</p>
      <p>Conformément au RGPD, vous pouvez demander l’accès, la rectification ou la suppression de vos données en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''
    else:
        content = f'''
      <h2>Site publisher</h2>
      <p>Meghan de Biolley, independent massage and wellbeing practitioner<br>
      {ADDRESS_1}, {ADDRESS_2}, Belgium<br>
      Company number (BCE/KBO): {bce}<br>
      Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>
      Phone: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>

      <h2>Hosting</h2>
      <p>This site is hosted by GitHub Pages, a service of GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>

      <h2>Nature of the treatments</h2>
      <p>The massages and treatments offered are wellbeing treatments intended for relaxation. They are not medical or therapeutic procedures and do not replace advice from a healthcare professional.</p>

      <h2>Intellectual property</h2>
      <p>The texts, photographs and graphics on this site belong to Meghan de Biolley unless stated otherwise. Reproduction without prior permission is prohibited.</p>

      <h2>Personal data</h2>
      <p>This site has no forms and sets no tracking cookies. Information you send by WhatsApp, email, phone or Instagram is used only to answer your request and arrange your appointment, and is never shared with third parties.</p>
      <p>Online booking is handled by Calendly, a third-party service with its own privacy policy. The site’s fonts are loaded from Google Fonts.</p>
      <p>Under the GDPR, you can request access to, correction or deletion of your data by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''
    body = f'''
  <section class="page-hero">
    <div class="container container--narrow">
      <span class="eyebrow">{S(lang, "Informations légales", "Legal information")}</span>
      <h1>{S(lang, "Mentions légales", "Legal notice")}</h1>
    </div>
  </section>
  <section class="section section--tight">
    <div class="container container--narrow prose">{content}
    </div>
  </section>
'''
    layout(lang, "legal", S(lang, "Mentions légales", "Legal notice"),
           S(lang, "Mentions légales et politique de confidentialité du site de Meghan de Biolley.",
             "Legal notice and privacy policy for Meghan de Biolley’s website."), body,
           '\n  <meta name="robots" content="noindex">')


for lang in ("fr", "en"):
    page_home(lang)
    page_soins(lang)
    page_ateliers(lang)
    page_about(lang)
    page_contact(lang)
    page_gifts(lang)
    page_quiz(lang)
    page_legal(lang)

# 404 (served by GitHub Pages from any path, so use root-relative URLs)
with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
    fh.write(f'''<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page introuvable | Meghan de Biolley</title>
  <meta name="robots" content="noindex">
  <link rel="icon" href="/images/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500&family=DM+Sans:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
<main class="section">
  <div class="container text-center">
    <span class="monogram" aria-hidden="true" style="margin-bottom:1.5rem">MB</span>
    <h1>Cette page s’est égarée.</h1>
    <p class="lead">La page demandée n’existe pas ou plus. <span lang="en">This page doesn’t exist.</span></p>
    <div class="button-group button-group--center">
      <a class="button" href="/">Retour à l’accueil</a>
      <a class="button button--outline" href="/en/" lang="en">English homepage</a>
    </div>
  </div>
</main>
</body>
</html>
''')

# sitemap.xml + robots.txt: tell search engines which pages exist, in both languages
import datetime


def page_url(lang, key):
    name = FILES[lang][key]
    path = "" if name == "index.html" else name[:-len(".html")]
    return SITE + "/" + ("" if lang == "fr" else "en/") + path


today = datetime.date.today().isoformat()
order = ["home", "soins", "ateliers", "gifts", "quiz", "about", "contact"]  # legal notice left out on purpose (noindex)
priority = {"home": "1.0", "soins": "0.9", "ateliers": "0.9", "gifts": "0.8", "quiz": "0.6",
            "about": "0.6", "contact": "0.7", "legal": "0.2"}
entries = []
for key in order:
    alternates = "".join(
        f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, key)}"/>' for l in ("fr", "en"))
    for lang in ("fr", "en"):
        entries.append(f"""  <url>
    <loc>{page_url(lang, key)}</loc>
    <lastmod>{today}</lastmod>
    <priority>{priority[key]}</priority>{alternates}
  </url>""")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
    fh.write(f"User-agent: *\nAllow: /\nDisallow: /_outils/\n\nSitemap: {SITE}/sitemap.xml\n")

print("ok")
