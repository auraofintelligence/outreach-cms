# Working on the outreach website

Use Australian English and the user's connected project sources. Use Ready SET Co-op in new content. Preserve the Strange But True Public Source Licence and the Unicode data attribution.

Google Sheets is the editorial CMS. `cms.config.json` identifies the public-content workbook. `scripts/cms.py` reads only the fixed public tabs and validates their exact columns. Private contacts, correspondence, consent and outreach authorisations belong in the separate private workbook. Never put private spreadsheets, credentials, CSV exports or contact records in this repository or a Pages artifact.

Keep directory availability, an organisation's audience, actual resident contacts and cultural participation distinct. Preserve source dates and uncertainty. Do not fabricate partnerships, contacts, sent emails or country representatives. A reference place is not a claim about statehood or cultural representation.

Website content is plain text. Escape it for HTML; do not add a CMS HTML execution path. Keep URL validation and publication filtering. The invitation tool prepares a local draft; GitHub Actions must not send messages.

Run `python3 -m unittest discover -s tests -v` and `python3 scripts/build.py` before publication. Test privacy boundaries and user behaviour when changing them. Build output goes in `.site/`; GitHub Pages publishes it through the `Publish website` workflow.

