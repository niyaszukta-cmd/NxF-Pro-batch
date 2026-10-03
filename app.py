"""
Finzcom x NYZTrade - Equity Trading Webinar Library
===================================================
A password-gated Streamlit app for sharing webinar recordings (Veed.io embeds).
Laid out for laptop and phone: the player resizes to the screen, and the session
list lives in the sidebar on desktop and in a collapsible picker on mobile.

Run locally:   streamlit run app.py
Set the password (in order of priority):
  1. .streamlit/secrets.toml  ->  APP_PASSWORD = "your-password"
  2. environment variable     ->  APP_PASSWORD=your-password
  3. the DEFAULT_PASSWORD constant below (change it before you deploy)
"""

import os
import re

import streamlit as st
import streamlit.components.v1 as components

# ─────────────────────────────────────────────────────────────────────────────
# 1. ACCESS
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_PASSWORD = "finzcom2026"         # ← change this before sharing

# ─────────────────────────────────────────────────────────────────────────────
# 2. BRANDING / COPY   ── edit freely
# ─────────────────────────────────────────────────────────────────────────────
BRAND_LEFT = "Finzcom"
BRAND_RIGHT = "NYZTrade"
SERIES_TITLE = "The Trading Foundation for Indian Equity Traders"
SERIES_BLURB = (
    "Recorded sessions on reading price and volume, building a watchlist, "
    "sizing a position and knowing where you're wrong — taught on real charts, "
    "for people who trade their own money."
)
HOST_LINE = "Hosted by Dr. Niyas N · NYZTrade Financial Solutions"

# ─────────────────────────────────────────────────────────────────────────────
# 3. SESSION LIBRARY
#    Replace the titles, descriptions and topics below with your curriculum.
#
#    HOW TO ADD A RECORDING
#    ──────────────────────
#    1. In Veed: open the video → Share → Embed → Copy code.
#    2. Veed gives you two lines. Keep ONLY the <iframe ...></iframe> line.
#       Drop the "made with VEED" <a href="..."> link underneath it — that is
#       Veed's own footer link, and pasting it here does nothing.
#    3. Paste it between SINGLE quotes, on the "embed" line:
#
#           "embed": '<iframe src="https://www.veed.io/embed/xxxx" ...></iframe>',
#
#       Single quotes matter. The iframe's src is already wrapped in double
#       quotes, so using double quotes on the outside breaks the file.
#    4. Keep the comma at the end of the line.
#
#    Only the src URL is read — the width="744" height="504" in Veed's code is
#    ignored, so the player can resize itself to the screen. To hide the Veed
#    watermark or the share button, switch those off in Veed's embed options
#    before copying (they come through as watermark=0 and sharing=0 in the URL).
#    A session with an empty "embed" shows a "recording is not up yet" card, so
#    you can publish the outline before every video is uploaded.
# ─────────────────────────────────────────────────────────────────────────────
WEBINAR_SESSIONS = [
    {
        "title": "Introduction to tradingview and platform navigation",
        "desc": "",
        "topics": [
            "",
            "",
        ],
        # Recorded 8 Sep 2026
        "embed": '<iframe src="https://veed.io/embed/3dfe43de-6875-4dfe-a34e-3e23800f5f69?watermark=0&color=&sharing=0&title=1" width="744" height="504" frameborder="0" title="Batch 36 class 1" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "Deeper dive into tradingview features",
        "desc": "",
        "topics": [
            "Earnings card analysis",
            "Gold chart analysis",
            "other tradingview features",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/5ec2e661-8e84-461f-936a-9f4ee2ebaefb?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="Batch 36 class 2" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "Earning analysis, Event (dividend) analysis with calanders in tradingview,Reading price structure, Channel patterns and trendlines",
        "desc": "Trends, ranges, and levels that hold",
        "topics": [
            "Higher highs, lower lows, and what a trend really requires",
            "Marking support and resistance without cluttering the chart",
            "Ranges, breakouts and failed breakouts",
            "trendlines and parallal channels",
        ],
        "embed": '<iframe src="https://veed.io/embed/d269d9ce-560e-4a50-b129-c183641b0e6d?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="batch 36 class 3" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "Deeper dive into Earnings analysis in Tradingview, News flow analysis for stock selection for swing trading",
        "desc": "",
        "topics": [
            "Earnings card analysis",
            "newsflow analysis",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/df1dcb40-d1ba-4c68-a2fa-8a44e019d45d?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="batch 36 class 4" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "Broadening wedge: A money printing pattern for long term trades",
        "desc": "",
        "topics": [
            "Everything about Broadening Wedge pattern",
            "Stocks with broadening pattern , practical examples and assignemnts",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/e8e5a5f8-5c34-441d-943f-1ae8edb66928?watermark=1&color=&sharing=1&title=1" width="744" height="504" frameborder="0" title="batch 36- class 5" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "Broadening wedge pattern (Continuation) Cup and Handle pattern",
        "desc": "",
        "topics": [
            "Practical lessons on Cup and Handle patterns",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/daa07c48-4e06-492d-9640-77c08e1b39a2?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="batch 36 class 6" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>',
    },
    {
        "title": "deep dive into Broadening wedge pattern",
        "desc": "",
        "topics": [
            "Stocks with Cup and handle pattern",
            "Complete trade plan with Broadening wedge pattern",
            "",
        ],
        "embed": '<iframe src="https://www.veed.io/embed/d8e8e28b-db85-4da7-b9d7-3385f2ffacab?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="Niyas N&#39;s Video - Sep 16, 2026" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
,
    },

  {
        "title": "pro class 1",
        "desc": "",
        "topics": [
            "",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/a38b2633-a821-4d99-8c20-ed9982d7cb6d?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="Pro batch 2 class 1 INtro" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
,
    },


   {
        "title": "pro class 2",
        "desc": "",
        "topics": [
            "",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/8f800e50-2906-4340-87db-d8df158804b3?watermark=0&color=&sharing=0&title=0" width="744" height="504" frameborder="0" title="Screen Recording - Sep 3, 2026" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
,
    },


   {
        "title": "pro class 2",
        "desc": "",
        "topics": [
            "",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/9f8e3450-57e3-42e1-9a22-63ca463855c0?watermark=0&color=&sharing=0&title=1" width="744" height="504" frameborder="0" title="pro be4 LQ" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
,
    },

  {
        "title": "pro class 2",
        "desc": "",
        "topics": [
            "",
            "",
            "",
        ],
        "embed": '<iframe src="https://veed.io/embed/07d34172-0c3e-4f07-8c2f-537c58fb8037?watermark=0&color=&sharing=0&title=1" width="744" height="504" frameborder="0" title="pro after LQ" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
,
    },

]

# Price action behind the landing-page graphic: (open, high, low, close, volume).
# A base, then a breakout above the prior high on expanding volume.
PRICE_ACTION = [
    (100, 103, 99, 102, 40), (102, 104, 100, 101, 35), (101, 102, 98, 99, 42),
    (99, 101, 97, 100, 38), (100, 102, 99, 101, 30), (101, 104, 100, 104, 55),
    (104, 105, 102, 103, 45), (103, 104, 101, 102, 36), (102, 103, 100, 102, 28),
    (102, 105, 101, 105, 62), (105, 109, 104, 108, 88), (108, 111, 107, 110, 74),
    (110, 112, 108, 109, 50), (109, 113, 109, 112, 58),
]
BREAKOUT_INDEX = 10          # candle that clears the prior high
PRIOR_HIGH = 105             # the level being broken

VIDEO_RATIO = 504 / 744      # aspect ratio of the Veed embeds
PLAYER_MAX_H = 620           # px — cap on laptops so the page still scrolls

# ─────────────────────────────────────────────────────────────────────────────
# 4. PAGE SETUP
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{BRAND_LEFT} × {BRAND_RIGHT} — Webinar Library",
    page_icon="◧",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');
:root{--bg:#070a12;--bg2:#0b1020;--panel:rgba(17,24,39,.78);--line:rgba(148,163,184,.16);--line-strong:rgba(99,102,241,.35);--ink:#f8fafc;--muted:#94a3b8;--muted2:#64748b;--brand:#7c3aed;--brand2:#4f46e5;--accent:#22d3ee;--up:#34d399;--gold:#fbbf24;--danger:#fb7185;--down:#fb7185}
.stApp{background:radial-gradient(900px 500px at 8% -5%,rgba(79,70,229,.24),transparent 60%),radial-gradient(800px 500px at 95% 8%,rgba(124,58,237,.18),transparent 62%),linear-gradient(180deg,var(--bg2) 0%,var(--bg) 62%);color:var(--ink);font-family:'DM Sans',system-ui,sans-serif;-webkit-text-size-adjust:100%}
.block-container{padding-top:1.25rem;padding-bottom:4rem;max-width:1240px;padding-left:max(1.15rem,env(safe-area-inset-left));padding-right:max(1.15rem,env(safe-area-inset-right))}
h1,h2,h3,h4{font-family:'Manrope','DM Sans',sans-serif;color:var(--ink)}p,li,label,span{color:var(--ink)}
.wordmark{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem;letter-spacing:-.02em;color:var(--ink)}.wordmark .x{color:var(--accent);font-weight:600;padding:0 .35rem}
.landing-shell{position:relative;overflow:hidden;padding:.25rem 0 0}.landing-topbar{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:2.4rem}.brand-suite{display:flex;align-items:center;gap:.7rem}.brand-card{display:flex;align-items:center;gap:.55rem;padding:.52rem .75rem;border:1px solid var(--line);background:rgba(15,23,42,.62);border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.14)}.brand-card .brand-name{font-family:'Manrope',sans-serif;font-size:.9rem;font-weight:800;letter-spacing:-.02em}.brand-divider{color:var(--muted2);font-weight:700}
.hero-badge{display:inline-flex;align-items:center;gap:.45rem;padding:.42rem .7rem;border-radius:999px;border:1px solid rgba(52,211,153,.25);background:rgba(16,185,129,.08);color:#86efac;font-size:.76rem;font-weight:700;letter-spacing:.02em}.hero-badge-dot{width:.42rem;height:.42rem;border-radius:50%;background:var(--up);box-shadow:0 0 14px rgba(52,211,153,.75)}
.hero-title{font-size:clamp(2.3rem,5vw,4.6rem);line-height:1.02;font-weight:800;letter-spacing:-.045em;margin:.95rem 0 1rem;max-width:11ch}.hero-title .gradient{background:linear-gradient(100deg,#fff 15%,#a78bfa 60%,#67e8f9 100%);-webkit-background-clip:text;background-clip:text;color:transparent}.hero-blurb{color:#b5c2d6;font-size:clamp(1rem,2.3vw,1.12rem);line-height:1.72;max-width:58ch;margin:0 0 1.35rem}.hero-meta{display:flex;flex-wrap:wrap;gap:.55rem;margin:0 0 1.5rem}.meta-chip{display:inline-flex;align-items:center;gap:.45rem;padding:.48rem .68rem;border-radius:10px;background:rgba(15,23,42,.68);border:1px solid var(--line);color:#cbd5e1;font-size:.78rem;font-weight:600}.meta-chip b{color:var(--ink)}
.hero-panel{position:relative;border:1px solid rgba(124,58,237,.28);border-radius:28px;padding:1.15rem;background:linear-gradient(145deg,rgba(17,24,39,.9),rgba(9,13,24,.72));box-shadow:0 25px 70px rgba(0,0,0,.34),inset 0 1px rgba(255,255,255,.03)}.hero-panel::before{content:"";position:absolute;inset:0;border-radius:28px;background:linear-gradient(135deg,rgba(124,58,237,.09),transparent 45%,rgba(34,211,238,.05));pointer-events:none}.panel-label{position:relative;display:flex;justify-content:space-between;align-items:center;margin:0 0 .65rem;color:#cbd5e1;font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.panel-label span:last-child{color:var(--up);font-family:'JetBrains Mono',monospace;font-size:.68rem;letter-spacing:.02em}.viz-wide,.viz-narrow{position:relative;border-radius:18px;overflow:hidden;background:rgba(2,6,23,.62);border:1px solid rgba(148,163,184,.1)}.viz-wide{display:block;padding:.8rem;min-height:330px;box-sizing:border-box}.viz-narrow{display:block;margin:0;padding:.8rem;min-height:330px;box-sizing:border-box}.chart-caption{position:relative;display:flex;justify-content:space-between;gap:.7rem;align-items:center;margin-top:.7rem;padding:0 .15rem;color:var(--muted);font-size:.75rem}.chart-caption strong{color:#e2e8f0}
.gate{border:1px solid var(--line-strong);border-radius:22px;background:linear-gradient(145deg,rgba(30,41,59,.82),rgba(15,23,42,.72));padding:1.15rem 1.2rem 1rem;margin-top:1rem;box-shadow:0 16px 45px rgba(0,0,0,.18)}.gate-head{display:flex;align-items:center;gap:.7rem;margin-bottom:.35rem}.gate-icon{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;background:linear-gradient(135deg,var(--brand2),var(--brand));font-size:.95rem}.gate-h{font-family:'Manrope',sans-serif;font-weight:800;font-size:1rem}.gate-p{color:var(--muted);font-size:.84rem;line-height:1.55;margin:.15rem 0 .8rem}.access-note{display:flex;gap:.55rem;align-items:flex-start;color:#94a3b8;font-size:.72rem;line-height:1.45;margin-top:.65rem}.access-note b{color:#cbd5e1}
.contents{margin-top:2.5rem;padding:1.35rem 0 0;border-top:1px solid var(--line)}.contents-head{display:flex;align-items:flex-end;justify-content:space-between;gap:1rem;margin-bottom:1rem}.contents h3{font-size:1.25rem;margin:0;letter-spacing:-.02em}.contents-sub{color:var(--muted);font-size:.8rem}.c-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem}.c-row{display:flex;gap:.8rem;align-items:flex-start;padding:.9rem 1rem;border:1px solid var(--line);border-radius:16px;background:rgba(15,23,42,.42);transition:transform .15s ease,border-color .15s ease,background .15s ease}.c-row:hover{transform:translateY(-2px);border-color:rgba(124,58,237,.4);background:rgba(30,41,59,.55)}.c-num{font-family:'JetBrains Mono',monospace;color:#a78bfa;font-size:.72rem;min-width:2rem;padding-top:.1rem}.c-title{font-weight:700;font-size:.9rem;line-height:1.35}.c-desc{color:var(--muted);font-size:.78rem;line-height:1.5;margin-top:.18rem}
.chapter-kicker{font-family:'JetBrains Mono',monospace;color:var(--accent);font-size:.75rem;margin-bottom:.5rem}.chapter-title{font-size:clamp(1.45rem,3.6vw,2.2rem);line-height:1.18;font-weight:800;letter-spacing:-.025em;margin:0 0 .4rem}.chapter-desc{color:var(--muted);font-size:clamp(.92rem,2.5vw,1rem);margin-bottom:1.2rem;max-width:68ch}.pending{border:1px dashed var(--line);border-radius:18px;background:rgba(15,23,42,.35);padding:2.6rem 1.4rem;text-align:center}.pending strong{font-family:'Manrope',sans-serif;font-size:1.02rem;display:block;margin-bottom:.35rem}.pending span{color:var(--muted);font-size:.9rem}.covers{margin-top:1.8rem;border-top:1px solid var(--line);padding-top:1.2rem}.covers h4{font-family:'Manrope',sans-serif;font-size:1rem;font-weight:800;margin:0 0 .7rem}.covers ul{list-style:none;padding:0;margin:0}.covers li{position:relative;padding-left:1.25rem;margin-bottom:.55rem;font-size:clamp(.92rem,2.5vw,.95rem);line-height:1.55;max-width:72ch}.covers li::before{content:"";position:absolute;left:0;top:.62em;width:.42rem;height:.42rem;background:var(--accent);border-radius:50%;box-shadow:0 0 10px rgba(34,211,238,.35)}
[data-testid="stSidebar"]{background:rgba(5,8,15,.96);border-right:1px solid var(--line)}[data-testid="stSidebar"] .block-container,[data-testid="stSidebarUserContent"]{padding-top:1.25rem}.rail-label{font-family:'Manrope',sans-serif;font-weight:800;font-size:.9rem;margin:1.25rem 0 .55rem}.rail-meta{color:var(--muted);font-size:.76rem}.rail-bar{height:4px;background:rgba(148,163,184,.12);border-radius:999px;margin:.55rem 0 .25rem;overflow:hidden}.rail-bar>div{height:4px;background:linear-gradient(90deg,var(--brand),var(--accent));border-radius:999px}.st-key-mobile_nav{display:none}
.stButton>button{font-family:'DM Sans',sans-serif;font-weight:700;font-size:.86rem;border-radius:12px;padding:.58rem .85rem;line-height:1.35;min-height:2.65rem;transition:all .15s ease}.stButton>button[kind="secondary"]{background:rgba(15,23,42,.4);color:#cbd5e1;border:1px solid transparent}.stButton>button[kind="secondary"]:hover{background:rgba(30,41,59,.8);color:#fff;border-color:var(--line)}.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--brand2),var(--brand));color:#fff;border:1px solid rgba(167,139,250,.35);box-shadow:0 10px 28px rgba(79,70,229,.22)}.stButton>button[kind="primary"]:hover{filter:brightness(1.08);transform:translateY(-1px);box-shadow:0 14px 32px rgba(79,70,229,.3)}.stButton>button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}.stTextInput>div>div>input{background:rgba(2,6,23,.7);color:var(--ink);border:1px solid var(--line);border-radius:12px;font-family:'DM Sans',sans-serif;font-size:1rem;min-height:3rem}.stTextInput>div>div>input:focus{border-color:rgba(124,58,237,.8);box-shadow:0 0 0 3px rgba(124,58,237,.12)}[data-testid="stForm"]{border:0;padding:0}[data-testid="stExpander"]{border:1px solid var(--line);border-radius:14px;background:rgba(15,23,42,.4)}[data-testid="stAlert"]{border-radius:12px}footer,#MainMenu{visibility:hidden}
@media (min-width:641px){[data-testid="stSidebar"]{min-width:288px;max-width:322px}}@media (max-width:860px){.hero-title{max-width:14ch}.c-grid{grid-template-columns:1fr}}@media (max-width:640px){.viz-wide{display:none}.viz-narrow{display:block;min-height:0;padding:.55rem}.block-container{padding-top:1rem;padding-bottom:2.6rem}.landing-topbar{margin-bottom:1.4rem}.brand-card{padding:.45rem .6rem}.hero-badge{font-size:.68rem}.hero-title{font-size:clamp(2.1rem,12vw,3.25rem);max-width:100%;margin:.7rem 0 .8rem}.hero-blurb{font-size:.95rem;margin-bottom:1rem}.hero-meta{gap:.4rem}.meta-chip{font-size:.7rem;padding:.42rem .55rem}.hero-panel{padding:.7rem;border-radius:20px}.hero-panel::before{border-radius:20px}.viz-wide{display:none}.viz-narrow{display:block}.gate{padding:1rem;border-radius:18px}.contents{margin-top:2rem}.contents-head{display:block}.contents-sub{margin-top:.3rem}.c-grid{grid-template-columns:1fr}.c-row{padding:.8rem .85rem}.c-num{min-width:1.8rem}.c-title{font-size:.86rem}.c-desc{font-size:.74rem}.st-key-mobile_nav{display:block;margin-bottom:1rem}.stButton>button{min-height:2.9rem;font-size:.9rem}.host{margin-top:1.35rem}}@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)
# Enhanced NYZTrade / Finzcom brand layer — visual-only; app logic remains unchanged.
BRAND_CSS = r"""
<style>
:root{--nyz-indigo:#4f46e5;--nyz-purple:#7c3aed;--nyz-cyan:#22d3ee}
.brand-suite{gap:.6rem!important}.brand-card{position:relative!important;padding:.62rem .9rem!important;border:1px solid rgba(124,58,237,.32)!important;background:linear-gradient(145deg,rgba(22,27,49,.92),rgba(10,14,27,.78))!important;border-radius:16px!important;box-shadow:0 10px 35px rgba(79,70,229,.12),inset 0 1px rgba(255,255,255,.04)!important}.brand-card.nyz{border-color:rgba(34,211,238,.3)!important}.brand-mark{width:38px;height:38px;display:grid;place-items:center;border-radius:11px;background:linear-gradient(135deg,var(--nyz-indigo),var(--nyz-purple));box-shadow:0 8px 20px rgba(79,70,229,.28)}.brand-card .brand-name{font-size:.98rem!important}.brand-card .brand-sub{display:block;color:#8fa0b6;font-size:.61rem;line-height:1.1;margin-top:.12rem;letter-spacing:.035em;text-transform:uppercase}.brand-divider{font-size:1rem!important;color:#64748b!important}.top-brandline{display:flex;align-items:center;gap:.65rem;color:#94a3b8;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.hero-brand-kicker{display:flex;align-items:center;gap:.65rem;margin:0 0 .8rem;color:#c4b5fd;font-size:.72rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.hero-brand-kicker .pulse{width:8px;height:8px;border-radius:50%;background:var(--nyz-cyan);box-shadow:0 0 16px rgba(34,211,238,.8)}.hero-title{font-size:clamp(2.5rem,5.2vw,4.9rem)!important;max-width:12ch!important}.hero-title .brand-gradient{background:linear-gradient(100deg,#fff 8%,#c4b5fd 48%,#67e8f9 100%);-webkit-background-clip:text;background-clip:text;color:transparent}.brand-positioning{font-family:'Manrope',sans-serif;font-weight:800;font-size:clamp(.95rem,2vw,1.18rem);color:#e2e8f0;margin:-.25rem 0 1rem;letter-spacing:-.02em}.brand-positioning span{color:#67e8f9}.brand-trust{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1.25rem}.brand-trust span{display:inline-flex;align-items:center;gap:.4rem;padding:.43rem .65rem;border-radius:999px;border:1px solid rgba(124,58,237,.25);background:rgba(79,70,229,.08);color:#cbd5e1;font-size:.72rem;font-weight:700}.brand-trust i{font-style:normal;color:#67e8f9}.brand-signature{margin-top:1.15rem;padding-top:.9rem;border-top:1px solid var(--line);display:flex;align-items:center;gap:.7rem}.brand-signature-mark{width:30px;height:30px;border-radius:9px;background:linear-gradient(135deg,var(--nyz-indigo),var(--nyz-purple));display:grid;place-items:center;color:white;font-family:'Manrope';font-size:.8rem;font-weight:800}.brand-signature strong{display:block;font-family:'Manrope';font-size:.82rem}.brand-signature small{display:block;color:#718096;font-size:.67rem;margin-top:.12rem}.brand-ribbon{position:relative;display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:1.35rem 0 0;padding:.8rem 1rem;border-radius:16px;border:1px solid rgba(34,211,238,.18);background:linear-gradient(90deg,rgba(79,70,229,.12),rgba(34,211,238,.055));overflow:hidden}.brand-ribbon:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--nyz-purple),var(--nyz-cyan))}.brand-ribbon b{font-size:.76rem;color:#f1f5f9}.brand-ribbon span{font-size:.68rem;color:#94a3b8;text-align:right}.hero-panel.brand-panel{border-color:rgba(124,58,237,.35)!important}.brand-panel .panel-label span:first-child{color:#e9d5ff}.brand-panel .panel-label span:last-child{color:#67e8f9!important}@media(max-width:640px){.top-brandline{display:none}.brand-card{padding:.5rem .65rem!important}.brand-mark{width:33px;height:33px}.brand-card .brand-name{font-size:.87rem!important}.brand-card .brand-sub{font-size:.54rem}.brand-divider{display:none}.hero-brand-kicker{font-size:.65rem}.brand-positioning{font-size:.92rem}.brand-trust span{font-size:.66rem}.brand-ribbon{display:block}.brand-ribbon span{display:block;text-align:left;margin-top:.25rem}}
</style>
"""
FINAL_HERO_CSS = r'''
<style>
/* ── NYZTrade hero: one chart, right-aligned, responsive ───────────────── */
.hero-copy{padding-top:.15rem}
.hero-chart-card{
  position:relative;
  height:100%;
  min-height:420px;
  box-sizing:border-box;
  padding:1.15rem;
  border:1px solid rgba(124,58,237,.38);
  border-radius:28px;
  background:
    radial-gradient(circle at 80% 10%,rgba(34,211,238,.07),transparent 32%),
    linear-gradient(145deg,rgba(20,27,45,.96),rgba(7,12,23,.92));
  box-shadow:0 25px 70px rgba(0,0,0,.34),inset 0 1px rgba(255,255,255,.04);
  overflow:hidden;
}
.hero-chart-card:before{
  content:"";
  position:absolute;inset:0;border-radius:28px;pointer-events:none;
  background:linear-gradient(135deg,rgba(124,58,237,.10),transparent 42%,rgba(34,211,238,.06));
}
.hero-chart{
  position:relative;
  width:100%;
  min-height:300px;
  display:flex;
  align-items:center;
  justify-content:center;
  border:1px solid rgba(148,163,184,.10);
  border-radius:19px;
  background:rgba(2,6,23,.72);
  padding:.65rem;
  box-sizing:border-box;
  overflow:hidden;
}
.hero-chart svg{display:block;width:100%!important;height:auto!important;max-width:100%;min-width:0!important}
.hero-chart-card > .hero-chart{margin:0!important}
.hero-chart-card .panel-label,.hero-chart-card .chart-caption,.hero-chart-card .chart-brand-note{position:relative;z-index:1}
.chart-brand-note{
  position:relative;
  display:flex;
  align-items:center;
  gap:.15rem;
  margin-top:.8rem;
  padding:.68rem .75rem;
  border-radius:13px;
  border:1px solid rgba(34,211,238,.14);
  background:rgba(34,211,238,.035);
  color:#91a4bb;
  font-size:.72rem;
}
.chart-brand-note b{color:#e2e8f0}
.chart-brand-dot{
  width:7px;height:7px;border-radius:50%;
  background:#22d3ee;box-shadow:0 0 14px rgba(34,211,238,.8);
  margin-right:.35rem;flex:0 0 auto;
}
.hero-access-wrap{margin-top:1.25rem}
.hero-access-wrap .gate{margin-top:0}
@media (min-width:861px){
  .hero-copy{min-height:420px;display:flex;flex-direction:column;justify-content:center}
  .hero-chart-card{min-height:0}
  .hero-chart{min-height:0}
  .hero-chart svg{max-height:360px}
}
@media (max-width:860px){
  .hero-copy{min-height:0}
  .hero-chart-card{min-height:0;margin-top:.25rem}
  .hero-chart{min-height:260px}
  .hero-chart svg{max-height:330px}
}
@media (max-width:640px){
  .landing-shell{padding-left:0;padding-right:0}
  .landing-topbar{align-items:flex-start}
  .brand-suite{max-width:100%;flex-wrap:wrap}
  .hero-copy{padding-top:0}
  .hero-brand-kicker{line-height:1.5;margin-bottom:.65rem}
  .hero-title{font-size:clamp(2.35rem,12vw,3.5rem)!important;line-height:.98!important}
  .hero-blurb{line-height:1.6}
  .hero-trust,.brand-trust{margin-bottom:1rem}
  .hero-chart-card{padding:.8rem;border-radius:20px;margin-top:.15rem}
  .hero-chart-card:before{border-radius:20px}
  .hero-chart{min-height:0;padding:.35rem;border-radius:15px}
  .hero-chart svg{min-width:0!important;max-height:none!important}
  .chart-caption{font-size:.68rem}
  .chart-brand-note{font-size:.67rem;line-height:1.45}
  .hero-access-wrap{margin-top:1rem}
}
/* Streamlit's column gap can become excessive on small screens */
@media (max-width:640px){
  div[data-testid="stHorizontalBlock"]{gap:.9rem!important}
  .landing-shell div[data-testid="stHorizontalBlock"]{flex-wrap:wrap!important}
  .landing-shell div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{width:100%!important;flex:1 1 100%!important;min-width:100%!important}
  .hero-chart-card{width:100%;box-sizing:border-box}
  .hero-chart-card .panel-label{font-size:.67rem}
  .hero-chart-card .panel-label span:last-child{white-space:nowrap}
}
</style>
'''
st.markdown(BRAND_CSS, unsafe_allow_html=True)

st.markdown(FINAL_HERO_CSS, unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────────────────────────
# 5. HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def expected_password() -> str:
    """Password from secrets, then environment, then the constant above."""
    try:
        value = st.secrets["APP_PASSWORD"]
        if value:
            return str(value)
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD", DEFAULT_PASSWORD)


def wordmark() -> str:
    return f'<div class="wordmark">{BRAND_LEFT}<span class="x">×</span>{BRAND_RIGHT}</div>'


def price_chart_svg(compact: bool = False) -> str:
    """
    Candles and volume: a base, then a breakout through the prior high.
    The landing page's one bold element — and the thing the series is about.
    """
    if compact:
        candles = PRICE_ACTION[-8:]
        breakout = BREAKOUT_INDEX - (len(PRICE_ACTION) - 8)
        vb_w, pad_l, pad_r = 392, 20, 20
        price_top, price_h, vol_h, gap = 26, 168, 40, 16
        fs = 12
    else:
        candles = PRICE_ACTION
        breakout = BREAKOUT_INDEX
        vb_w, pad_l, pad_r = 620, 26, 26
        price_top, price_h, vol_h, gap = 24, 214, 52, 18
        fs = 11.5

    lo = min(c[2] for c in candles)
    hi = max(c[1] for c in candles)
    span = (hi - lo) or 1
    vol_top = price_top + price_h + gap
    height = vol_top + vol_h + 20
    slot = (vb_w - pad_l - pad_r) / len(candles)
    body_w = slot * 0.52
    max_vol = max(c[4] for c in candles)

    def y_of(price: float) -> float:
        return price_top + (hi - price) / span * price_h

    marks = []
    for i, (o, h, l, c, v) in enumerate(candles):
        cx = pad_l + slot * (i + 0.5)
        rising = c >= o
        colour = "#00C853" if rising else "#FF5252"
        strong = i == breakout
        opacity = "1" if strong else ".62"
        top_y, bot_y = y_of(max(o, c)), y_of(min(o, c))
        marks.append(
            f'<line x1="{cx:.1f}" y1="{y_of(h):.1f}" x2="{cx:.1f}" y2="{y_of(l):.1f}" '
            f'stroke="{colour}" stroke-width="1.2" opacity="{opacity}"/>'
            f'<rect x="{cx - body_w / 2:.1f}" y="{top_y:.1f}" width="{body_w:.1f}" '
            f'height="{max(bot_y - top_y, 2):.1f}" fill="{colour}" opacity="{opacity}" rx="1"/>'
        )
        vh = v / max_vol * vol_h
        marks.append(
            f'<rect x="{cx - body_w / 2:.1f}" y="{vol_top + vol_h - vh:.1f}" '
            f'width="{body_w:.1f}" height="{vh:.1f}" fill="{colour}" '
            f'opacity="{".85" if strong else ".28"}" rx="1"/>'
        )

    level_y = y_of(PRIOR_HIGH)
    breakout_x = pad_l + slot * (breakout + 0.5)
    return f"""
<svg viewBox="0 0 {vb_w} {height}" width="100%" role="img"
     aria-label="A price chart: several sessions building a base, then a breakout above the prior high on rising volume.">
  <line x1="{pad_l}" y1="{level_y:.1f}" x2="{vb_w - pad_r}" y2="{level_y:.1f}"
        stroke="#7A8A99" stroke-width="1" stroke-dasharray="3 4"/>
  <text x="{pad_l}" y="{level_y - 8:.1f}" font-family="IBM Plex Sans, sans-serif"
        font-size="{fs}" fill="#7A8A99">prior high</text>
  <text x="{breakout_x:.1f}" y="{vol_top + vol_h + 15:.1f}" text-anchor="middle"
        font-family="IBM Plex Sans, sans-serif" font-size="{fs}" fill="#D97706">breakout on volume</text>
  <line x1="{pad_l}" y1="{vol_top + vol_h:.1f}" x2="{vb_w - pad_r}" y2="{vol_top + vol_h:.1f}"
        stroke="#8A98A8" stroke-width="1"/>
  {''.join(marks)}
</svg>
"""


def player_html(src: str, tag: str) -> str:
    """
    Rebuild the pasted Veed iframe so it tracks the column width instead of the
    fixed 744x504, and repair the fullscreen permission chain.

    The video sits two iframes deep: page -> Streamlit component frame -> Veed
    player. Fullscreen has to be granted at every level, and Streamlit sets the
    modern `allow` attribute but never the legacy `allowfullscreen` one, so the
    player can read fullscreen as unavailable and its button does nothing. The
    script below re-asserts both attributes on the component frame on every
    render, and the bar underneath gives a fullscreen control of our own that
    does not depend on the player at all.
    """
    return f"""
<style>
  html,body{{margin:0;padding:0;background:transparent;overflow:hidden;}}
  .stage{{
    width:100%;aspect-ratio:744/504;max-height:100vh;
    border:1px solid rgba(242,233,220,.16);border-radius:4px;
    overflow:hidden;background:#0a1d27;
  }}
  .stage iframe{{width:100%;height:100%;border:0;display:block;}}
  .stage:fullscreen,.stage:-webkit-full-screen{{
    width:100vw;height:100vh;max-height:none;aspect-ratio:auto;border:0;border-radius:0;
  }}
  .bar{{
    display:flex;gap:1.1rem;align-items:center;justify-content:flex-end;
    height:30px;font:500 13px/1 'IBM Plex Sans',system-ui,sans-serif;
  }}
  .bar button,.bar a{{
    background:none;border:0;padding:.35rem .1rem;cursor:pointer;
    color:#a9bfc9;font:inherit;text-decoration:none;
  }}
  .bar button:hover,.bar a:hover{{color:#e8a33d;}}
  .bar button:focus-visible,.bar a:focus-visible{{outline:2px solid #e8a33d;outline-offset:2px;}}
  .stage:fullscreen + .bar{{display:none;}}
</style>
<div class="stage" id="stage-{tag}">
  <iframe src="{src}" allow="autoplay; fullscreen; picture-in-picture; encrypted-media"
          allowfullscreen webkitallowfullscreen mozallowfullscreen
          title="Session recording"></iframe>
</div>
<div class="bar">
  <button type="button" id="fs-{tag}">⤢ Full screen</button>
  <a href="{src}" target="_blank" rel="noopener">Open in a new tab ↗</a>
</div>
<script>
  (function(){{
    var frame = window.frameElement;
    var stage = document.getElementById('stage-{tag}');
    var BAR = 30, lastW = -1, lastH = -1;

    // 1. hand fullscreen down through the Streamlit component frame.
    //    Only write an attribute when it is actually missing — writing
    //    unconditionally (or watching for mutations) feeds back into itself.
    function grantFullscreen(){{
      if (!frame) return;
      try {{
        if (!frame.hasAttribute('allowfullscreen')) frame.setAttribute('allowfullscreen', '');
        if (!frame.hasAttribute('webkitallowfullscreen')) frame.setAttribute('webkitallowfullscreen', '');
        if (!frame.hasAttribute('mozallowfullscreen')) frame.setAttribute('mozallowfullscreen', '');
        frame.allowFullscreen = true;
        var allow = frame.getAttribute('allow') || '';
        if (allow.indexOf('fullscreen') === -1) {{
          frame.setAttribute('allow', (allow ? allow + '; ' : '') + 'fullscreen');
        }}
      }} catch (e) {{}}
    }}
    grantFullscreen();
    // re-check a few times, in case Streamlit re-renders the frame just after
    // this script runs, then stop
    var tries = 0;
    var recheck = setInterval(function(){{
      grantFullscreen();
      if (++tries >= 5) clearInterval(recheck);
    }}, 400);

    // 2. our own fullscreen control, independent of the player's own button
    var btn = document.getElementById('fs-{tag}');
    btn.addEventListener('click', function(){{
      var req = stage.requestFullscreen || stage.webkitRequestFullscreen || stage.msRequestFullscreen;
      if (!req) {{ window.open('{src}', '_blank', 'noopener'); return; }}
      var out = req.call(stage);
      if (out && out.catch) {{
        out.catch(function(){{ window.open('{src}', '_blank', 'noopener'); }});
      }}
    }});

    // 3. size the frame to the column — no-ops unless the width really changed,
    //    so the resize observer cannot chase its own writes
    function fit(force){{
      if (!frame || document.fullscreenElement) return;
      var w = document.documentElement.clientWidth;
      if (!force && w === lastW) return;
      lastW = w;
      var h = Math.min(Math.round(w * {VIDEO_RATIO}) + 2, {PLAYER_MAX_H}) + BAR;
      if (h === lastH) return;
      lastH = h;
      frame.style.height = h + 'px';
      frame.setAttribute('height', h);
      if (frame.parentElement) frame.parentElement.style.height = h + 'px';
    }}
    fit(true);

    var pending = false;
    function schedule(){{
      if (pending) return;
      pending = true;
      requestAnimationFrame(function(){{ pending = false; fit(false); }});
    }}
    window.addEventListener('resize', schedule);
    window.addEventListener('orientationchange', schedule);
    document.addEventListener('fullscreenchange', function(){{ fit(true); }});
  }})();
  </script>
"""


def render_player(session: dict, idx: int) -> None:
    """Play the recording, or show an honest empty state if none is set yet."""
    raw = (session.get("embed") or "").strip()
    # tolerate a full paste (iframe + Veed's footer link) or a bare embed URL
    match = re.search(r'<iframe[^>]*\ssrc="([^"]+)"', raw) or re.search(r'src="([^"]+)"', raw)
    src = match.group(1) if match else (raw if raw.startswith("http") else "")
    if src:
        # keying the container on the session forces Streamlit to build a fresh
        # iframe per video instead of reusing one that has gone stale
        with st.container(key=f"player_{idx}"):
            components.html(
                player_html(src, str(idx)), height=PLAYER_MAX_H + 30, scrolling=False
            )
    else:
        st.markdown(
            '<div class="pending"><strong>Recording is not up yet</strong>'
            '<span>It will appear here as soon as the session is uploaded.</span></div>',
            unsafe_allow_html=True,
        )


def go_to(index: int) -> None:
    st.session_state.chapter = index


# ─────────────────────────────────────────────────────────────────────────────
# 6. LANDING PAGE
# ─────────────────────────────────────────────────────────────────────────────
def landing() -> None:
    """Premium branded landing page. Authentication and webinar library remain unchanged."""
    st.markdown('<div class="landing-shell">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="landing-topbar">
      <div class="brand-suite">
        <div class="brand-card">
          <div class="brand-mark" aria-label="Finzcom logo">
            <svg width="25" height="25" viewBox="0 0 32 32" aria-hidden="true">
              <path d="M7 23V8h15v4H12v3h8v4h-8v4H7z" fill="white"/>
              <path d="M23 20.5l3-3 3 3-3 3-3-3z" fill="#67e8f9"/>
            </svg>
          </div>
          <div><span class="brand-name">Finzcom</span><span class="brand-sub">Finance • Commerce</span></div>
        </div>
        <span class="brand-divider">×</span>
        <div class="brand-card nyz">
          <div class="brand-mark" aria-label="NYZTrade logo">
            <svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">
              <path d="M6 23V9h4l7 8V9h4v14h-4l-7-8v8H6z" fill="white"/>
              <path d="M24 23V9h3v14h-3z" fill="#67e8f9"/>
            </svg>
          </div>
          <div><span class="brand-name">NYZTrade</span><span class="brand-sub">Financial Solutions</span></div>
        </div>
      </div>
      <div class="top-brandline">PRIVATE • NYZTRADE LEARNING HUB</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero: copy left / ONE chart right on desktop; stacks cleanly on mobile.
    hero_left, hero_right = st.columns([1.08, 0.92], gap="large")

    with hero_left:
        st.markdown(f"""
        <div class="hero-copy">
          <div class="hero-brand-kicker"><span class="pulse"></span>
            NYZTRADE FINANCIAL SOLUTIONS · EQUITY MARKET EDUCATION
          </div>
          <h1 class="hero-title">Professional trading strategies for <span class="brand-gradient">trading in Indian equities</span></h1>
          <div class="brand-positioning">
            Research-backed thinking. <span>Chart-based execution.</span> Practical risk management.
          </div>
          <p class="hero-blurb">{SERIES_BLURB}</p>
          <div class="brand-trust">
            <span><i>◆</i> NYZTrade Research Framework</span>
            <span><i>↗</i> Real-market chart work</span>
            <span><i>✓</i> Practical &amp; structured</span>
          </div>
          <div class="hero-meta">
            <span class="meta-chip">◈ <b>{len(WEBINAR_SESSIONS)} recorded sessions</b></span>
            <span class="meta-chip">↗ Real-chart examples</span>
            <span class="meta-chip">◷ Learn at your pace</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        # Use a dedicated HTML component for the chart card. Streamlit's
        # Markdown renderer can treat nested SVG/HTML as a Markdown block and
        # expose trailing tags as visible text. components.html() gives the
        # chart its own valid HTML document, eliminating HTML leakage.
        chart_svg = price_chart_svg()
        chart_html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  *{{box-sizing:border-box}}
  html,body{{margin:0;padding:0;background:transparent;overflow:hidden}}
  body{{font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#e2e8f0}}
  .chart-card{{
    width:100%;height:100%;min-height:430px;padding:18px;
    border:1px solid rgba(124,58,237,.42);border-radius:28px;
    background:radial-gradient(circle at 82% 8%,rgba(34,211,238,.08),transparent 32%),
               linear-gradient(145deg,rgba(20,27,45,.98),rgba(7,12,23,.96));
    box-shadow:0 25px 70px rgba(0,0,0,.34),inset 0 1px rgba(255,255,255,.04);
    overflow:hidden;
  }}
  .panel-label{{display:flex;justify-content:space-between;align-items:center;gap:12px;
    margin:0 2px 12px;font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}}
  .panel-label span:last-child{{color:#22d3ee;white-space:nowrap}}
  .hero-chart{{width:100%;border:1px solid rgba(148,163,184,.10);border-radius:19px;
    background:rgba(2,6,23,.78);padding:10px;overflow:hidden}}
  .hero-chart svg{{display:block;width:100%;height:auto;max-width:100%}}
  .chart-caption{{display:flex;justify-content:space-between;gap:12px;margin-top:12px;
    font-size:12px;color:#91a4bb}}
  .chart-caption strong{{color:#e2e8f0}}
  .chart-brand-note{{display:flex;align-items:center;gap:6px;margin-top:12px;padding:10px 12px;
    border:1px solid rgba(34,211,238,.14);border-radius:13px;background:rgba(34,211,238,.035);
    color:#91a4bb;font-size:11px;line-height:1.4}}
  .chart-brand-note b{{color:#e2e8f0}}
  .chart-brand-dot{{width:7px;height:7px;flex:0 0 7px;border-radius:50%;background:#22d3ee;
    box-shadow:0 0 14px rgba(34,211,238,.8)}}
  @media(max-width:640px){{
    .chart-card{{min-height:0;padding:12px;border-radius:20px}}
    .panel-label{{font-size:10px;margin-bottom:8px}}
    .hero-chart{{padding:5px;border-radius:15px}}
    .chart-caption{{font-size:10px;margin-top:8px}}
    .chart-brand-note{{font-size:9px;margin-top:8px;padding:8px 9px}}
  }}
</style>
</head>
<body>
  <div class="chart-card">
    <div class="panel-label">
      <span>NYZTRADE MARKET FRAMEWORK</span>
      <span>PRICE + VOLUME</span>
    </div>
    <div class="hero-chart">
      {chart_svg}
    </div>
    <div class="chart-caption">
      <span><strong>Base → breakout with participation</strong></span>
      <span>Illustrative</span>
    </div>
    <div class="chart-brand-note">
      <span class="chart-brand-dot"></span>
      <b>NYZTrade</b>&nbsp; • &nbsp;Learn the process. Apply it on your own charts.
    </div>
  </div>
</body>
</html>
"""
        components.html(chart_html, height=500, scrolling=False)

    st.markdown('<div class="hero-access-wrap">', unsafe_allow_html=True)
    st.markdown("""
      <div class="gate">
        <div class="gate-head">
          <div class="gate-icon">🔐</div>
          <div class="gate-h">Enter your NYZTrade access password</div>
        </div>
        <div class="gate-p">This is a private learning library for participants. No account or email required — use the password shared by the host.</div>
      </div>
    """, unsafe_allow_html=True)

    with st.form("gate", clear_on_submit=False):
        entry = st.text_input(
            "Access password",
            type="password",
            placeholder="Enter your private access password",
            label_visibility="collapsed",
        )
        unlocked = st.form_submit_button(
            "Unlock NYZTrade Learning Hub  →",
            type="primary",
            use_container_width=True,
        )

    if unlocked:
        if entry and entry.strip() == expected_password():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("That password doesn't match. Check the message from the host and try again.")

    st.markdown(
        '<div class="access-note"><span>●</span><span><b>Private participant access:</b> recordings become available after successful authentication.</span></div>'
        f'<div class="brand-signature"><div class="brand-signature-mark">NZ</div><div><strong>NYZTrade Financial Solutions</strong><small>{HOST_LINE}</small></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    rows = "".join(
        f'<div class="c-row"><div class="c-num">{i + 1:02d}</div>'
        f'<div><div class="c-title">{s["title"]}</div><div class="c-desc">{s["desc"]}</div></div></div>'
        for i, s in enumerate(WEBINAR_SESSIONS)
    )
    st.markdown(
        f'<div class="contents">'
        f'<div class="contents-head"><div><h3>NYZTrade Learning Hub</h3>'
        f'<div class="contents-sub">A progressive sequence from market mechanics to trade review — delivered through the Finzcom × NYZTrade learning series.</div></div>'
        f'<div class="hero-badge">{len(WEBINAR_SESSIONS)} SESSIONS</div></div>'
        f'<div class="c-grid">{rows}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 7. LIBRARY
# ─────────────────────────────────────────────────────────────────────────────
def session_buttons(idx: int, key_prefix: str) -> None:
    for i, s in enumerate(WEBINAR_SESSIONS):
        st.button(
            f"{i + 1:02d}   {s['title']}",
            key=f"{key_prefix}_{i}",
            type="primary" if i == idx else "secondary",
            use_container_width=True,
            on_click=go_to,
            args=(i,),
        )


def library() -> None:
    total = len(WEBINAR_SESSIONS)
    idx = min(st.session_state.get("chapter", 0), total - 1)
    session = WEBINAR_SESSIONS[idx]
    pct = int((idx + 1) / total * 100)

    # laptop: persistent left rail
    with st.sidebar:
        st.markdown(wordmark(), unsafe_allow_html=True)
        st.markdown('<div class="rail-label">Sessions</div>', unsafe_allow_html=True)
        session_buttons(idx, "nav")
        st.markdown(
            f'<div class="rail-bar"><div style="width:{pct}%"></div></div>'
            f'<div class="rail-meta">Session {idx + 1} of {total}</div>'
            '<div style="height:1.1rem"></div>',
            unsafe_allow_html=True,
        )
        if st.button("Lock the library", key="lock", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # phone: the same list, collapsed into the page (CSS hides it on laptops)
    with st.container(key="mobile_nav"):
        with st.expander(f"Sessions · {idx + 1} of {total}", expanded=False):
            session_buttons(idx, "mnav")

    st.markdown(
        f'<div class="chapter-kicker">Session {idx + 1:02d} / {total:02d}</div>'
        f'<h1 class="chapter-title">{session["title"]}</h1>'
        f'<p class="chapter-desc">{session["desc"]}</p>',
        unsafe_allow_html=True,
    )

    render_player(session, idx)

    prev_col, next_col = st.columns(2)
    with prev_col:
        st.button(
            "← Previous session", key="prev", disabled=idx == 0,
            use_container_width=True, on_click=go_to, args=(idx - 1,),
        )
    with next_col:
        st.button(
            "Next session →", key="next", disabled=idx == total - 1,
            use_container_width=True, on_click=go_to, args=(idx + 1,),
        )

    topics = [t.strip() for t in (session.get("topics") or []) if t.strip()]
    if topics:
        items = "".join(f"<li>{t}</li>" for t in topics)
        st.markdown(
            f'<div class="covers"><h4>What this session covers</h4><ul>{items}</ul></div>',
            unsafe_allow_html=True,
        )

    st.markdown(f'<div class="host">{HOST_LINE}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 8. ROUTER
# ─────────────────────────────────────────────────────────────────────────────
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("chapter", 0)

if st.session_state.authenticated:
    library()
else:
    landing()
