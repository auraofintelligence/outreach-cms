# Public data sources

This catalogue supports discovery and locally relevant invitations. It contains public project descriptions, public organisational routes and a geographic reference list. It contains no imported university mailing list, personal contact database, correspondence or claimed partnerships.

## What the initial data means

- `projects` contains six connected project entry points. Each invitation is an editable starting request rather than a commitment or an appointment.
- `sources` contains sixteen public network or research routes. A route is not a confirmed local contact or an endorsement of this project.
- `places` contains 257 named Unicode CLDR reference places, with zero resident contacts and zero participating cultural communities initially recorded.
- `Seeking contacts` describes the absence of confirmed contact records in this seed. It does not claim that nobody in a place has heard of the projects.
- `publish: Yes` authorises the seed's public descriptions for website use. It does not authorise sending messages or adding private contact details.
- `checked_on` records review of the public source route on 31 October 2026. Each organisation's individual contact channel, present activity, English communication and willingness require their own checks.
- `Directory checked` means a public directory route was identified. `Research route` indicates an organisational entry point or source that requires further local discovery.
- “International” identifies a network's organising scope. It does not assert coverage of every country or culture.

Countries, territories, Indigenous nations, languages and cultural communities are different kinds of records. The geographic reference list is not a list of sovereign states, Indigenous nations or cultural representatives. Cultural community connections should be optional and self-described. Residence, diaspora connections and citizenship should remain separate when actual contacts are added to the private workspace.

The existing university lists mentioned by Luke remain an additional private discovery input. They have not been accessed or copied into this public seed.

## Geographic reference provenance

The geographic names and macroregion assignment derive from the Unicode Consortium's [CLDR JSON repository](https://github.com/unicode-org/cldr-json), retrieved on 31 October 2026. The supplemental files identify CLDR version 49 and Unicode version 16.0.0.

Repository main commit observed during retrieval: `7d2b9cb11cec08f4d333ad73209deb3df0711c3b`.

| Source file | Use | Retrieved Git blob SHA |
| --- | --- | --- |
| [English territory names](https://github.com/unicode-org/cldr-json/blob/7d2b9cb11cec08f4d333ad73209deb3df0711c3b/cldr-json/cldr-localenames-full/main/en/territories.json) | English place labels | `be20511f9b4b3230c09639e43c6a1ba532dc83b5` |
| [Territory information](https://github.com/unicode-org/cldr-json/blob/7d2b9cb11cec08f4d333ad73209deb3df0711c3b/cldr-json/cldr-core/supplemental/territoryInfo.json) | Named two-letter territory-code membership | `4bee3ddc0c987adcf4d66130c74fb1e973a314d6` |
| [Territory containment](https://github.com/unicode-org/cldr-json/blob/7d2b9cb11cec08f4d333ad73209deb3df0711c3b/cldr-json/cldr-core/supplemental/territoryContainment.json) | Official CLDR macroregion containment | `bdb7c2a8a20d164ea54ab2319b5e0aa85d1d8207` |

Transformation:

1. Take two-letter uppercase codes in `supplemental.territoryInfo`.
2. Exclude `ZZ`, the unknown-region record, and require an English territory label.
3. Resolve containment recursively under CLDR's Africa `002`, Americas `019`, Asia `142`, Europe `150` and Oceania `009` macroregions.
4. Keep the place code and English name. Sort by English place name.
5. Initialise `stage` to `Seeking contacts`; initialise `resident_contacts` and `communities` to numeric zero.

All 257 included codes have a resolved macroregion. CLDR containment places some special areas within its “Outlying Oceania” grouping; macroregion labels reproduce that data convention rather than a fresh geographic or political judgement. Special reference territory codes include Ascension Island, Clipperton Island, Diego Garcia, Ceuta and Melilla, the Canary Islands, Tristan da Cunha, Sark and Kosovo. The catalogue may be extended with other place or community records without treating a single official code list as the complete map of human cultures.

Population, language percentages, GDP and literacy fields from `territoryInfo` were not copied into this project.

## Public organisational routes

- **Grassroots Justice Network**: [official route](https://grassrootsjusticenetwork.org/connect/organizations/). Directory checked. International.
- **GNDR**: [official route](https://www.gndr.org/network/find-a-member/). Directory checked. International.
- **Association for Progressive Communications**: [official route](https://www.apc.org/en/about-apc). Research route. International.
- **Internet Society chapters**: [official route](https://www.internetsociety.org/chapters/). Directory checked. International.
- **Asia Indigenous Peoples Pact**: [official route](https://aippnet.org/). Research route. Asia.
- **Indigenous Peoples of Africa Co-ordinating Committee**: [official route](https://www.ipacc.org.za/). Directory checked. Africa.
- **Global Voices and Rising Voices**: [official route](https://globalvoices.org/about/). Research route. International.
- **Wikimedia affiliates and user groups**: [official route](https://meta.wikimedia.org/wiki/Wikimedia_Affiliates). Directory checked. International.
- **URI Cooperation Circles**: [official route](https://www.uri.org/who-we-are/cooperation-circles). Directory checked. International.
- **WFUNA national associations**: [official route](https://wfuna.org/una/). Directory checked. International.
- **Rotary and Rotaract clubs**: [official route](https://www.rotary.org/get-involved/our-clubs). Research route. International.
- **Toastmasters club finder**: [official route](https://www.toastmasters.org/find-a-club). Directory checked. International.
- **Servas groups**: [official route](https://servas.org/servas-group-websites). Directory checked. International.
- **TESOL affiliate associations**: [official route](https://www.tesol.org/tesol-global-community/affiliates/find-an-affiliate/). Directory checked. International.
- **IATEFL teaching associations**: [official route](https://www.iatefl.org/iatefl-associates/). Research route. International.
- **Co-operative and local trade networks**: [official route](https://www.ica.coop/en/our-members/search-our-members). Research route. International.

The Grassroots Justice Network states that its organisation entries are crowdsourced and unverified. Use a listing to find an organisation's own appropriate public enquiry route. Its site terms restrict collecting or storing other users' personal information, so this catalogue does not contain copied member profiles or personal contact details.

AIPP and IPACC are regional sources. Additional community-controlled organisations must be identified for other regions. A network label or an institutional affiliation does not establish an organisation's independence, a person's freedom to participate, English ability or consent to be contacted.

The ICA directory is an additional research route for co-operative organisations. It does not establish a partnership with Ready SET Co-op, and it is not a general directory of local tradespeople.

## Connected project sources

- **Your Relevance in every jurisdiction**: [public project](https://auraofintelligence.github.io/australian-law-2012-lukes-relevance/pages/your-relevance.html).
- **Aura Disaster Resilience**: [public project](https://auraofintelligence.github.io/aura-disaster-resilience/).
- **Installing the Missing Middle**: [public project](https://auraofintelligence.github.io/installing-the-missing-middle/).
- **A fair go in the age of intelligence**: [public project](https://auraofintelligence.github.io/UNGA81-Luke-Hayes/).
- **GAJRA Earth Infinity**: [public project](https://auraofintelligence.github.io/GAJRA-earth-infinity/).
- **P4A Australia**: [public project](https://p4a.xyz/).
- **Australian Legal Engine**: [source project](https://github.com/auraofintelligence/australian-legal-engine).
- **GAJRA Earth Claude**: [public project](https://auraofintelligence.github.io/gajra-earth-claude-build/).
- **GAJRA Earth Community**: [public hub](https://auraofintelligence.github.io/gajra-earth-public-hub/).
- **Aura Genesis**: [Genesis Protocol guide](https://auraofintelligence.github.io/aura-genesis-geode-atlas/).
- **Aura Tourism**: [public project](https://auraofintelligence.github.io/aura-tourism/).
- **Joyful Responsible Abundance**: [public project](https://auraofintelligence.github.io/joyful-responsible-abundance/index.html).
- **Mutual Futures**: [public project](https://auraofintelligence.github.io/mutual-futures/).
- **Aura Children & Young People**: [public project](https://auraofintelligence.github.io/aura-child-services/).
- **Aura Whole-of-Life Support**: [public project](https://auraofintelligence.github.io/aura-whole-of-life/).
- **Verse Box**: [public project](https://auraofintelligence.github.io/aura-verse-box/).
- [Author's open record](https://github.com/auraofintelligence/open-record-luke-nathan-hayes).
- [P4A Oceania](https://auraofintelligence.github.io/p4a-oceania-cinema/).
- [P4A Native Nations](https://auraofintelligence.github.io/p4a-native-nations-cinema/).
- [GAJRA Earth original site](https://gajra.earth/) and [public hub](https://auraofintelligence.github.io/gajra-earth-public-hub/) retain their own editions and histories.

The UNGA81 contribution is Luke Nathan Hayes's personal contribution. The public project links do not imply an external organisation's endorsement.

## Unicode data licence

The derived geographic catalogue retains the following [Unicode licence](https://github.com/unicode-org/cldr-json/blob/7d2b9cb11cec08f4d333ad73209deb3df0711c3b/LICENSE). This notice accompanies the derived data; the project's own licence does not replace third-party data terms.

```text
UNICODE LICENSE V3

COPYRIGHT AND PERMISSION NOTICE

Copyright © 2015-2024 Unicode, Inc.

NOTICE TO USER: Carefully read the following legal agreement. BY
DOWNLOADING, INSTALLING, COPYING OR OTHERWISE USING DATA FILES, AND/OR
SOFTWARE, YOU UNEQUIVOCALLY ACCEPT, AND AGREE TO BE BOUND BY, ALL OF THE
TERMS AND CONDITIONS OF THIS AGREEMENT. IF YOU DO NOT AGREE, DO NOT
DOWNLOAD, INSTALL, COPY, DISTRIBUTE OR USE THE DATA FILES OR SOFTWARE.

Permission is hereby granted, free of charge, to any person obtaining a
copy of data files and any associated documentation (the "Data Files") or
software and any associated documentation (the "Software") to deal in the
Data Files or Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, and/or sell
copies of the Data Files or Software, and to permit persons to whom the
Data Files or Software are furnished to do so, provided that either (a)
this copyright and permission notice appear with all copies of the Data
Files or Software, or (b) this copyright and permission notice appear in
associated Documentation.

THE DATA FILES AND SOFTWARE ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF
THIRD PARTY RIGHTS.

IN NO EVENT SHALL THE COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE
BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES,
OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THE DATA
FILES OR SOFTWARE.

Except as contained in this notice, the name of a copyright holder shall
not be used in advertising or otherwise to promote the sale, use or other
dealings in these Data Files or Software without prior written
authorization of the copyright holder.

SPDX-License-Identifier: Unicode-3.0
```


Sidebar project doorways: [Aura of Intelligence](https://auraofintelligence.github.io/) and [Strange But True](https://auraofintelligence.github.io/strange-but-true/).


## Additional outreach routes — checked 7 November 2026

Added 24 bodies and networks for the connected projects: CREATE, SNAICC, FICE, ADI, DAI, Dementia Australia development, PWDA research, ARATA, ATSA, PIANGO, Pacific Disability Forum, Local Contexts, Engagement Institute, Ecotourism Australia, IITOQ, WFTGA, ALIA Digital Literacy, Employee Ownership Australia, BCCM, ALTA, Free Access to Law member discovery, Social Enterprise Australia, ACM SIGCHI and IEEE SSIT. The directory also links to the Queensland international-relations register, taking the public route total to 41.

Official URLs, published organisational routes, suggested project fit and material limitations are recorded in [the outreach research record](outreach-research-2026-11-07.json). Suggested fit is our research judgement; it is not interest or endorsement from those bodies. Individual member destinations and message delivery have not all been tested. Research did not send outreach, create partnerships or change resident contact totals.

Current checks corrected IAP2 Australasia's trading name to Engagement Institute. XR Access was excluded as an active enquiry because its official hibernation notice says its general mailbox is no longer actively monitored from January 2026. Relevant fees, eligibility and co-development terms remain visible in each body's contact guidance.

## Queensland international links — checked 7 November 2026

The register covers Brisbane, Gold Coast, Sunshine Coast, Logan, Ipswich, Redlands, Moreton Bay, Toowoomba, Townsville, Cairns, Mackay, Rockhampton, Bundaberg, Fraser Coast and Gladstone, plus Queensland state. Its 83 records comprise 78 council-level relationships of several kinds and five sister-state agreements. Every record has official evidence and a responsible council or state contact route. This is a selected Queensland register, not an exhaustive list of every local government relationship.

The [full research record](queensland-international-links-research-2026-11-07.json) retains agreement labels, additional sources, source conflicts, pending announcements and historical state arrangements. Those historical arrangements and the separately announced Shizuoka MOU are not counted in the published 83. No current suspension or termination was established in the checked official sources; that is not proof that every programme is active.

Queensland's June 2026 DPC protocol guide, section 1.9 (PDF page 29), lists Shanghai, Saitama, Central Java, Gyeonggi and South Carolina as sister states. Historical Texas, Nevada and North Rhine Westphalia references remain in the research record with current status unverified.

Nine published council records are labelled Needs confirmation: Sunshine Coast's four links, Rockhampton's Zhenjiang and Huizhou links, and Fraser Coast's Otsuki, Honiara and Tome/Nakada classifications. Sunshine Coast's indexed list returned 404; its recent annual report corroborates Tatebayashi and Xiamen, while latest agreement terms need confirmation. Fraser Coast's current programme and published policy use different classifications. Individual notes explain these limits. Contact the council before treating a dated or conflicting record as an active formal sister agreement.

Other distinctions preserved include Redlands' friendship, cultural/education and MOU agreements; Moreton Bay's Sanyo-Onoda transition to friendship; Townsville's specific Foshan friendship description; and Gold Coast's Ancient Olympia sister agreement announced in September 2026. Country and territory wording follows the evidence with obvious spelling corrections; it is not a statehood claim. English-language access and institutional independence are not inferred from an official relationship.
