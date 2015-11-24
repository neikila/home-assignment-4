# -*- coding: utf-8 -*-

from test.search.page_objects import *
from test_data import TestSearch


class PositiveTests(TestSearch):
    YEAR = u"год"

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

    def test_accurate_search(self):
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

    def test_time_gate(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        side_bar = search_page.get_side_bar_form
        side_bar.set_period(self.YEAR)

        search_results = search_page.get_search_results_form
        self.assertTrue(search_results.check_question_exist(self.QUESTION_ID_OTHER))

    def test_sort_by_time(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.search(search_page, self.QUESTION_TITLE_OTHER)
        search_results = search_page.get_search_results_form
        search_results.set_sort_by_time()

        elements = search_results.get_questions()
        old_element = search_results.get_question_date(elements[0])
        old_number = int(re.search(r'\d+', old_element).group()) #Судя по тестам в терминале не работает
        #old_type
        for elem in elements:
            new_time = search_results.get_question_date(elem)
            #TODO сравннение времени
            last_time = new_time

    def test_check_number_of_answers(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)
        search_results = search_page.get_search_results_form
        question = search_results.get_question_form(self.QUESTION_ID_OTHER)
        answers = question.get_answers()
        answers = int(answers.split()[0])
        question_form = question.go_to_question_page_and_get_form()
        self.assertEqual(answers, question_form.get_number_of_answers())


class NegativeTests(TestSearch):
    JAVA_SUBCATEGORY = u"Java"
    MONTH = u"месяц"

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

    def test_wrong_time_gate(self):
        search_page = SearchPage(self.driver)
        search_page.open()

        self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        side_bar = search_page.get_side_bar_form
        side_bar.set_period(self.MONTH)

        search_results = search_page.get_search_results_form
        self.assertFalse(search_results.check_question_exist(self.QUESTION_ID_PROGRAMMING))
