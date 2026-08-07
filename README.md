# From Future — fromfuture.io (Cinematic Rebuild)

Full static rebuild of fromfuture.io: **86 pages**, identical URL structure and content to the current site, redesigned as a dark cinematic-scroll experience in the official brand system (Future Purple `#C154F8` / Void `#0A0A0F` / Orbitron + Inter).

## What's in here

- `dist/` — the built website. **This is what gets deployed.**
- `build.py` + `src/` — the Python generator (edit content here, run `python3 build.py` to rebuild)
- `content/` — all harvested site content: 46 industry pages (JSON), 16 blog posts (Markdown), team pages, solutions index
- `assets/` — brand logos/icons from the media kit, CSS, JS
- `mediakit/` — your original media kit export

## Pages (same URLs as the live site — no links break)

Home, /services + 7 service pages, /pricing, /connect, /about + 3 team pages, /resources, /resources/free-ai-resources (+ /prompts), /blog + 16 posts, /solutions/voice-ai/ + 46 industry pages, /careers, /privacy, /terms. `/contact` (a 404 on the old site) now redirects to /connect.

## ⚠️ THE CLIENT PORTAL — read before touching DNS

The **Client Portal button links to `https://portal.fromfuture.io`** — same as today. The portal itself runs on **Wayfront** (SaaS) behind Cloudflare, **not** on the old web server, so redeploying the website cannot break it — as long as DNS for the subdomain is left alone.

Current DNS facts (verified Aug 7, 2026):
- Nameservers: Cloudflare (`eoin.ns.cloudflare.com` / `rosa.ns.cloudflare.com`)
- `fromfuture.io` (apex) → `152.53.81.11`  ← the old server. **This is the only record you change.**
- `portal.fromfuture.io` → Cloudflare-proxied → Wayfront  ← **DO NOT TOUCH**
- `www.fromfuture.io` → Cloudflare-proxied
- MX → Google Workspace, plus SPF/verification TXT records  ← **DO NOT TOUCH** (your email lives here)

### Cutover checklist (when you're ready to flip)

1. **Confirm who controls the Cloudflare account** holding the fromfuture.io zone. If it's yours — perfect, skip to step 3. If it's your former partner's:
2. In **Namecheap**, you can repoint nameservers to your own Cloudflare account — but FIRST recreate every existing record in your new Cloudflare zone (portal CNAME/proxy, www, MX, all TXT records). Cloudflare imports most of these automatically when you add the domain; verify `portal` and MX made it before switching.
3. Deploy the new site on Render (below), then change **only** the apex `fromfuture.io` (and `www`) records to point at Render.
4. Portal button keeps working because `portal.fromfuture.io` never changed.

## Deploy on Render (10 minutes)

1. Push this folder to a GitHub repo.
2. In Render: **New → Static Site** → connect the repo.
3. Build command: *(leave empty)* — Publish directory: `dist`
4. Add custom domains `fromfuture.io` and `www.fromfuture.io`; Render shows you the A/CNAME targets to set in Cloudflare (proxy off or on — both work).
5. Optional rebuilds: set build command to `python3 build.py` (Render's environment includes Python 3; also `pip install markdown`).

## Things to wire up / review (marked with HTML comments in the code)

1. **Voice demo widgets** (homepage "Play Demo", Tap-to-Talk page, chatbot demo): the old site used `<sistem-convai agent-id="...">` + `https://scripts.sistem.ai/voice.js`. Paste your agent IDs where the `<!-- VOICE WIDGET -->` comments are.
2. **PageSpeak audio players** (blog + PageSpeak page): powered by your 11Labs/PageSpeak system — embed slots are marked `<!-- PAGESPEAK PLAYER -->`.
3. **Phone AI callback form** and **Process Automation analyzer**: forms are built and styled; wire their submit handlers to your endpoints (see `assets/site.js`, `data-ff-form`).
4. **/connect booking widget**: the old page loaded a scheduler via JS. A `<!-- SCHEDULING EMBED -->` slot is ready — paste your Calendly (or other) inline embed.
5. **Newsletter form** (footer): currently a styled placeholder — wire to your email tool (Klaviyo TXT records exist on the domain) or Supabase.
6. **Pricing FAQ + PageSpeak FAQ answers**: the old site loaded answers via JavaScript, so they couldn't be extracted. The questions are verbatim; the answers were reconstructed from facts on the site — **review these before launch.**
7. **Team photos** (About page): initials placeholders until you drop in photos (`<!-- TEAM PHOTO -->` in `src/misc.py`).
8. **Blog fidelity**: all 16 posts are included; a few of the older posts are near-verbatim reconstructions rather than character-perfect copies — worth a skim.
9. **Hero film**: the hero uses a procedural particle nebula. A 10-second cinematic film was also generated in your Higgsfield library — download it and save as `assets/media/hero.mp4`, rebuild, and the hero upgrades to full video automatically.

## Analytics

GTM container `GTM-NFGP7XQD` is preserved on every page (LinkedIn Insight fires through GTM if configured there).
