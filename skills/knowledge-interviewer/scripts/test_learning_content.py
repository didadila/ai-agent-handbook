"""Public lookup covers every stable point and rejects cross-domain IDs."""
import json
import re
import unittest
from learning_content import ROOT, locate


class PublicContentTest(unittest.TestCase):
    def test_every_point_resolves_to_a_real_heading_and_section(self):
        catalog = json.loads((ROOT / 'catalog.json').read_text())
        for domain in catalog['domains']:
            name = domain['id']
            text = (ROOT / 'skills/knowledge-interviewer/references/domains' / name / 'map.md').read_text()
            ids = set(re.findall(r'^\|\s*`([^`]+)`\s*\|', text, re.M))
            for point in ids:
                with self.subTest(domain=name, point=point):
                    found = locate(ROOT, name, point)
                    self.assertTrue(found['sections'])
                    for section in found['sections']:
                        lines = (ROOT / section['path']).read_text().splitlines()
                        self.assertIn(point, lines[section['start_line'] - 1])
                        self.assertGreater(section['end_line'], section['start_line'])
                        self.assertTrue(all(not l.startswith('## ') for l in lines[section['start_line']:section['end_line']]))

    def test_domain_aliases_do_not_change_material_location(self):
        self.assertEqual(locate(ROOT, 'serve', 'go.lang.interface'), locate(ROOT, 'go-backend', 'go.lang.interface'))

    def test_learner_title_is_real_heading_without_internal_identifiers(self):
        section = locate(ROOT, 'frontend', 'fe.ts.contract')['sections'][0]
        self.assertEqual(section['display_title'], '类型在边界之后才可信')
        self.assertIn(section['display_title'], section['heading'])

    def test_unknown_and_cross_domain_requests_are_rejected(self):
        for domain, point in [('frontend', 'conc.volatile'), ('../frontend', 'fe.js.value'), ('frontend', 'fe.js')]:
            with self.assertRaises(ValueError):
                locate(ROOT, domain, point)
