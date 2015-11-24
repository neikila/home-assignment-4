# -*- coding: utf-8 -*-

from test.search.page_objects import *
from test_data import TestSearch


class PositiveTests(TestSearch):
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

    def test_author(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        question_form = results_form.get_question_form(self.QUESTION_ID_OTHER)
        self.assertEquals(question_form.get_author(), self.USERNAME)

    def test_category(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        question_form = results_form.get_question_form(self.QUESTION_ID_OTHER)
        self.assertEquals(question_form.get_category(), self.OTHER_CATEGORY)

    def test_subcategory(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_TITLE_PROGRAMMING)

        question_form = results_form.get_question_form(self.QUESTION_ID_PROGRAMMING)
        self.assertEquals(question_form.get_category(), self.PYTHON_SUBCATEGORY)

    def test_question_text(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        question_form = results_form.get_question_form(self.QUESTION_ID_OTHER)
        self.assertEquals(question_form.get_title(), self.QUESTION_TITLE_OTHER)

    def test_category_search(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        side_bar = search_page.get_side_bar_form
        side_bar.set_category(self.OTHER_CATEGORY)

        search_results = search_page.get_search_results_form
        self.assertTrue(search_results.check_question_exist(self.QUESTION_ID_OTHER))

    def test_subcategory_search(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_PROGRAMMING)

        side_bar = search_page.get_side_bar_form
        side_bar.set_category(self.PROG_CATEGORY)
        side_bar.set_subcategory(self.PYTHON_SUBCATEGORY)

        search_results = search_page.get_search_results_form
        self.assertTrue(search_results.check_question_exist(self.QUESTION_ID_PROGRAMMING))


class NegativeTests(TestSearch):
    JAVA_SUBCATEGORY = u"Java"

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

    def test_wrong_category(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_PROGRAMMING)

        side_bar = search_page.get_side_bar_form
        side_bar.set_category(self.OTHER_CATEGORY)

        search_results = search_page.get_search_results_form
        self.assertFalse(search_results.check_question_exist(self.QUESTION_ID_PROGRAMMING))

    def test_wrong_subcategory(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_PROGRAMMING)

        side_bar = search_page.get_side_bar_form
        side_bar.set_category(self.PROG_CATEGORY)
        side_bar.set_subcategory(self.JAVA_SUBCATEGORY)

        search_results = search_page.get_search_results_form
        self.assertFalse(search_results.check_question_exist(self.QUESTION_ID_PROGRAMMING))