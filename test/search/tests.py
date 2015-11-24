# -*- coding: utf-8 -*-

from test.search.page_objects import *


class PositiveTests(unittest.TestCase):
    QUESTION_ID_PROGRAMMING = u"184484161"
    PROG_CATEGORY = u'Программирование'
    PYTHON_SUBCATEGORY = u'Python'
    USERNAME = u'Артур Пирожков'

    QUESTION_ID_OTHER = u"182362166"
    QUESTION_TITLE_OTHER = u"\"Тестирование длины форм -\""
    OTHER_CATEGORY = u'Другое'

    def tearDown(self):
        # pass
        self.driver.quit()

    def setUp(self):
        browser = 'CHROME'

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser)
                .copy()
        )

    def test_category_search(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        top_bar = search_page.get_top_bar_form()
        top_bar.search(self.QUESTION_TITLE_OTHER)
        top_bar.submit()

        side_bar = search_page.get_side_bar_form()
        side_bar.set_category(self.OTHER_CATEGORY)


    def test_author(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        top_bar = search_page.get_top_bar_form
        top_bar.search(self.QUESTION_TITLE_OTHER)
        top_bar.submit()