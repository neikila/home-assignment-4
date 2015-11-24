# -*- coding: utf-8 -*-

from test.search.page_objects import *


class TestSearch(unittest.TestCase):
    QUESTION_ID_PROGRAMMING = u"184484161"
    QUESTION_TITLE_PROGRAMMING = u"I hope now it is long enough? You need more symbols, really? " \
                                 u"WTF How much do you need? Да вы блин серьезно?!"
    PROG_CATEGORY = u'Программирование'
    PYTHON_SUBCATEGORY = u'Python'
    USERNAME = u'Артур Пирожков'

    QUESTION_ID_OTHER = u"182362166"
    QUESTION_TITLE_OTHER = u"Тестирование длины форм -"
    OTHER_CATEGORY = u'Другое'

    def search(self, page, search_request):
        top_bar = page.get_top_bar_form
        top_bar.search(search_request)
        top_bar.submit()
        return page.get_search_results_form

    def accurate_search(self, page, search_request):
        return self.search(page, '\"' + search_request + '\"')
