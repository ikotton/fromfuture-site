from base import page, write_page, page_hero, cards_grid, cta_section
from services import sec, accordion
import os, re
import markdown as md

ROOT = "/home/claude/fromfuture-site"

# ---------------- connect ----------------
def build_connect():
    body = page_hero("Get Started", 'Schedule Your Free <span class="grad-text">Strategy Session</span>',
        "Book a 30-minute consultation with our AI specialists to discover how voice AI can transform your business")
    body += f"""<section style="padding-top:0"><div class="wrap"><div class="cta-grid" style="display:grid;grid-template-columns:1fr 1.2fr;gap:60px;align-items:start">
      <div>
        <h3 style="margin-bottom:24px">What to Expect</h3>
        <ul class="cta-list rv">
          <li>Custom AI implementation strategy</li>
          <li>ROI analysis for your business</li>
          <li>Live demo of our AI technology</li>
          <li>Industry-specific use cases</li>
          <li>Pricing and timeline discussion</li>
        </ul>
        <div class="card rv" style="margin-top:34px"><h3>30-Minute Session</h3>
          <p>Quick but comprehensive overview of how AI can benefit your business</p></div>
      </div>
      <div class="card" style="min-height:680px;padding:10px;overflow:hidden">
        <!-- Cal.com booking — official inline embed, same config as the live site
             (embed.js + Cal("init","30min") + calLink fromfutureai/30min) -->
        <div id="my-cal-inline" style="width:100%;height:660px;overflow:auto;position:relative;z-index:2"></div>
        <script type="text/javascript">
          (function (C, A, L) {{ let p = function (a, ar) {{ a.q.push(ar); }}; let d = C.document; C.Cal = C.Cal || function () {{ let cal = C.Cal; let ar = arguments; if (!cal.loaded) {{ cal.ns = {{}}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; }} if (ar[0] === L) {{ const api = function () {{ p(api, arguments); }}; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") {{ cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); }} else p(cal, ar); return; }} p(cal, ar); }}; }})(window, "https://app.cal.com/embed/embed.js", "init");
          Cal("init", "30min", {{origin:"https://cal.com"}});
          Cal.ns["30min"]("inline", {{
            elementOrSelector: "#my-cal-inline",
            config: {{"layout":"month_view","theme":"dark"}},
            calLink: "fromfutureai/30min"
          }});
          Cal.ns["30min"]("ui", {{"theme":"dark","hideEventTypeDetails":false,"layout":"month_view"}});
        </script>
      </div>
    </div></div></section>"""
    write_page("connect", page("Schedule Your Free Strategy Session | From Future",
        "Book a 30-minute consultation with our AI specialists to discover how voice AI can transform your business.", body,
        canonical="https://www.fromfuture.io/connect"))

# ---------------- about + team ----------------
LEADERS = [
 dict(slug="kotton-grammer", name="Kotton Grammer", role="CEO &amp; Founder", initials="KG",
      bio="Digital marketing pioneer and SEO visionary. Founded From Future to revolutionize AI-driven marketing solutions.",
      highlights=["Featured in Forbes, Inc.com, and Huffington Post","Built multiple 7-figure businesses","Pioneered AI integration in digital marketing"],
      quote="Revenue isn't everything; it's the only thing."),
 dict(slug="joe-mulcahy", name="Joe Mulcahy", role="Chief Technology Officer", initials="JM",
      bio="Self-taught tech innovator driving From Future's AI development and technical vision.",
      highlights=["Lead architect of From Future's AI solutions","Expert in automation and lead generation","Pioneered custom AI integration systems"],
      quote="Technology should solve real problems, not create new ones."),
 dict(slug="scotlyn-lozano", name="Scotlyn Lozano", role="Chief Marketing Officer", initials="SL",
      bio="Strategic marketing leader specializing in AI-driven business development and digital transformation.",
      highlights=["Scaled marketing operations for multiple tech companies","Expert in AI-powered outreach and lead generation","Pioneered innovative social media strategies"],
      quote="The future of marketing is personalized, automated, and AI-driven."),
]

def build_about():
    lead_cards = []
    for i, L in enumerate(LEADERS):
        hl = "".join(f"<li>{h}</li>" for h in L["highlights"])
        photo = {
          "kotton-grammer": "https://media.fromfuture.io/people/cards/kotton-portrait-card.png",
          "joe-mulcahy": "https://media.fromfuture.io/people/cards/joe-portrait-card.png",
          "scotlyn-lozano": "https://media.fromfuture.io/people/cards/scotlyn-portrait-card1.png",
        }[L['slug']]
        lead_cards.append(f"""<div class="card rv rv-d{i}">
          <img src="{photo}" alt="{L['name']}" width="104" height="104"
            style="width:104px;height:104px;border-radius:9999px;object-fit:cover;margin-bottom:24px;box-shadow:inset 0 1px 1px rgba(255,255,255,.18)"
            onerror="this.outerHTML='&lt;div class=&quot;avatar&quot;&gt;{L['initials']}&lt;/div&gt;'">
          <h3>{L['name']}</h3>
          <div style="font-family:var(--display);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--tint);margin:6px 0 14px">{L['role']}</div>
          <p>{L['bio']}</p><ul>{hl}</ul>
          <p class="quote">&ldquo;{L['quote']}&rdquo;</p>
          <a class="learn" style="margin-top:18px" href="/about/team/{L['slug']}">Learn more <span class="arrow">→</span></a></div>""")
    body = page_hero("About From Future", "We're not just another <span class='grad-text'>AI company</span>",
        "We're your catalyst for exponential growth through AI-powered solutions",
        '<a class="btn btn-primary" href="/connect">Schedule a Strategy Session</a><a class="btn btn-ghost" href="/services">Explore Our Solutions</a>')
    body += sec("Our Mission","Our <span class='grad-text'>Mission</span>","",
        """<div class="grid-2" style="align-items:center"><p class="lead rv" style="max-width:none">From Future is revolutionizing how businesses interact with AI technology. We make advanced AI solutions accessible and practical for businesses of all sizes. Our white-label solutions enable digital marketing agencies to expand into AI services seamlessly, while our direct solutions help businesses automate and enhance their customer interactions.</p>
        <div class="rv rv-d1" style="display:flex;justify-content:center"><img src="/assets/logo/fromfuture-mark-white.png" alt="From Future mark" style="width:200px;opacity:.9"></div></div>""")
    body += sec("Leadership","Meet Our <span class='grad-text'>Leadership</span>","", f'<div class="grid-3">{"".join(lead_cards)}</div>')
    body += sec("Our Values","What We <span class='grad-text'>Stand For</span>","",
        cards_grid([
          dict(title="Innovation First", desc="We constantly push the boundaries of what's possible with AI technology."),
          dict(title="Client Success", desc="Your growth is our priority. We measure our success through your achievements."),
          dict(title="Trust &amp; Security", desc="We maintain the highest standards of security and reliability in our AI solutions."),
        ]))
    body += cta_section()
    write_page("about", page("About From Future | Leading AI Solutions Provider | FromFuture.io",
        "Meet the team behind From Future, pioneering AI voice agents and automation solutions. Led by industry experts dedicated to revolutionizing how businesses interact with AI technology.",
        body, canonical="https://www.fromfuture.io/about"))

def build_team():
    for L in LEADERS:
        path = f"{ROOT}/content/team/{L['slug']}.md"
        content_html = ""
        if os.path.exists(path):
            raw = open(path).read()
            raw = re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
            content_html = md.markdown(raw, extensions=["tables"])
        hl = "".join(f"<li>{h}</li>" for h in L["highlights"])
        body = page_hero(L["role"].replace("&amp;","&"), L["name"], L["bio"])
        body += f"""<section style="padding-top:0"><div class="wrap"><div class="prose rv">
          <ul>{hl}</ul><blockquote>&ldquo;{L['quote']}&rdquo;</blockquote>{content_html}</div></div></section>"""
        body += cta_section()
        write_page(f"about/team/{L['slug']}", page(f"{L['name']} | From Future",
            L["bio"], body, canonical=f"https://www.fromfuture.io/about/team/{L['slug']}"))

# ---------------- resources ----------------
def build_resources():
    body = page_hero("Resources", 'Fuel Your <span class="grad-text">AI Journey</span>',
        "Free tools and resources to enhance your AI journey")
    body += f"""<section style="padding-top:0"><div class="wrap">{cards_grid([
      dict(title="Blog", badge="Updated", desc="Explore our latest articles, guides, and insights on AI technology and solutions", href="/blog"),
      dict(title="Free AI Resources", desc="Free professional prompts, tools, and guides for businesses", href="/resources/free-ai-resources"),
      dict(title="AI for Agencies", badge="Coming Soon", soon=True, desc="Learn how agencies can leverage AI to expand services and increase revenue"),
    ])}</div></section>"""
    body += cta_section()
    write_page("resources", page("Resources | From Future",
        "Free tools and resources to enhance your AI journey.", body, canonical="https://www.fromfuture.io/resources"))

    body = page_hero("Free AI Resources", 'Free AI <span class="grad-text">Resources</span>',
        "Free tools and resources to enhance your AI journey")
    body += f"""<section style="padding-top:0"><div class="wrap">{cards_grid([
      dict(title="AI Analysis Prompts", desc="Free professional prompts for business intelligence and market analysis", href="/resources/free-ai-resources/prompts"),
      dict(title="Coming Soon", badge="Coming Soon", soon=True, desc="More AI resources and tools coming soon"),
    ], cols=2)}</div></section>"""
    body += cta_section()
    write_page("resources/free-ai-resources", page("Free AI Resources | From Future",
        "Free professional prompts, tools, and guides for businesses.", body, canonical="https://www.fromfuture.io/resources/free-ai-resources"))

    body = page_hero("AI Analysis Prompts", 'AI Analysis <span class="grad-text">Prompts</span>',
        "Free professional prompts for business intelligence and market analysis")
    body += f"""<section style="padding-top:0"><div class="wrap">{cards_grid([
      dict(title="Social Media Forensic Analysis", desc="Deep dive into social media presence to uncover patterns, relationships, and hidden insights."),
      dict(title="Business Forensic Analysis", desc="Comprehensive analysis of business operations, market position, and growth potential."),
    ], cols=2)}<div style="margin-top:40px"><a class="learn" href="/resources/free-ai-resources">&larr; Back to Resources</a></div></div></section>"""
    write_page("resources/free-ai-resources/prompts", page("AI Analysis Prompts | From Future",
        "Free professional prompts for business intelligence and market analysis.", body,
        canonical="https://www.fromfuture.io/resources/free-ai-resources/prompts"))

# ---------------- careers ----------------
def build_careers():
    perks = cards_grid([
      dict(title="Remote-First Culture", desc="Work from anywhere in the world with flexible hours"),
      dict(title="Career Growth", desc="Continuous learning opportunities and clear advancement paths"),
      dict(title="Comprehensive Benefits", desc="Health, dental, and vision coverage for you and your family"),
      dict(title="Unlimited PTO", desc="Take the time you need to recharge and stay productive"),
      dict(title="Learning Budget", desc="Annual budget for courses, conferences, and certifications"),
      dict(title="Collaborative Environment", desc="Work with talented individuals who share your passion for AI"),
    ])
    jobs = [
      ("AI Solutions Architect","Engineering &middot; Remote &middot; Full-time","Design and implement custom AI solutions for enterprise clients.",
       ["Experience with LLMs and AI frameworks","5+ years software architecture","Strong cloud infrastructure background","Excellent communication skills"],"ai-solutions-architect"),
      ("Voice AI Developer","Engineering &middot; Remote &middot; Full-time","Build next-generation voice AI applications and integrations.",
       ["Speech recognition and NLP experience","Strong JavaScript/TypeScript","Real-time audio processing","API integration"],"voice-ai-developer"),
      ("AI Marketing Strategist","Marketing &middot; Remote &middot; Full-time","Develop AI-driven marketing strategies for our clients.",
       ["Digital marketing expertise","Understanding of AI capabilities/limitations","Marketing automation experience","Data analysis skills"],"ai-marketing-strategist"),
    ]
    job_html = ""
    for i,(t,meta,d,reqs,slug) in enumerate(jobs):
        r = "".join(f"<li>{x}</li>" for x in reqs)
        job_html += f"""<div class="card rv rv-d{i}" style="display:flex;flex-direction:column">
          <div style="font-family:var(--display);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--tint);margin-bottom:12px">{meta}</div>
          <h3>{t}</h3><p style="margin-top:10px">{d}</p><ul>{r}</ul>
          <a class="btn btn-primary" style="margin-top:auto;justify-content:center" href="/careers/{slug}/apply">Apply Now</a></div>"""
    for t, meta, d, reqs, slug in jobs:
        form = f"""<section style="padding-top:0"><div class="wrap"><div class="card" style="max-width:760px;margin:0 auto;padding:40px 36px">
          <form class="form-grid" style="max-width:none" data-ff-form>
            <input type="hidden" name="position" value="{t}">
            <div class="grid-2" style="gap:14px"><input type="text" name="firstName" required placeholder="First name"><input type="text" name="lastName" required placeholder="Last name"></div>
            <input type="email" name="email" required placeholder="Email">
            <input type="tel" name="phone" placeholder="Phone">
            <input type="text" name="location" placeholder="City, Country">
            <input type="url" name="linkedIn" placeholder="https://linkedin.com/in/...">
            <input type="url" name="portfolio" placeholder="https://...">
            <input type="url" name="github" placeholder="https://github.com/...">
            <select name="experience" style="background:rgba(255,255,255,.04);border:1px solid hsl(var(--foreground) / .12);border-radius:9999px;padding:14px 20px;color:hsl(var(--foreground));font-family:var(--body);font-size:15px">
              <option value="">Years of experience</option><option>0-2 years</option><option>3-5 years</option><option>5-8 years</option><option>8+ years</option></select>
            <textarea name="coverLetter" rows="6" placeholder="Tell us about your interest in From Future..." style="background:rgba(255,255,255,.04);border:1px solid hsl(var(--foreground) / .12);border-radius:16px;padding:16px 20px;color:hsl(var(--foreground));font-family:var(--body);font-size:15px;resize:vertical"></textarea>
            <label style="font-size:13.5px;color:hsl(var(--foreground) / .5)">Resume <input type="file" name="resumeFile" style="border:none;background:none;padding:8px 0;border-radius:0"></label>
            <button class="btn btn-primary" type="submit" style="justify-content:center">Submit Application</button>
          </form></div></div></section>"""
        pbody = page_hero("Careers", f'Apply for <span class="grad-text">{t}</span>', d) + form
        write_page(f"careers/{slug}/apply", page(f"Apply for {t} | From Future", d, pbody,
            canonical=f"https://www.fromfuture.io/careers/{slug}/apply"))

    body = page_hero("Careers", 'Join the <span class="grad-text">Future of AI</span>',
        "Help shape the future of digital marketing with AI-powered solutions that transform businesses.")
    body += sec("Benefits","Why Join <span class='grad-text'>From Future?</span>","", perks)
    body += sec("Open Positions","Open <span class='grad-text'>Positions</span>","", f'<div class="grid-3">{job_html}</div>')
    body += cta_section()
    write_page("careers", page("Careers | From Future",
        "Help shape the future of digital marketing with AI-powered solutions that transform businesses.", body,
        canonical="https://www.fromfuture.io/careers"))

# ---------------- legal ----------------
def legal_page(slug, title, sections):
    inner = ""
    for h, items in sections:
        inner += f"<h2>{h}</h2>"
        for it in items:
            if isinstance(it, list):
                inner += "<ul>" + "".join(f"<li>{x}</li>" for x in it) + "</ul>"
            else:
                inner += f"<p>{it}</p>"
    body = page_hero("Legal", title, f'Last updated: <span id="legal-date"></span><script>document.currentScript.previousSibling.textContent=new Date().toLocaleDateString("en-US")</script>')
    body += f'<section style="padding-top:0"><div class="wrap"><div class="prose rv">{inner}</div></div></section>'
    write_page(slug, page(f"{title} | From Future", f"From Future {title}.", body,
        canonical=f"https://www.fromfuture.io/{slug}"))

def build_legal():
    legal_page("privacy","Privacy Policy",[
      ("1. Introduction",["This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI voice assistant services, visit our website, or interact with our platform."]),
      ("2. Information We Collect",[
        "<strong>2.1 Personal Information.</strong> We may collect personal information including your name, contact details, email address, phone number, business information, login credentials, payment information, and communication preferences.",
        "<strong>2.2 Voice Data.</strong> When using our voice assistant services, we collect:",
        ["Voice recordings from interactions with our AI assistants","Transcripts of conversations"],
        "<strong>2.3 Technical Data.</strong> We collect technical information including IP addresses, location data, browser type, device information, operating system, usage patterns, and error logs."]),
      ("3. How We Use Your Information",[
        "<strong>3.1 Service Provision.</strong> We use your information to deliver and maintain our AI voice assistant services and to train and improve our AI models.",
        "<strong>3.2 Communication and Support.</strong> We use your information to respond to inquiries, send service updates, and provide marketing communications with your consent.",
        "<strong>3.3 Business Operations.</strong> We use your information for payment processing, fraud prevention, legal compliance, and business analysis."]),
      ("4. Data Sharing and Disclosure",[
        "We may share your information with:",
        ["Service providers","AI technology partners","Legal authorities when required","Business partners with your explicit consent"]]),
      ("5. Data Security",[
        "We implement industry-standard security measures including:",
        ["Encryption of data in transit and at rest","Regular security assessments and audits"]]),
      ("6. Your Rights and Choices",[
        "You have the right to:",
        ["Access your personal information","Correct inaccurate information","Delete your information","Opt out of marketing communications","Export your data"]]),
      ("7. Data Retention",["Voice recordings and transcripts are retained for a period of 30 days unless otherwise specified by contract or legal requirements."]),
      ("8. International Data Transfers",["Your information may be transferred internationally with appropriate safeguards in place."]),
      ("9. Changes to This Policy",["We may update this policy from time to time and will notify you of material changes."]),
      ("10. Contact Us",['If you have questions about this Privacy Policy, contact us at <a href="mailto:support@fromfuture.io">support@fromfuture.io</a> &mdash; Miami, FL, USA.']),
    ])
    legal_page("terms","Terms of Service",[
      ("1. Agreement to Terms",["By accessing or using the services provided by From Future (&ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;), including our AI voice assistant services, website, and related technologies, you agree to be bound by these Terms of Service."]),
      ("2. Description of Services",[
        "From Future provides white-label AI voice assistant solutions, including:",
        ["Tap-to-talk website voice agents","Phone-call voice agents","AI conversation management systems","Voice customization tools","Integration services","Analytics and reporting tools"]]),
      ("3. Account Terms",[
        ["You must be 18 years or older to use our services","You must provide accurate registration information","You are responsible for maintaining account security","You must notify us immediately of any unauthorized access","We reserve the right to terminate accounts for violations"]]),
      ("4. Service Usage and Limitations",[
        "<strong>4.1 Acceptable Use.</strong> You agree not to use our services to:",
        ["Violate any laws or regulations","Harass, abuse, or harm others","Impersonate others or provide false information","Interfere with the proper functioning of the services","Attempt to gain unauthorized access to our systems"],
        "<strong>4.2 Service Limitations.</strong> Services are provided &ldquo;as is&rdquo; without warranties. We may modify or discontinue services, availability and quality may vary, and AI responses may have imperfections."]),
      ("5. Intellectual Property",[
        ["We retain all rights to our technology","You retain rights to your content and data","You grant us a license to use your data for service provision","White-label rebranding is permitted per service agreements"]]),
      ("6. Payment Terms",[
        ["Fees are specified in service agreements","Payments are non-refundable unless otherwise stated","We may change pricing with notice","Late payments may result in service suspension"]]),
      ("7. Data Usage and Privacy",['Our collection and use of your information is governed by our <a href="/privacy">Privacy Policy</a>.']),
      ("8. Liability and Indemnification",[
        "<strong>8.1</strong> We are not liable for any indirect, incidental, special, consequential, or punitive damages arising from your use of our services.",
        "<strong>8.2</strong> You agree to indemnify and hold us harmless from any claims arising from your use of our services or violation of these terms."]),
      ("9. Service Level Agreement",[
        ["99.9% uptime target","Support response times per agreements","Advance communication of scheduled maintenance","Service credits for enterprise customers"]]),
      ("10. Termination",[
        ["Either party may terminate with notice","We may terminate immediately for violations","You remain liable for all fees incurred through termination","Certain provisions survive termination"]]),
      ("11. Changes to Terms",["We reserve the right to modify these terms at any time. We will notify you of significant changes through our website or direct communication."]),
      ("12. Contact Information",['Questions about these Terms? Contact us at <a href="mailto:support@fromfuture.io">support@fromfuture.io</a> &mdash; Miami, FL, USA.']),
    ])

def build():
    build_connect(); build_about(); build_team(); build_resources(); build_careers(); build_legal()
