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

    def search(self, page, search_request):
        top_bar = page.get_top_bar_form
        top_bar.search(search_request)
        top_bar.submit()
        return page.get_search_results_form

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

        self.search(search_page, self.QUESTION_TITLE_OTHER)

        side_bar = search_page.get_side_bar_form
        side_bar.set_category(self.OTHER_CATEGORY)

        search_results = search_page.get_search_results_form
        self.assertTrue(search_results.check_question_exist(self.QUESTION_ID_OTHER))

    def test_author(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.search(search_page, self.QUESTION_TITLE_OTHER)
        results_form.get_question_form(self.QUESTION_ID_OTHER)
