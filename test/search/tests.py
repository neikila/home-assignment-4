# -*- coding: utf-8 -*-

from test.search.page_objects import SearchPage
from test_data import TestSearch


class PositiveTests(TestSearch):
    YEAR = u"год"

    time_dictionary = {
        u'ми': 0,
        u'ча': 1,
        u'дн': 2,
        u'де': 2,
        u'не': 3,
        u'ме': 4,
        u'ле': 5,
        u'го': 6
    }

    def convert(self, time_word):
        return self.time_dictionary[time_word[0:2]]

    def is_first_less_than_second(self, first, second):
        if first[1] < second[1]:
            return True
        elif first[1] == second[1] and first[0] <= second[0]:
            return True
        else:
            return False

    def parse_str_to_tuple(self, data_str):
        array = data_str.split(' ')
        try:
            first = int(array[1])
            return first, self.convert(array[2])
        except ValueError:
            return 1, self.convert(array[1])

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

    def test_accurate_search_by_text(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_TITLE_OTHER)

        self.assertTrue(results_form.check_question_exist(self.QUESTION_ID_OTHER))

    def test_accurate_search_by_description(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.QUESTION_DESCRIPTION_PROGRAMMING)

        self.assertTrue(results_form.check_question_exist(self.QUESTION_ID_PROGRAMMING))

    def test_accurate_search_by_answer(self):
        search_page = SearchPage(self.driver)
        search_page.open()
        results_form = self.accurate_search(search_page, self.BEST_ANSWER_OTHER)

        self.assertTrue(results_form.check_question_exist(self.QUESTION_ID_OTHER))

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

        self.search(search_page, self.QUESTION_TITLE_OTHER_REDUCED)
        search_results = search_page.get_search_results_form
        search_results.set_sort_by_time()

        elements = search_results.get_dates()
        first_time = self.parse_str_to_tuple(elements[0].text)
        second_time = self.parse_str_to_tuple(elements[1].text)
        result = self.is_first_less_than_second(first_time, second_time)
        self.assertTrue(result)

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
