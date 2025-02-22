# Tests for parsing a page
#
# Copyright (c) 2021 Tatu Ylonen.  See file LICENSE and https://ylonen.org

import unittest

from wikitextprocessor import Wtp

from wiktextract.config import WiktionaryConfig
from wiktextract.extractor.fr.page import parse_page
from wiktextract.thesaurus import close_thesaurus_db
from wiktextract.wxr_context import WiktextractContext


class FrPageTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        conf1 = WiktionaryConfig(
            dump_file_lang_code="fr",
            capture_language_codes=None,
        )
        self.wxr = WiktextractContext(Wtp(lang_code="fr"), conf1)

    def tearDown(self) -> None:
        self.wxr.wtp.close_db_conn()
        close_thesaurus_db(
            self.wxr.thesaurus_db_path, self.wxr.thesaurus_db_conn
        )

    def test_fr_parse_page(self):
        self.wxr.wtp.add_page("Modèle:langue", 10, "Français")
        self.wxr.wtp.add_page("Modèle:S", 10, "Nom commun")
        lst = parse_page(
            self.wxr,
            "exemple",
            """
== {{langue|fr}} ==
=== {{S|nom|fr}} ===
'''exemple'''
""",
        )
        self.assertEqual(
            lst,
            [
                {
                    "lang": "Français",
                    "lang_code": "fr",
                    "pos": "noun",
                    "pos_title": "Nom commun",
                    "word": "exemple",
                }
            ],
        )
