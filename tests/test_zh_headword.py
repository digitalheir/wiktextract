from collections import defaultdict
from unittest import TestCase
from unittest.mock import Mock, patch

from wikitextprocessor import Wtp

from wiktextract.extractor.zh.headword_line import extract_headword_line
from wiktextract.thesaurus import close_thesaurus_db
from wiktextract.wxr_context import WiktextractContext


class TestHeadword(TestCase):
    def setUp(self):
        self.wxr = WiktextractContext(Wtp(lang_code="zh"), Mock())

    def tearDown(self):
        self.wxr.wtp.close_db_conn()
        close_thesaurus_db(
            self.wxr.thesaurus_db_path, self.wxr.thesaurus_db_conn
        )

    @patch(
        "wikitextprocessor.Wtp.node_to_wikitext",
        return_value='<strong class="Latn headword" lang="en">manga</strong> ([[可數|可數]] & [[不可數|不可數]]，複數 <b class="Latn form-of lang-en p-form-of" lang="en"><strong class="selflink">manga</strong></b> <small>或</small> <b class="Latn form-of lang-en p-form-of" lang="en">[[mangas#英語|mangas]]</b>)',
    )
    def test_english_headword(self, mock_node_to_wikitext) -> None:
        # https://zh.wiktionary.org/wiki/manga#字源1
        # wikitext: {{en-noun|~|manga|s}}
        # expanded text: manga (可數 & 不可數，複數 manga 或 mangas)
        node = Mock()
        node.largs = [["en-noun"]]
        page_data = [defaultdict(list)]
        self.wxr.wtp.title = "manga"
        extract_headword_line(self.wxr, page_data, node, "en")
        self.assertEqual(
            page_data,
            [
                {
                    "forms": [
                        {"form": "manga", "tags": ["plural"]},
                        {"form": "mangas", "tags": ["plural"]},
                    ],
                    "tags": ["countable", "uncountable"],
                }
            ],
        )

    @patch(
        "wikitextprocessor.Wtp.node_to_wikitext",
        return_value='<strong class="Latn headword" lang="nl">manga</strong>&nbsp;<span class="gender"><abbr title="陽性名詞">m</abbr></span> (複數 <b class="Latn form-of lang-nl p-form-of" lang="nl">[[manga\'s#荷蘭語|manga\'s]]</b>，指小詞 <b class="Latn form-of lang-nl 指小詞-form-of" lang="nl">[[mangaatje#荷蘭語|mangaatje]]</b>&nbsp;<span class="gender"><abbr title="中性名詞">n</abbr></span>)',
    )
    def test_headword_gender(self, mock_node_to_wikitext) -> None:
        # https://zh.wiktionary.org/wiki/manga#字源1_2
        # wikitext: {{nl-noun|m|-'s|mangaatje}}
        # expanded text: manga m (複數 manga's，指小詞 mangaatje n)
        node = Mock()
        node.largs = [["nl-noun"]]
        page_data = [defaultdict(list)]
        self.wxr.wtp.title = "manga"
        extract_headword_line(self.wxr, page_data, node, "nl")
        self.assertEqual(
            page_data,
            [
                {
                    "forms": [
                        {"form": "manga's", "tags": ["plural"]},
                        {"form": "mangaatje", "tags": ["diminutive", "neuter"]},
                    ],
                    "tags": ["masculine"],
                }
            ],
        )

    @patch(
        "wikitextprocessor.Wtp.node_to_wikitext",
        return_value='<strong class="polytonic headword" lang="grc">-κρατίᾱς</strong> (<span lang="grc-Latn" class="headword-tr tr Latn" dir="ltr">-kratíās</span>)&nbsp;<span class="gender"><abbr title="陰性名詞">f</abbr></span>',
    )
    def test_headword_roman(self, mock_node_to_wikitext) -> None:
        # https://zh.wiktionary.org/wiki/-κρατίας
        # wikitext: {{head|grc|後綴變格形|g=f|head=-κρατίᾱς}}
        # expanded text: -κρατίᾱς (-kratíās) f
        node = Mock()
        node.largs = [["head"]]
        page_data = [defaultdict(list)]
        self.wxr.wtp.title = "-κρατίας"
        extract_headword_line(self.wxr, page_data, node, "grc")
        self.assertEqual(
            page_data,
            [
                {
                    "forms": [
                        {"form": "-kratíās", "tags": ["romanization"]},
                    ],
                    "tags": ["feminine"],
                }
            ],
        )
