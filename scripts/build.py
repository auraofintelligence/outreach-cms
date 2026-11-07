import argparse
import html
import json
import shutil
from pathlib import Path
from cms import ROOT, load_public

OUT = ROOT / ".site"
ICONS = {
 "home": '<path d="m3 11 9-8 9 8v10h-6v-7H9v7H3Z"/>',
 "route": '<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M5 7v7a5 5 0 0 0 5 5h7M9 5h8v6"/>',
 "place": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 7h14M5 17h14"/>',
 "work": '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12h18M10 12v3h4v-3"/>',
 "write": '<path d="M16 3 21 8 9 20 3 21 4 15Z M13 6l5 5"/>',
 "book": '<path d="M12 5c-4-3-8-2-10-1v16c4-2 7-1 10 1 3-2 6-3 10-1V4c-3-1-7-2-10 1Z M12 5v16"/>',
 "settings": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 3v18M8 9h13M13 14h4M13 17h4"/>',
 "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
 "external": '<path d="M13 3h8v8M21 3 10 14M10 3H3v18h18v-7"/>',
}
NAV = [("index.html", "Overview", "home"), ("routes.html", "Find routes", "route"), ("places.html", "Places", "place"), ("sister-cities.html", "Queensland sister cities", "place"), ("projects.html", "Connected work", "work"), ("invite.html", "Prepare invitation", "write"), ("playbook.html", "How it works", "book"), ("workspace.html", "Workspace", "settings")]
THEMES = {"law":"Law and rights", "resilience":"Disaster resilience", "technology":"Technology and data", "cooperation":"Cooperation", "culture":"Culture and knowledge", "civic":"Civic participation", "community":"Community networks", "education":"Education", "livelihoods":"Livelihoods"}
LEADS = {
 "index": ("Find a route into every place.", "A contact workbench for GAJRA Earth, P4A and the Web3 Sensorium. Explore existing networks, connect useful work to local needs and prepare a relevant introduction."),
 "routes": ("Start with an existing connection.", "Find public directories and organisations that can open a conversation. Check the local organisation and choose the appropriate contact route."),
 "places": ("Every place has its own context.", "Explore the country and territory reference list. Record real connections as they develop, while making room for communities that cross borders."),
 "sister-cities": ("Local connections. International introductions.", "Explore Queensland council and state relationships, then ask the responsible team about a relevant introduction. Formal sister links, friendship agreements and other partnerships retain their own labels."),
 "projects": ("Useful work gives an invitation substance.", "Approach people through a subject that matters locally. These connected projects offer several ways to begin."),
 "invite": ("Prepare a relevant introduction.", "Choose the place, project and request. Make the wording your own, then decide how to share it."),
 "playbook": ("Make contact. Keep the next step clear.", "A repeatable way to find appropriate people, make a useful approach and turn replies into direct relationships."),
 "workspace": ("Keep the working records together.", "Edit public website content in the CMS. Keep personal contacts, correspondence and outreach decisions in the private workspace."),
}

def e(value): return html.escape(str(value), quote=True)
def icon(name): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS.get(name,ICONS["route"])}</svg>'
def tag(text, cls=""): return f'<span class="tag {cls}">{e(text)}</span>'
def external(url, label, cls=""): return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}{icon("external")}</a>'

def source_card(row):
    return f'''<article class="source-card" data-source data-projects="{e(row.get('project_ids', ''))}" data-theme="{e(row['theme'])}" data-scope="{e(row['scope'])}" data-search="{e(' '.join(str(v) for v in row.values()).lower())}">
      <div class="source-top">{tag(THEMES[row['theme']])}<span class="scope">{e(row['scope'])}</span></div>
      <h3>{e(row['name'])}</h3><p>{e(row['summary'])}</p><details><summary>How to make contact</summary><p>{e(row['contact_route'])}</p></details>
      <div class="source-bottom"><span>{e(row['status'])}<small>{e(row['checked_on'])}</small></span>{external(row['url'],'Open source','text-link')}</div></article>'''

def project_card(row):
    return f'''<article class="project-card"><span class="project-symbol">{icon({'law':'book','resilience':'route','technology':'settings','cooperation':'place'}.get(row['theme'],'work'))}</span>{tag(THEMES[row['theme']])}<h3>{e(row['title'])}</h3><p>{e(row['summary'])}</p><div class="project-links">{external(row['url'],'Explore project','text-link')}<a class="text-link" href="routes.html?project={e(row['id'])}">Find outreach bodies {icon("arrow")}</a><a href="invite.html?project={e(row['id'])}">Prepare invitation {icon('arrow')}</a></div></article>'''

def overview(data):
    count = len(data['places'])
    override=next((r for r in data.get('pages',[]) if r['id']=='index'),None)
    heading,lead=(override['heading'],override['body']) if override else LEADS['index']
    return f'''<section class="hero"><div><p class="eyebrow">LOCAL KNOWLEDGE · WORLDWIDE CONNECTION</p><h1>{e(heading)}</h1><p class="hero-lead">{e(lead)}</p><div class="actions"><a class="button" href="routes.html">Explore contact routes {icon('arrow')}</a><a class="button secondary" href="invite.html">Prepare an invitation</a></div><p class="hero-note">{e(data['settings']['strapline'])}</p></div><div class="reach-panel"><div class="panel-heading"><span class="live-dot"></span> The reach ledger <span class="small-label">STARTING POINT</span></div><div class="orbit" aria-hidden="true"><div class="orbit-ring ring-a"></div><div class="orbit-ring ring-b"></div><div class="orbit-ring ring-c"></div><div class="orbit-core">{icon('place')}</div><span class="orbit-node n1"></span><span class="orbit-node n2"></span><span class="orbit-node n3"></span><span class="orbit-node n4"></span><span class="orbit-node n5"></span><span class="orbit-node n6"></span></div><div class="reach-count"><strong>{count}</strong><span>reference places<br>open for discovery</span></div><p>Countries and territories are a starting index. People and cultures give each place its meaning.</p><a href="places.html">Explore the place register {icon('arrow')}</a></div></section>
      <section class="stats" aria-label="Published catalogue totals"><div><strong>{len(data['sources'])}</strong><span>public discovery routes</span></div><div><strong>{len(data['projects'])}</strong><span>connected project starting points</span></div><div><strong>{sum(r['resident_contacts'] for r in data['places'])}</strong><span>confirmed resident contacts recorded</span></div></section>
      <section class="section"><div class="section-head"><div><p class="eyebrow">FIND YOUR STARTING POINT</p><h2>People are already connected.</h2><p>Use a network that overlaps the place and the work you care about.</p></div><a class="text-link" href="routes.html">View every route {icon('arrow')}</a></div><div class="source-grid">{''.join(source_card(s) for s in data['sources'][:3])}</div></section>
      <section class="section work-section"><div class="section-head"><div><p class="eyebrow">THE WORK BEHIND THE INVITATION</p><h2>Choose a useful way to begin.</h2></div><a class="text-link" href="projects.html">Connected work {icon('arrow')}</a></div><div class="project-grid">{''.join(project_card(p) for p in data['projects'][:3])}</div></section>
      <aside class="wide-note"><span>{icon('book')}</span><div><h3>Different places. Shared learning.</h3><p>The UNGA81 contribution invites locally shaped associations to cooperate while retaining their own judgment, culture and authority over information.</p></div>{external('https://auraofintelligence.github.io/UNGA81-Luke-Hayes/futures.html','Read the invitation','text-link')}</aside>'''

def routes(data):
    options=''.join(f'<option value="{k}">{v}</option>' for k,v in THEMES.items())
    scopes=''.join(f'<option>{e(x)}</option>' for x in sorted({r['scope'] for r in data['sources']}))
    projects=''.join(f'<option value="{e(p["id"])}">{e(p["title"])}</option>' for p in data['projects'])
    return f'''<div class="filter-bar route-filters"><label class="search-field"><span>Search sources</span><input id="source-search" type="search" placeholder="Name, interest or type of work"></label><label><span>Connected project</span><select id="project-filter"><option value="">All projects</option>{projects}</select></label><label><span>Interest</span><select id="theme-filter"><option value="">All interests</option>{options}</select></label><label><span>Scope</span><select id="scope-filter"><option value="">All scopes</option>{scopes}</select></label><button class="clear-button" id="reset-sources">Reset filters</button></div><div class="results-line"><p id="source-count" role="status">{len(data['sources'])} routes to investigate</p><span>Project matches are suggested approaches, subject to each body's interests.</span></div><div class="source-grid" id="source-results">{''.join(source_card(s) for s in sorted(data['sources'],key=lambda r:r['checked_on'],reverse=True))}</div><p id="source-empty" class="empty-state" hidden>No matching routes. Try a broader project, interest or scope.</p><aside class="wide-note"><div><h3>Choose the right request.</h3><p>Ask for an introduction, appropriate circulation, a conversation or a defined collaboration. Check each body's current remit and any fees. A public route does not establish local participation or a partnership.</p></div><a class="text-link" href="invite.html">Prepare an approach {icon('arrow')}</a></aside>'''

def sister_row(row):
    notes=f'<p class="relationship-note">{e(row["notes"])}</p>' if row.get('notes') else ''
    return f'''<article class="relationship-row" data-sister data-place="{e(row['queensland_place'])}" data-level="{e(row['level'])}" data-relationship="{e(row['relationship'])}" data-status="{e(row['status'])}" data-search="{e(' '.join(str(v) for v in row.values()).lower())}"><div><h3>{e(row['partner_place'])}</h3><p class="relationship-country">{e(row['country'])}</p></div><div>{tag(row['relationship'])}<p class="relationship-date">{('Agreement year: '+e(row['year'])) if row['year'] else 'Signing year not verified'} · {e(row['status'])}</p></div>{notes}<div class="relationship-source">{external(row['source_url'],'Official evidence','text-link')}<span>Checked {e(row['checked_on'])}</span></div></article>'''

def sister_cities(data):
    links=data.get('sister_links', [])
    places=list(dict.fromkeys(r['queensland_place'] for r in links))
    def options(values): return ''.join(f'<option>{e(x)}</option>' for x in values)
    groups=[]
    for place in places:
        rows=[r for r in links if r['queensland_place']==place]
        first=rows[0]
        groups.append(f'''<section class="sister-group" data-sister-group><header><div><p class="eyebrow">{'STATE RELATIONSHIPS' if first['level']=='State' else 'COUNCIL RELATIONSHIPS'}</p><h2>{e(place)}</h2></div>{external(first['contact_url'],'Contact the responsible team','text-link')}</header><p class="sister-contact">{e(first['contact_route'])}</p><div class="relationship-list">{''.join(sister_row(r) for r in rows)}</div></section>''')
    return f'''<aside class="wide-note sister-intro"><span>{icon('route')}</span><div><h2>An existing bridge to start from.</h2><p>Choose a Queensland place, then ask its council or state team whether an appropriate counterpart, local association or community group could receive an introduction. Mention a specific project and a small first request.</p><p>These are documented relationships, not confirmed resident contacts. “Listed by source” records the official evidence available when checked; it does not confirm a current exchange programme. Records needing confirmation remain labelled.</p></div></aside><div class="filter-bar sister-filters"><label class="search-field"><span>Search international links</span><input id="sister-search" type="search" placeholder="Partner, country or agreement"></label><label><span>Queensland place</span><select id="sister-place"><option value="">All places</option>{options(places)}</select></label><label><span>Level</span><select id="sister-level"><option value="">City and state</option><option>City</option><option>State</option></select></label><label><span>Relationship</span><select id="sister-type"><option value="">All relationships</option>{options(sorted({r['relationship'] for r in links}))}</select></label><label><span>Evidence</span><select id="sister-status"><option value="">All evidence</option>{options(sorted({r['status'] for r in links}))}</select></label><button id="reset-sisters" class="clear-button">Reset filters</button></div><div class="results-line"><p id="sister-count" role="status">{len(links)} documented international links across {len(places)} Queensland places</p><span>Source and contact links lead to official council or state pages.</span></div><div class="sister-groups">{''.join(groups)}</div><p id="sister-empty" class="empty-state" hidden>No links match these filters. Try another place or relationship.</p><aside class="wide-note"><div><h3>Make the request locally specific.</h3><p>For example: could the sister-city team suggest a community, library, tourism, technology or resilience organisation interested in a short English-language conversation? Let each organisation decide whether to introduce people.</p></div><a href="projects.html" class="text-link">Choose a project {icon('arrow')}</a></aside>'''

def places(data):
    rows=''.join(f'''<tr data-place data-region="{e(r['region'])}" data-search="{e((r['name']+' '+r['code']+' '+r['region']).lower())}"><td><button class="place-button" data-place-code="{e(r['code'])}"><span class="place-code">{e(r['code'])}</span>{e(r['name'])}</button></td><td>{e(r['region'])}</td><td>{tag(r['stage'],'muted')}</td><td>{r['resident_contacts']}</td><td>{r['communities']}</td><td><a class="text-link" href="invite.html?place={e(r['code'])}" aria-label="Prepare invitation for {e(r['name'])}">{icon('arrow')}</a></td></tr>''' for r in data['places'])
    return f'''<div class="info-strip">{icon('place')}<p><strong>{len(data['places'])} reference places.</strong> This catalogue includes countries, territories and special geographic codes. It does not count sovereign states or claim cultural representation.</p></div><div class="filter-bar"><label class="search-field"><span>Find a place</span><input id="place-search" type="search" placeholder="Search a country, territory or code"></label><label><span>Region</span><select id="region-filter"><option value="">All regions</option>{''.join('<option>'+x+'</option>' for x in ['Africa','Americas','Asia','Europe','Oceania'])}</select></label><label><span>Contact stage</span><select id="stage-filter"><option value="">All stages</option>{''.join('<option>'+x+'</option>' for x in ['Seeking contacts','Route identified','In conversation','Resident connection'])}</select></label></div><div class="results-line"><p id="place-count" role="status">{len(data['places'])} places</p><a href="docs/data-sources.html">About the reference data</a></div><div class="table-wrap"><table class="places-table"><thead><tr><th>Place</th><th>Region</th><th>Stage</th><th>Residents</th><th>Communities</th><th><span class="sr-only">Prepare invitation</span></th></tr></thead><tbody>{rows}</tbody></table></div><p id="place-empty" class="empty-state" hidden>No places match these filters.</p><dialog id="place-dialog"><button id="close-place" class="close-button" aria-label="Close place details">×</button><div id="place-detail"></div></dialog>'''

def invite(data):
    projects=''.join(f'<option value="{e(p["id"])}">{e(p["title"])}</option>' for p in data['projects'])
    places_=''.join(f'<option value="{e(p["code"])}">{e(p["name"])}</option>' for p in data['places'])
    return f'''<div class="invitation-layout"><form id="invitation-form" class="form-panel"><div class="form-heading"><span class="step-number">01</span><div><h2>Give the approach some context.</h2><p>Fill what you know. Keep the first request clear.</p></div></div><label>Connected project<select name="project" id="invite-project" required>{projects}</select></label><div class="form-row"><label>Place<select name="place" id="invite-place"><option value="">Across places</option>{places_}</select></label><label>The request<select name="request" id="invite-request"><option value="circulate">Circulate an invitation</option><option value="introduce">Make an introduction</option><option value="conversation">Have a conversation</option><option value="collaborate">Explore collaboration</option></select></label></div><div class="form-row"><label>Recipient name<input name="name" maxlength="120" placeholder="Optional"></label><label>Organisation<input name="organisation" maxlength="160" placeholder="Optional"></label></div><label>Why this contact fits<textarea name="context" rows="3" maxlength="1000" placeholder="A specific connection to their work or community"></textarea></label><label>Recipient email<input name="email" type="email" maxlength="200" placeholder="Optional, for opening your email app"></label><button class="button" type="submit">Prepare draft {icon('write')}</button><p class="field-note">The draft is prepared in your browser. You choose whether and how to share it.</p></form><section class="draft-panel"><div class="form-heading"><span class="step-number">02</span><div><h2>Review it in your own voice.</h2><p>Edit the subject and message before sharing.</p></div></div><label>Subject<input id="draft-subject" placeholder="Your subject will appear here"></label><label>Message<textarea id="draft-body" rows="20" placeholder="Choose a project and prepare a draft."></textarea></label><div class="draft-actions"><button type="button" class="button" id="copy-draft" disabled>Copy draft</button><button type="button" class="button secondary" id="download-draft" disabled>Download text</button><a class="button secondary" id="compose-email" hidden>Open email app</a></div><p id="draft-status" class="field-note" role="status"></p></section></div>'''

def playbook(data):
    steps=[('Find an appropriate route','Search across place, community and interest. Use an organisation’s own contact information to check a directory lead.'),('Choose a useful request','Ask for circulation, an introduction, a conversation or a defined collaboration. Link the project that fits the recipient.'),('Record the next action','Keep the contact source, last exchange, relationship owner, next action and sharing preferences together.'),('Make the approach','Use the appropriate channel and the authority agreed for the message or campaign. Keep a record of the actual result.'),('Turn replies into relationships','Answer the question, follow the introduction or discuss a local need. Confirm what was agreed and keep direct communication available.'),('Learn where access is missing','Look at confirmed contacts and conversations alongside geographic, cultural and language gaps. Use the results to select the next work.')]
    return '<div class="steps-list">'+''.join(f'<article><span class="step-number">0{i+1}</span><div><h2>{e(t)}</h2><p>{e(b)}</p></div></article>' for i,(t,b) in enumerate(steps))+'</div><section class="section"><h2>Five connected records</h2><div class="record-grid">'+''.join(f'<article><h3>{e(t)}</h3><p>{e(b)}</p></article>' for t,b in [('Contacts','People, organisations, current places, interests and appropriate channels.'),('Sources','Where a lead came from, when it was checked and how it can be used.'),('Outreach history','The approach, message version, response and next action.'),('Coverage','Reference places, actual resident connections and community participation.'),('Permissions','Agreed contact, introductions, updates and public attribution.')])+'</div></section><aside class="wide-note"><div><h3>Several routes into each place.</h3><p>Institutional reach and freedom to participate are separate questions. Keep known governance and affiliation facts alongside independently sourced routes, and let people describe their own connections.</p></div></aside>'

def workspace(data):
    c=data['config'];cms=external(c['cms_url'],'Open public-content CMS','button') if c.get('cms_url') else '<span class="setup-state">CMS workbook connection pending</span>'
    private=external(c['workspace_url'],'Open private contact workbook','button secondary') if c.get('workspace_url') else '<span class="setup-state">Private workbook connection pending</span>'
    note='<p class="info-strip">The CMS workbook is prepared. Automatic Sheets refresh awaits public Viewer access; this publication uses the verified source snapshot.</p>' if data['meta']['mode']=='Source snapshot' and c.get('cms_url') else ''
    return f'''{note}<div class="workspace-grid"><article class="workspace-card"><span class="workspace-icon">{icon('book')}</span><p class="eyebrow">PUBLIC EDITORIAL CONTENT</p><h2>The website CMS</h2><p>Edit headings, source routes, projects and approved aggregate place counts. Set a row’s Publish field to Yes when it is ready for the website.</p>{cms}<p class="field-note">Keep personal contact records in the private workbook.</p></article><article class="workspace-card private-card"><span class="workspace-icon">{icon('settings')}</span><p class="eyebrow">PRIVATE OPERATING RECORDS</p><h2>The contact workspace</h2><p>Keep people, correspondence, permissions and next actions together. Google account permissions control access to this workbook.</p>{private}<p class="field-note">The public website build does not read this workbook.</p></article></div><section class="section"><div class="section-head"><div><p class="eyebrow">PUBLISHING AND MAINTENANCE</p><h2>GitHub takes care of the repeatable work.</h2></div>{external(c['repository_url']+'/actions','Open GitHub Actions','text-link')}</div><div class="automation-list"><article><span class="automation-symbol">↻</span><div><h3>Refresh and publish</h3><p>On a code change, manually, or every six hours: build from the connected public CMS or current source snapshot, run checks and publish through GitHub Pages.</p></div>{tag('Every 6 hours')}</article><article><span class="automation-symbol">✓</span><div><h3>Check changes</h3><p>Pull requests check the public schema, publication filtering and the static build before merging.</p></div>{tag('Every pull request')}</article><article><span class="automation-symbol">↗</span><div><h3>Review source links</h3><p>A weekly report checks the public project and directory URLs. Access restrictions remain distinct from broken links.</p></div>{tag('Weekly')}</article></div></section><div class="workspace-bottom"><div><h3>Publication state</h3><p><strong>{e(data['meta']['mode'])}</strong><br>Built {e(data['meta']['built_at'][:16].replace('T',' '))} UTC</p>{external(data['meta']['run_url'],'View publishing run','text-link') if data['meta']['run_url'] else ''}</div><div><h3>Editor and setup guide</h3><p>See the exact sheet columns, deployment steps, publishing controls and recovery instructions.</p>{external(c['repository_url']+'/blob/main/docs/cms-guide.md','Read the CMS guide','text-link')}</div></div>'''

def projects(data):
    groups = [
        ('Law and community computing', ['your-relevance', 'legal-engine', 'missing-middle']),
        ('P4A', ['p4a-cinema', 'p4a-oceania', 'p4a-native-nations']),
        ('GAJRA Earth', ['gajra-earth', 'gajra-claude', 'gajra-community']),
        ('Aura', ['aura-genesis', 'aura-tourism', 'disaster-resilience']),
        ('Aura support and participation', ['aura-child-services', 'aura-whole-of-life', 'verse-box']),
    ]
    by_id = {p['id']: p for p in data['projects']}
    used = set()
    rows = []
    for label, ids in groups:
        items = [by_id[id] for id in ids if id in by_id]
        used.update(p['id'] for p in items)
        if items:
            rows.append(f'<section class="project-grid" aria-label="{e(label)}">'+''.join(project_card(p) for p in items)+'</section>')
    remaining = [p for p in data['projects'] if p['id'] not in used]
    if remaining:
        rows.append('<section class="project-grid" aria-label="Connected cooperation">'+''.join(project_card(p) for p in remaining)+'</section>')
    return '<div class="project-rows">'+''.join(rows)+'</div>'

def simple_page(key, data):
    if key=='index': return overview(data)
    content={'routes':routes,'sister-cities':sister_cities,'places':places,'projects':projects,'invite':invite,'playbook':playbook,'workspace':workspace}[key](data)
    override=next((r for r in data.get('pages',[]) if r['id']==key),None)
    title,lead=(override['heading'],override['body']) if override else LEADS[key]
    return f'<header class="page-heading"><p class="eyebrow">WORLDWIDE CONTACT SYSTEM</p><h1>{e(title)}</h1><p>{e(lead)}</p></header>'+content

def frame(key,body,data,title=None):
    nav=''.join(f'<a href="{url}" class="nav-link {"active" if url==key+".html" else ""}" {"aria-current=page" if url==key+".html" else ""}>{icon(ico)}<span>{label}</span></a>' for url,label,ico in NAV)
    label=dict((u[:-5],l) for u,l,_ in NAV).get(key,title or 'Reference')
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A worldwide contact workbench connecting local knowledge, community capability and international cooperation."><meta name="theme-color" content="#34254b"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'"><title>{e(title or label)} · {e(data['settings']['title'])}</title><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script type="module" src="assets/site.js"></script></head><body data-page="{key}"><a class="skip-link" href="#main">Skip to content</a><aside class="sidebar"><a class="brand" href="index.html"><img src="assets/favicon.svg" width="42" height="42" alt=""><span>{e(data['settings']['title']).replace(' Contact System','<br><strong>Contact System</strong>')}</span></a><p class="sidebar-label">THE WORKBENCH</p><nav aria-label="Main navigation">{nav}</nav><div class="sidebar-bottom"><p>Joyful Responsible<br>Abundance on Earth</p>{external('https://auraofintelligence.github.io/','Aura of Intelligence','sidebar-about')}{external('https://auraofintelligence.github.io/strange-but-true/','Strange But True','sidebar-about')}{external('https://github.com/auraofintelligence/open-record-luke-nathan-hayes','Meet Luke','sidebar-about')}<span>Local roots. Shared possibility.</span></div></aside><div class="main-shell"><header class="topbar"><button id="menu-toggle" class="menu-toggle" aria-label="Open navigation" aria-expanded="false">☰</button><span class="breadcrumb">Worldwide outreach <span>/</span> {e(label)}</span><div class="topbar-right"><span class="sync-label"><span></span>{e(data['meta']['mode'])}</span><a class="contact-link" href="mailto:{e(data['settings']['contact_email'])}">Contact Luke {icon('arrow')}</a></div></header><main id="main" tabindex="-1">{body}</main><footer><p>Luke Nathan Hayes · Aura of Intelligence</p><nav aria-label="Footer"><a href="sitemap.html">Site map</a><a href="licence.html">Licence</a><a href="privacy.html">Privacy</a><a href="https://github.com/auraofintelligence/outreach-cms">Source</a><button id="back-to-top" class="back-top">Back to top ↑</button></nav></footer></div><div class="nav-scrim" id="nav-scrim" hidden></div></body></html>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args()
    data=load_public(args.offline)
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    (OUT/'assets/data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
    for filename,_,_ in NAV:
        key=filename[:-5]
        (OUT/filename).write_text(frame(key,simple_page(key,data),data))
    pages={
      'privacy': ('Privacy and contact choices','<p>The website serves public project and directory information. It uses no analytics, advertising, tracking cookies or remote fonts. The invitation drafter runs in your browser and does not submit the fields to a server.</p><p>Choosing a source link opens that organisation’s website. Choosing to compose an email opens your email application. Those services apply their own terms.</p><p>Personal contacts, correspondence and permissions belong in the separate private workspace. The publication pipeline reads only the named public editorial tabs. Public place totals describe records cleared for publication.</p><p>Contact Luke to discuss an introduction, correction, sharing preference or withdrawal from future contact.</p>'),
      'sitemap':('Site map','<ul class="site-map">'+''.join(f'<li><a href="{f}">{label} {icon("arrow")}</a></li>' for f,label,_ in NAV)+'</ul><p><a href="licence.html">Licence</a> · <a href="privacy.html">Privacy</a> · <a href="docs/data-sources.html">Reference data and attribution</a></p>'),
      'licence':('Rights and reuse','<p>Original work copyright 2026 Luke Nathan Hayes / Strange But True / Aura of Intelligence.</p><p>The Strange But True Public Source Licence permits specified personal, educational, artistic, research, community and other non-commercial uses with attribution. Commercial, corporate, institutional and government uses require written permission. Third-party sources retain their own rights.</p><p><a href="LICENCE.md">Read the complete licence</a></p><p>The country and territory catalogue derives from Unicode CLDR. Its separate Unicode Licence V3 notice is preserved in the <a href="docs/data-sources.html">data-source record</a>.</p>')}
    for key,(title,body) in pages.items():
        (OUT/f'{key}.html').write_text(frame(key,f'<article class="prose"><p class="eyebrow">WORLDWIDE CONTACT SYSTEM</p><h1>{title}</h1>{body}</article>',data,title))
    (OUT/'404.html').write_text(frame('404','<article class="prose"><p class="eyebrow">PAGE NOT FOUND</p><h1>Let’s find the right route.</h1><p>This address does not lead to a page in the contact workbench.</p><a class="button" href="index.html">Return to the overview</a></article>',data,'Page not found').replace('<head>',f'<head><base href="{e(data["config"]["public_site_url"])}">',1))
    (OUT/'docs').mkdir(exist_ok=True)
    provenance=e((ROOT/'docs/data-sources.md').read_text())
    doc_html=frame('reference',f'<article class="prose"><h1>Reference data and attribution</h1><pre class="source-notice">{provenance}</pre></article>',data,'Reference data')
    doc_html=doc_html.replace('href="assets/','href="../assets/').replace('src="assets/','src="../assets/').replace('href="index.html"','href="../index.html"')
    for filename,_,_ in NAV: doc_html=doc_html.replace(f'href="{filename}"',f'href="../{filename}"')
    for x in ['sitemap','licence','privacy']:doc_html=doc_html.replace(f'href="{x}.html"',f'href="../{x}.html"')
    (OUT/'docs/data-sources.html').write_text(doc_html)
    shutil.copy2(ROOT/'LICENCE.md',OUT/'LICENCE.md')
    base=data['config']['public_site_url']
    urls=[f for f,_,_ in NAV]+[f'{k}.html' for k in pages]+['docs/data-sources.html']
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(base+url)}</loc></url>' for url in urls)+'</urlset>')
    (OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n')
    (OUT/'.nojekyll').touch()
    print(json.dumps({'output':str(OUT),'mode':data['meta']['mode'],'sources':len(data['sources']),'places':len(data['places']),'pages':len(urls)+1}))

if __name__=='__main__':main()

