import copy
import csv
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from cms import FIELDS, ROOT, rows_from_csv, safe_url, validate, load_public
from build import source_card, sister_row

class PublicationTests(unittest.TestCase):
    def cms_fixture(self, root):
        data=json.loads((ROOT/'data/seed.json').read_text())
        (root/'cms.config.json').write_text(json.dumps({'spreadsheet_id':'public_editorial_sheet_12345','repository_url':'https://github.com/auraofintelligence/outreach-cms','public_site_url':'https://auraofintelligence.github.io/outreach-cms/'}))
        rows={'Site':[{'key':k,'value':v} for k,v in data['settings'].items()],
              'Pages':data.get('pages',[]),'Projects':data['projects'],'Sources':data['sources'],'Places':data['places'],'SisterLinks':data['sister_links']}
        def response(request,timeout):
            params=parse_qs(urlparse(request.full_url).query)
            tab=params['sheet'][0]
            self.assertEqual(params['headers'],['1'])
            stream=io.StringIO();writer=csv.DictWriter(stream,fieldnames=FIELDS[tab]);writer.writeheader()
            for row in rows[tab]:
                row=dict(row)
                if 'publish' in FIELDS[tab]:row.setdefault('publish','Yes')
                writer.writerow(row)
            return io.BytesIO(stream.getvalue().encode())
        return response

    def test_configured_cms_reads_only_the_six_public_tabs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);response=self.cms_fixture(root)
            with patch('cms.ROOT',root),patch.dict(os.environ,{'CMS_SPREADSHEET_ID':''}),patch('cms.urlopen',side_effect=response) as request:
                data=load_public()
            self.assertEqual(data['meta']['mode'],'Google Sheets')
            self.assertEqual(request.call_count,6)
            self.assertEqual({parse_qs(urlparse(c.args[0].full_url).query)['sheet'][0] for c in request.call_args_list},set(FIELDS))
            self.assertEqual(len(data['places']),257)

    def test_configured_cms_failure_does_not_silently_publish_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.cms_fixture(root)
            with patch('cms.ROOT',root),patch.dict(os.environ,{'CMS_SPREADSHEET_ID':''}),patch('cms.urlopen',side_effect=OSError('CMS unavailable')):
                with self.assertRaises(OSError):load_public()

    def test_private_tabs_are_never_public_sources(self):
        for tab in ['Contacts','Outreach','Permissions','Communities','Private']:
            with self.assertRaises(ValueError):rows_from_csv('name,email\nA,a@example.com',tab)

    def test_schema_rejects_extra_contact_fields(self):
        headers=FIELDS['Sources']+['email']
        with self.assertRaises(ValueError):rows_from_csv(','.join(headers)+'\n','Sources')

    def test_unpublished_rows_are_excluded(self):
        self.assertEqual(rows_from_csv('id,heading,body,publish\nprivate,Hidden,Do not publish,No\nready,Visible,Ready,Yes\n','Pages'),[{'id':'ready','heading':'Visible','body':'Ready','publish':'Yes'}])

    def test_invalid_publication_flag_fails_closed(self):
        with self.assertRaises(ValueError):rows_from_csv('id,heading,body,publish\nx,Title,Text,Maybe\n','Pages')

    def test_unsafe_links_are_rejected(self):
        for url in ['javascript:alert(1)','http://example.com','https://user:pass@example.com','https://example.com\nX: a']:
            with self.assertRaises(ValueError):safe_url(url)

    def test_source_text_is_escaped(self):
        row=copy.deepcopy(json.loads((ROOT/'data/seed.json').read_text())['sources'][0])
        row['name']='<script>alert(1)</script>'
        output=source_card(row)
        self.assertNotIn('<script>',output)
        self.assertIn('&lt;script&gt;',output)

    def test_project_routes_reject_unknown_project_references(self):
        data=json.loads((ROOT/'data/seed.json').read_text())
        data['sources'][0]['project_ids']='unpublished-or-unknown-project'
        with self.assertRaisesRegex(ValueError,'published projects'):validate(data)

    def test_sister_links_reject_private_fields_and_unsafe_evidence(self):
        for field,value in [('private_contact','A person'),('source_url','javascript:alert(1)'),('contact_url','http://example.com')]:
            data=json.loads((ROOT/'data/seed.json').read_text());data['sister_links'][0][field]=value
            with self.assertRaises(ValueError):validate(data)

    def test_sister_links_require_explicit_years_and_evidence_status(self):
        for field,value in [('year','probably 1990'),('status','Confirmed participating residents'),('level','Private')]:
            data=json.loads((ROOT/'data/seed.json').read_text());data['sister_links'][0][field]=value
            with self.assertRaises(ValueError):validate(data)

    def test_sister_evidence_notes_are_escaped_and_uncertainty_is_visible(self):
        row=copy.deepcopy(json.loads((ROOT/'data/seed.json').read_text())['sister_links'][0])
        row.update(notes='<script>untrusted</script>',status='Needs confirmation',year='')
        output=sister_row(row)
        self.assertNotIn('<script>',output)
        self.assertIn('&lt;script&gt;',output)
        self.assertIn('Needs confirmation',output)
        self.assertIn('Signing year not verified',output)

    def test_resident_stage_requires_confirmed_total(self):
        data=json.loads((ROOT/'data/seed.json').read_text());data['places'][0]['stage']='Resident connection'
        with self.assertRaises(ValueError):validate(data)

    def test_duplicate_reference_places_are_rejected(self):
        data=json.loads((ROOT/'data/seed.json').read_text());data['places'].append(copy.deepcopy(data['places'][0]))
        with self.assertRaises(ValueError):validate(data)

    def test_snapshot_has_no_fabricated_resident_contacts(self):
        data=load_public(offline=True)
        self.assertEqual(sum(p['resident_contacts'] for p in data['places']),0)
        self.assertTrue(all(p['stage']=='Seeking contacts' for p in data['places']))

if __name__=='__main__':unittest.main()
