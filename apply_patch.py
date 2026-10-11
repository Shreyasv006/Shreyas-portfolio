#!/usr/bin/env python3
"""
Adds "Awards & Recognition" + "Academic Achievements & Additional Training"
to Shreyas-portfolio/index.html (single-file site).

Usage (from the repo folder):   python apply_patch.py
Creates index.html.bak first. Safe to re-run: it refuses if already applied.
"""
import sys, shutil, pathlib

p = pathlib.Path('index.html')
if not p.exists():
    sys.exit('index.html not found - run this inside the repo folder.')
with open('index.html', encoding='utf-8', newline='') as f:
    s = f.read()
if 'id="recognition"' in s:
    sys.exit('Already applied (found id="recognition"). Nothing to do.')

CSS = r'''
/* ===== AWARDS & TRAINING ===== */
@media(max-width:960px){.links{display:none}.menu-btn{display:block}}
.rec-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(28px,4vw,64px);margin-top:56px;align-items:start}
.rec-col>h3{font-family:var(--mono);font-size:13px;font-weight:500;letter-spacing:.02em;color:var(--mute);margin-bottom:18px;display:flex;align-items:center;gap:10px}
.rec-col>h3::after{content:"";flex:1;height:1px;background:var(--line)}
.rcard{position:relative;background:var(--card);border-radius:24px;padding:24px 26px;margin-bottom:14px;box-shadow:inset 0 0 0 1px var(--line),0 20px 40px -34px rgba(0,0,0,.3);transition:transform .6s var(--ease),box-shadow .6s var(--ease)}
.rcard:hover{transform:translateY(-3px);box-shadow:inset 0 0 0 1px var(--line),0 30px 50px -30px rgba(109,94,252,.5)}
.rcard.hl{background:linear-gradient(var(--card),var(--card)) padding-box,var(--grad) border-box;border:1.5px solid transparent}
.rcard .rt{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;font-family:var(--mono);font-size:12px;color:var(--mute)}
.rcard .rt b{font-weight:500;color:var(--ink-2)}
.rcard .rt .new{background:var(--grad);color:#fff;border-radius:999px;padding:3px 10px;font-size:11px;letter-spacing:.02em}
.rcard h4{margin:10px 0 8px;font-size:clamp(18px,1.7vw,23px);font-weight:700;letter-spacing:-.03em;line-height:1.2}
.rcard p{font-size:14px;color:var(--ink-2);line-height:1.55}
.rcard .meta{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px}
.rcard .meta span{font-size:12px;font-weight:600;padding:5px 12px;border-radius:999px;box-shadow:inset 0 0 0 1px var(--line);color:var(--ink-2)}
.rcard .stack{margin-top:12px;display:flex;flex-wrap:wrap;gap:6px}
.rcard .stack span{font-family:var(--mono);font-size:11px;padding:4px 10px;border-radius:999px;background:var(--paper);box-shadow:inset 0 0 0 1px var(--line);color:var(--ink-2)}
@media(max-width:900px){.rec-grid{grid-template-columns:1fr}}
'''

SECTION = r'''<!-- RECOGNITION & TRAINING -->
<section class="sec" id="recognition">
<div class="wrap">
<p class="tag rv">06 — Recognition &amp; training</p>
<h2 class="rv-mask"><span>Awards &amp; <em>learning.</em></span></h2>
<div class="rec-grid">
<div class="rec-col">
<h3>Awards &amp; recognition</h3>
<article class="rcard hl rv" style="--i:0"><div class="rt"><span class="new">Latest</span><b>TCS Gems</b><span>6 October 2026</span></div><h4>On the Spot Award</h4><p>Recognized for outstanding contribution and acknowledged as an inspiring role model to colleagues.</p></article>
<article class="rcard rv" style="--i:1"><div class="rt"><b>TCS OP Pohjola</b><span>Azure Managed Services</span></div><h4>Technical Excellence Award</h4><p>Received team/project recognition for technical excellence and contribution to Azure Managed Services.</p></article>
<article class="rcard rv" style="--i:2"><div class="rt"><b>TCS</b></div><h4>Certificate of Recognition</h4><p>Recognized by TCS Leadership and OP Leadership for outstanding contribution to Azure MS.</p></article>
</div>
<div class="rec-col">
<h3>Academic achievements &amp; additional training</h3>
<article class="rcard rv" style="--i:0"><div class="rt"><b>IIT Kharagpur / SWAYAM</b><span>Jul–Sep 2023</span></div><h4>NPTEL Elite Certification — Database Management System</h4><div class="meta"><span>Consolidated score: 69%</span></div></article>
<article class="rcard rv" style="--i:1"><div class="rt"><b>IIT Kharagpur / SWAYAM</b><span>Jan–Apr 2024</span></div><h4>NPTEL Online Certification — Programming in Java</h4><div class="meta"><span>Consolidated score: 57%</span></div></article>
<article class="rcard rv" style="--i:2"><div class="rt"><b>NCICT ’24</b><span>8–9 March 2024</span></div><h4>Technical Paper Presentation</h4><p>Presented “Home Automation Utilizing NodeMCU with IoT Integration” at the National Conference on Innovative Computing Techniques, Dr. M.G.R. Educational and Research Institute, Chennai.</p></article>
<article class="rcard rv" style="--i:3"><div class="rt"><b>Capgemini / TNS India Foundation</b><span>2023–2024</span></div><h4>Campus to Technical Careers Training Program</h4><p>Completed training in:</p><div class="stack"><span>SQL</span><span>Core Java 8</span><span>JPA with Hibernate</span><span>Git</span><span>Spring 5.0</span><span>Spring Boot</span><span>HTML5</span><span>CSS3</span><span>JavaScript</span><span>TypeScript</span><span>Angular 7</span><span>Soft skills</span></div></article>
</div>
</div>
</div>
</section>

'''

# (anchor, replacement) - every anchor must appear exactly once
EDITS = [
 ('</style>', CSS + '</style>'),
 # top nav
 ('<a href="#achievements">Achievements</a><a href="#contact">Contact</a>',
  '<a href="#achievements">Achievements</a><a href="#recognition">Awards</a><a href="#contact">Contact</a>'),
 # mobile overlay menu
 ('<a href="#contact" style="--i:5"><small>06</small>Contact</a>',
  '<a href="#recognition" style="--i:5"><small>06</small>Awards</a>\n<a href="#contact" style="--i:6"><small>07</small>Contact</a>'),
 # new section before contact + renumber contact tag
 ('<!-- CONTACT -->', SECTION + '<!-- CONTACT -->'),
 ('<p class="tag rv">06 — Contact</p>', '<p class="tag rv">07 — Contact</p>'),
 # Ctrl/Cmd+K quick-jump palette
 ("['Achievements','section',go('achievements')],['Contact','section',go('contact')],",
  "['Achievements','section',go('achievements')],['Awards & training','section',go('recognition')],['Contact','section',go('contact')],"),
 # achievements carousel: add an awards card
 ("{l:'Years at TCS',c:'Since April 2025 as DevOps & Database Engineer.',n:1.7,d:1,s:'+',g:'Yr'}];",
  "{l:'TCS awards',c:'On the Spot, Technical Excellence and Certificate of Recognition.',n:3,g:'Aw'},\n{l:'Years at TCS',c:'Since April 2025 as DevOps & Database Engineer.',n:1.7,d:1,s:'+',g:'Yr'}];"),
]

# validate all anchors first (all-or-nothing)
for old, _ in EDITS:
    n = s.count(old)
    if n != 1:
        sys.exit(f'ABORTED - expected 1 match, found {n} for:\n  {old[:90]}\n(index.html may have changed; nothing was modified.)')

shutil.copyfile('index.html', 'index.html.bak')
for old, new in EDITS:
    s = s.replace(old, new)
with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('Done. Backup saved as index.html.bak')
print('Added: Awards & Recognition + Academic/Training section, nav + menu + Ctrl-K entries, awards card in Achievements.')
