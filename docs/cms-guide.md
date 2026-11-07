# Editing and operating the contact system

## Two workbooks

The **[Public CMS](https://docs.google.com/spreadsheets/d/1tntEkuyWQs4cPY-MPiSmvDq-K7cGT8AmxqsL3s22soU/edit)** is prepared for Viewer-by-link sharing, currently awaiting owner approval. Until sharing is enabled and the configured ID is activated, the website uses its labelled source snapshot. Once shared, everything in every tab can be read by a viewer, including rows marked `No`. Keep its contents suitable for public reading.

The **[Private Workspace](https://docs.google.com/spreadsheets/d/1Tapws8HTbiTlBk3-O0Og10QBzxoy0N6Yb3jpBzxJYKk/edit)** holds actual contacts, correspondence, permissions and community connections. Google account permissions control access. The public builder never reads this workbook. Its URL alone does not grant access.

Both workbooks belong to the Aura of Intelligence Google account and include a Guide tab. Tables have frozen headings, filters and dropdown choices. Add records inside the appropriate table or extend its range when necessary. The private record tables begin empty; format examples in the Guide are not contacts.

## Exact public columns

Keep these tab names, column order and header spelling. Do not add private fields to the public workbook.

| Tab | Columns, in order | Use |
| --- | --- | --- |
| Site | `key, value` | The keys `title`, `strapline`, `contact_email` only |
| Pages | `id, heading, body, publish` | Page headings and introductions |
| Projects | `id, title, theme, summary, url, invite, publish` | Connected work and invitation starting points |
| Sources | `id, name, theme, scope, summary, url, contact_route, checked_on, status, publish, project_ids` | Public routes to investigate |
| SisterLinks | `id, level, queensland_place, partner_place, country, relationship, year, source_url, contact_url, contact_route, checked_on, status, notes, publish` | Public council and state international relationships |
| Places | `code, name, region, stage, resident_contacts, communities, notes, publish` | Reference places and approved aggregate progress |

`publish` is exactly `Yes` or `No`. `No` omits the row from the generated website; it does not make the row private. A missing or invalid flag fails the import. Text is plain text and is escaped for HTML. Source and project links must use HTTPS, without embedded credentials.

Page IDs are `index`, `routes`, `places`, `sister-cities`, `projects`, `invite`, `playbook`, `workspace`. Omitting a Pages row uses the built-in heading for that page; a Pages row does not create or remove a page. Project and source IDs must remain stable and unique. Place codes are the existing two-letter reference codes.

Themes are `law`, `resilience`, `technology`, `cooperation`, `culture`, `civic`, `community`, `education`, `livelihoods`. Region labels are `Africa`, `Americas`, `Asia`, `Europe`, `Oceania`; source scope may also be `International` or `Australia`.

Source status choices are `Directory checked`, `Research route`, `Needs review`. Use `yyyy-mm-dd` for the checked date. A directory being accessible does not establish a local contact, suitability or independence. Record sourced affiliation and governance context in the private workspace as relevant.

Sources `project_ids` contains space-separated published project IDs. It controls the project filter and each card’s **Find outreach bodies** link. If you unpublish a project, remove its ID from source mappings in the same edit. Suggested matches do not imply the organisation has expressed interest.

SisterLinks uses `City` or `State` for level. Keep the precise official relationship label: a friendship agreement or MOU is not automatically a sister relationship. Enter a four-digit signing year only when explicit in a cited source; otherwise leave it blank. Both `source_url` and `contact_url` require HTTPS. Evidence status is `Listed by source`, `Needs confirmation`, `Historical`, `Suspended` or `Ended`. “Listed by source” describes the available evidence, not a confirmed active exchange. Explain conflicting or dated evidence in `notes`. The page shows public organisational routes only.

Place stages are `Seeking contacts`, `Route identified`, `In conversation`, `Resident connection`. The last stage requires at least one confirmed resident contact. Counts must be nonnegative whole numbers. Review private records and manually enter only approved aggregate counts in Places. No private names or messages are copied automatically.

## Private working records

| Tab | What belongs here |
| --- | --- |
| Contacts | Stable contact ID, person or organisation, resident place when known, self-described community, languages, relevant theme, appropriate channel, source, independence context, relationship stage, owner and next action |
| Outreach | One record per actual approach: contact ID, project ID, request, channel, message version, status, dates, response and next action |
| Permissions | Agreed purpose and scope, status, dates, evidence location, public attribution choices and notes |
| Communities | Self-described cultural and community names, languages, place codes, contact references, description and public listing preference |

Use stable contact IDs such as `contact-0001`; the Guide's sample format is not a real record. Keep dates as dates. Keep a current owner and next action. Mark an approach Sent only when it has actually been sent, and record withdrawals or declines so they inform later work.

## Publish a change

1. Edit the public CMS and confirm the changed rows have `publish = Yes`.
2. Wait for the six-hour refresh, or open **Actions → Publish website → Run workflow** on `main`.
3. Open the run. Both `build` and `deploy` must complete successfully.
4. Open the website Workspace page to see the mode, build time and publishing-run link.

Publishing runs on pushes to `main` as well. Scheduled jobs use UTC (`17 */6 * * *`); GitHub scheduling is best effort and may be delayed or disabled after repository inactivity. You can always run the workflow manually.

The weekly source-link report runs at `37 21 * * 0` UTC (Monday 07:37 in Brisbane). It checks source, project, sister-link evidence and council/state contact URLs and writes an Actions summary. Review the results before changing a source's status. A restricted response does not mean the organisation or contact has disappeared.

## Configuration and failure recovery

`cms.config.json` stores the public spreadsheet ID and workbook, repository and website URLs. `CMS_SPREADSHEET_ID`, when nonempty, overrides the configured spreadsheet ID. No Google credential or service-account secret is needed: the builder fetches only the intentionally public editorial workbook through Google's read-only CSV interface.

For initial activation after sharing approval, move `pending_spreadsheet_id` into `spreadsheet_id` in `cms.config.json` and run the publisher. For a replacement public CMS, copy the same tabs and exact columns, share the replacement as Viewer with anyone who has the link, then update `spreadsheet_id` and `cms_url`. Keep the private workbook restricted. Never point `spreadsheet_id` at a workbook containing private records.

The workflow fails before deployment if Google refuses access, a required header changes, the schema is invalid, or a check fails. The previous successful site remains live. Read the failed step's message, correct the CMS or code, then run publishing again. There is no silent fallback labelled as a fresh Google Sheets publication.

For offline development, use `python3 scripts/build.py --offline`. It builds `data/seed.json` and labels the result Source snapshot. To intentionally return production to that snapshot, remove the configured spreadsheet ID and any overriding repository variable in a reviewed change.

GitHub Pages uses **Settings → Pages → Source: GitHub Actions**. The publishing workflow grants only its deploy job Pages write and ID-token permissions; it does not have email credentials or a message-sending action.

## Reference data and rights

The 257 reference places include countries, territories and special reference codes. They do not imply statehood or cultural representation. Maintain Indigenous nations, languages and communities as people describe them, including connections spanning several places.

Preserve [data sources and Unicode attribution](data-sources.md), and the [Strange But True Public Source Licence](../LICENCE.md), when maintaining or reusing this project.
