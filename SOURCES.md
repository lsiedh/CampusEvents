# Sources

This file tracks where events come from, their current status, and any parsing notes.

This file owns source inventory only. Scope definition belongs in [README.md](/Users/scelsenus/Desktop/CampusEvents/README.md), architecture in [ARCHITECTURE.md](/Users/scelsenus/Desktop/CampusEvents/ARCHITECTURE.md), and status tracking in [PROGRESS.md](/Users/scelsenus/Desktop/CampusEvents/PROGRESS.md).

Statuses used in this document:

- `seed`: found in the provided source file but not yet validated
- `candidate`: looks promising and should be evaluated
- `validated`: confirmed usable for event ingestion
- `rejected`: not suitable for the digest

## Seed Sources From `RSS Feeds.txt`

| Institution | Source | Type | Status | Notes |
| --- | --- | --- | --- | --- |
| NUS | `https://myaces.nus.edu.sg/CoE/jsp/coeGenRss.jsp?Cat=0` | RSS | candidate | Official RSS endpoint is listed on the live NUS Calendar of Events subscription page, but direct fetch still needs parser-level confirmation |
| NTU | `http://www.rsis.edu.sg/feed/?post_type=event` | RSS | validated | Confirmed by RSIS RSS help page as the official events feed |
| NUS | `https://nusync.nus.edu.sg/ics_helper?TB_context=Subscribe_To_Calendars&TB_iframe=true&embed=1&height=550&modal=true&mode=set&width=850` | ICS helper page | candidate | Main helper page still needs extraction of the actual ICS endpoint; NUSync itself exposes public event pages |
| NUS | `https://myaces.nus.edu.sg/CoE/jsp/coeRss.jsp` | RSS directory page | validated | Live subscription page lists category feeds for Arts, Seminars, Exhibitions, Lectures, Social, and Sports |

## Candidate NUS Sources

| Source | Type | Status | Notes |
| --- | --- | --- | --- |
| `https://nus.edu.sg/events` | HTML portal | candidate | University-level events page |
| `https://www.nus.edu.sg/events` | HTML portal | candidate | Duplicate domain variant of the main portal |
| `https://nus.edu.sg/osa/events` | HTML portal | candidate | Equivalent to the working `osa.nus.edu.sg/events/` page; prefer the latter as canonical source |
| `https://nus.edu.sg/uci/sports-and-recreation` | HTML portal | candidate | Sports-related events may be relevant |
| `https://nus.edu.sg/nusync/events` | HTML portal | candidate | NUSync has public event pages, but canonical URLs appear under `nusync.nus.edu.sg` and may need care around auth and scraping |
| `https://enterprise.nus.edu.sg/events` | HTML portal | candidate | Entrepreneurship speaking and networking events |
| `https://nuscollege.nus.edu.sg/events` | HTML portal | candidate | College event listings may contain talks |
| `https://nus.edu.sg/oam/events` | HTML portal | candidate | Public engagement and outreach events possible |
| `https://science.nus.edu.sg/events` | HTML portal | candidate | Search results show valid science event pages, but the canonical listing appears fragmented across subpages rather than one stable index |
| `https://chemistry.nus.edu.sg/events` | HTML portal | candidate | Live events page exists, but it is mostly outreach, olympiad, camp, and open-house information rather than a broad ongoing seminar feed |
| `https://physics.nus.edu.sg/events` | HTML portal | candidate | Physics publishes event detail pages, but a stable all-events index still needs confirmation |
| `https://math.nus.edu.sg/events` | HTML portal | validated | Mathematics publishes event-series and conference pages under a stable events section; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://ims.nus.edu.sg/events` | HTML portal | candidate | Institute events |
| `https://stat.nus.edu.sg/events` | HTML portal | candidate | Department events |
| `https://cde.nus.edu.sg/events` | HTML portal | candidate | College-level event listing |
| `https://cee.nus.edu.sg/events` | HTML portal | candidate | Engineering events |
| `https://me.nus.edu.sg/events` | HTML portal | candidate | Engineering events |
| `https://www.comp.nus.edu.sg/events` | HTML portal | candidate | Search results skew toward event recaps and community posts; not yet confirmed as a strong forward-looking events feed |
| `https://bschool.nus.edu.sg/news-events/events` | HTML portal | candidate | Business school events |
| `https://law.nus.edu.sg/events` | HTML portal | candidate | Event pages exist, but many visible results are old or invitation-only; needs a pass to determine current usefulness |
| `https://ystmusic.nus.edu.sg/whats-on` | HTML portal | candidate | Concerts and public performances |
| `https://fass.nus.edu.sg/events` | HTML portal | validated | Live event taxonomy pages expose dated talks, workshops, festivals, and registration metadata; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://fass.nus.edu.sg/cs/events` | HTML portal | candidate | Department-specific events |
| `https://sph.nus.edu.sg/events` | HTML portal | validated | Live event detail pages include date, time, platform, and synopsis for public health talks and conferences; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://medicine.nus.edu.sg/cbme/events` | HTML portal | candidate | Ethics events |
| `https://medicine.nus.edu.sg/cbme/seminars-workshops-conferences` | HTML portal | candidate | Seminar-focused listing |
| `https://csi.nus.edu.sg/events` | HTML portal | candidate | Research institute events |
| `https://ari.nus.edu.sg/events` | HTML portal | candidate | Asia Research Institute events |
| `https://ca2dm.nus.edu.sg/events` | HTML portal | candidate | Research seminars |
| `https://cfpr.nus.edu.sg/events` | HTML portal | candidate | Centre events |

## Candidate NUS Arts, Performance, Museum, Gallery, And Athletics Sources

| Source | Type | Status | Notes |
| --- | --- | --- | --- |
| `https://osa.nus.edu.sg/events/` | HTML portal | validated | Strong source with filters for Arts, Sports, For Public, and upcoming date ranges; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://osa.nus.edu.sg/nusartsfestival/` | HTML festival site | validated | Live festival calendar includes dated performances by genre with individual event detail pages; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://museum.nus.edu.sg/` | HTML museum site | validated | Homepage exposes current events and exhibitions with event cards and dates; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://museum.nus.edu.sg/explore/about/` | Museum info page | candidate | Confirms museum role and public-facing gallery programming on campus |
| `https://babahouse.nus.edu.sg/` | HTML heritage site | validated | Homepage exposes current events and exhibitions and links to programmes and tours; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://babahouse.nus.edu.sg/explore/programmes/heritage-tours/` | HTML programme page | candidate | Heritage tours are event-like and publicly bookable |
| `https://babahouse.nus.edu.sg/explore/programmes/saturdays-at-nus-baba-house/` | HTML programme page | candidate | Recurring cultural programmes and thematic public activities |
| `https://lkcnhm.nus.edu.sg/` | HTML museum site | validated | Homepage includes “What’s on” plus tours and workshops sections suitable for cultural event discovery; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| `https://ystmusic.nus.edu.sg/whats-on` | HTML performance listing | candidate | High-value performing arts source from the seed list, but this specific page still needs direct parser validation |
| `https://osa.nus.edu.sg/event/inter-faculty-games-ifg/` | HTML event page | candidate | Signature NUS athletics event; useful pattern for sports listings |
| `https://osa.nus.edu.sg/event/inter-faculty-games-2024/` | HTML event page | candidate | Sports event detail template with date, venue, organiser, and audience fields |
| `https://valourhouse.nus.edu.sg/event/` | HTML event archive | candidate | Sports-themed residential cluster event listings; may contain public or semi-public sports events |
| `https://osa.nus.edu.sg/experience-communities/sports/` | HTML sports hub | candidate | Useful discovery page for TeamNUS and Sports Club flagship events, but not itself a strong canonical event feed |
| `https://uci.nus.edu.sg/campus-life/campus-services/sports-recreation/happenings/` | HTML page | rejected | Mostly training schedules and club sessions rather than digest-worthy public events |

## Candidate NTU Sources

| Source | Type | Status | Notes |
| --- | --- | --- | --- |
| `https://www.ntu.edu.sg/news-and-events` | HTML portal | candidate | Main NTU event/news entry point |
| `https://www.ntu.edu.sg/events` | HTML portal | validated | Live NTU event portal is reachable and uses structured event filters on the page |
| `https://www.ntu.edu.sg/openhouse` | HTML portal | candidate | Probably occasional, may not belong in digest |
| `https://www.ntu.edu.sg/library/news-and-events` | HTML portal | candidate | Library programs and talks |
| `https://www.ntu.edu.sg/engineering/news-and-events/events` | HTML portal | candidate | College-level event listing |
| `https://www.ntu.edu.sg/mae/news-events/events` | HTML portal | validated | Event detail pages include date, venue, audience, seminar metadata, and add-to-calendar support |
| `https://www.ntu.edu.sg/mae/research/knowledge-portal/research-seminars-events` | HTML portal | candidate | Research seminar source |
| `https://www.ntu.edu.sg/cceb/news-and-events/seminars-and-lecture-series` | HTML portal | validated | Strong seminar hub linking multiple seminar families with event detail pages and add-to-calendar metadata; automation now uses the school’s live `GetEvents` feed for safer recurring ingestion |
| `https://www.ntu.edu.sg/cceb/news-and-events/events` | HTML portal | candidate | School events |
| `https://www.ntu.edu.sg/sbs/news-events/events` | HTML portal | validated | Earlier URL now returns HTTP 404; use `https://www.ntu.edu.sg/sbs/news-and-events/events` as the working canonical replacement for automation |
| `https://www.ntu.edu.sg/mse/news-events/events` | HTML portal | candidate | Materials science events |
| `https://www.ntu.edu.sg/eee/news-and-events` | HTML portal | candidate | EEE exposes event-tagged pages and hackathons, but search results currently skew toward news recaps instead of a clean events index |
| `https://www.ntu.edu.sg/cee/news-and-events/events` | HTML portal | validated | Earlier URL now returns HTTP 404; use `https://www.ntu.edu.sg/cee/news-events/events?listingKeyword=&categories=all&interests=all&audiences=all&page=1` as the working canonical replacement for automation |
| `https://www.ntu.edu.sg/business/news-and-events/events` | HTML portal | candidate | Business school pages surface workshop stories and events, but the clean canonical event listing needs more validation |
| `https://www.ntu.edu.sg/ias/events` | HTML portal | validated | Search results confirm dedicated IAS event detail pages with dates, audiences, categories, and public-facing metadata; automation now uses the page’s live `GetEvents` feed |
| `https://www.ntu.edu.sg/research-seminars` | HTML portal | candidate | Central seminar page |
| `https://www.ntu.edu.sg/engineering/research-seminars` | HTML portal | candidate | Engineering seminar page |

## Candidate NTU Arts, Performance, Museum, Gallery, And Athletics Sources

| Source | Type | Status | Notes |
| --- | --- | --- | --- |
| `https://www.ntu.edu.sg/life-at-ntu/museum` | HTML museum site | candidate | NTU Museum homepage includes current exhibitions, workshops, and public art programming |
| `https://www.ntu.edu.sg/life-at-ntu/museum/exhibitions` | HTML museum listing | validated | Page explicitly lists ongoing and upcoming exhibitions, workshops, and other events |
| `https://www.ntu.edu.sg/life-at-ntu/museum/collection` | HTML collection page | candidate | Useful for campus art trail and museum-linked event discovery |
| `https://www.ntu.edu.sg/museum/on-the-cusp` | HTML event/exhibition page | candidate | Example of a campus-wide NTU Museum exhibition with strong structured metadata |
| `https://admgallery.sg/` | HTML gallery site | candidate | Known NTU-campus gallery, but direct fetch still needs confirmation before promoting |
| `https://admgallery.sg/exhibitions/` | HTML gallery listing | candidate | High-value gallery source, but direct fetch still needs confirmation before promoting |
| `https://www.ntu.edu.sg/chc` | HTML museum/centre site | candidate | Homepage confirms exhibitions, public lectures, seminars, conferences, and outreach, but a stable listing page is still needed |
| `https://www.ntu.edu.sg/chc/CHC-Museum/nantah-pictorial-exhibition` | HTML exhibition page | candidate | Example of a stable exhibition detail page on campus |
| `https://www.ntu.edu.sg/chc/CHC-Museum/guided-tours` | HTML programme page | candidate | Guided tours may qualify as public cultural events |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/clubs-groups-societies/ntu-students-union-council/cultural-activities-club` | HTML org page | candidate | Discovery source for performing arts groups and major culture programmes, though not itself an event feed |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/sports` | HTML sports hub | candidate | Useful discovery page for varsity and recreational programmes, but not yet a canonical event listing |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/sports/sports-excellence` | HTML sports hub | candidate | Good source for official varsity competition calendars and sports event families |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/sports/sports-excellence/sunig` | HTML competition page | candidate | Singapore University Games timing and competition metadata |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/sports/sports-excellence/ivp` | HTML competition page | candidate | Institute-Varsity-Polytechnic Games timing and competition metadata |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/student-activities-and-engagement/sports/sports-for-all` | HTML sports page | candidate | Recreational sports discovery source; may reveal public-facing novice competitions and workshops |
| `https://www.ntu.edu.sg/life-at-ntu/student-life/clubs-groups-societies/ntu-students-union-council/sports-club` | HTML org page | candidate | Discovery source for Sports Club flagship events; not a direct event feed |

## Campus-Based Institutes And Agencies Beyond Core University Departments

These are important because some event-rich organisations are hosted on campus, partnered with the universities, or physically located on campus without fitting neatly under a faculty or school site.

| Campus | Organisation | Source | Type | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| NTU | SCELSE | `https://scelse.sg/news-events/all-events/` | HTML portal | validated | Live event page with category filters including conferences, seminar series, talks, presentations, outreach, and webinars |
| NTU | SCELSE | `https://scelse.sg/about/who-we-are/` | About page | candidate | Confirms SCELSE is hosted at NTU and has shared NUS space |
| NTU | ERI@N | `https://www.ntu.edu.sg/erian/news-events` | HTML portal | validated | News & Events page exposes upcoming events and links to a dedicated all-events listing; automation now uses the institute’s live `GetEvents` feed |
| NTU | IAS | `https://www.ntu.edu.sg/ias/events` | HTML portal | validated | Dedicated event records are visible in current search results and include event metadata suitable for parsing; automation now uses the page’s live `GetEvents` feed |
| NUS | NERI | `https://www.nus.edu.sg/neri/events/eventsgallery/` | HTML portal | candidate | Event gallery is live and useful, but it appears archive-heavy; prefer an upcoming-events page if available |
| NUS | CQT | `https://www.cqt.sg/` | Mixed site | candidate | Site is live and exposes Upcoming Events and Event Calendar navigation; use the direct upcoming-events page for parsing |
| NUS | CQT | `https://www.cqt.sg/upcoming-events/` | HTML portal | validated | Direct upcoming-events page is live and should be preferred over the homepage; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| NUS | SMART | `https://smart.mit.edu/` | Mixed site | candidate | Live site confirms SMART at CREATE and has News and Events sections, but direct upcoming event extraction needs more validation |
| NUS | MBI | `https://mechanobio.info/` | Mixed site | rejected | Domain currently appears compromised and is not safe to treat as an official source |
| NUS | MBI | `https://www.mbi.nus.edu.sg/mbi-seminar-workshop-series/` | HTML portal | validated | Canonical NUS-hosted MBI page lists seminar series, workshops, conferences, and current event links; currently inactive in the automation registry because live fetches return an Incapsula challenge page |
| NUS | SNRSI | `https://snrsi.nus.edu.sg/` | Mixed site | rejected | Institute homepage is live, but no clear public events or seminar listing was found in the first validation pass |

## Discovery Heuristic For Non-Department Sources

- Include campus-based institutes, research centres of excellence, CREATE partners, corporate labs, national research institutes, and joint centres located on NTU or NUS campuses.
- Prefer organisations with a stable events, news-events, seminars, or calendar page.
- Record whether the organisation is university-governed, university-hosted, or an external partner physically located on campus.
- Keep these sources separate from faculty and school pages because their ownership and update patterns are different.

## Source Selection Rules

- Prefer machine-readable feeds over HTML-only pages when event quality is comparable.
- Prefer official university, faculty, school, institute, and center pages over third-party calendars.
- Reject sources that are mostly classes, student club logistics, or authenticated-only listings.
- Record whether each source needs RSS parsing, HTML scraping, or calendar parsing.
- Record duplication relationships so the same event is not ingested from multiple portals unnecessarily.

## Change Log

### 2026-03-16

- Seeded this file from the provided [RSS Feeds.txt](/Users/scelsenus/Desktop/CampusEvents/RSS%20Feeds.txt).
- Added candidate university, faculty, school, and institute event pages listed in the provided file.
- Added a dedicated category for campus-based institutes and agencies beyond core university departments, including SCELSE-like organisations.
- Expanded the inventory with arts, performance, museum, gallery, and athletics sources on both campuses.
- Completed a first validation pass for seed feeds, central event pages, arts and museum pages, and major institute sources.
- Confirmed that `https://www.ntu.edu.sg/sbs/news-events/events` and `https://www.ntu.edu.sg/cee/news-and-events/events` return HTTP 404, then promoted working replacement URLs for SBS and CEE after direct live checks.
- Confirmed that the currently inactive NUS HTML sources remain blocked by Incapsula from the automation environment, and no documented alternate machine-readable feed has been promoted yet.
- Confirmed that likely alternate machine-readable paths for the inactive NUS HTML sources, including common WordPress `wp-json` routes on OSA, NUS Museum, FASS, and SSHSPH, are also blocked by the same Incapsula challenge from the automation environment.
