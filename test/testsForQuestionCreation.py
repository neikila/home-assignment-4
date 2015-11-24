# -*- coding: utf-8 -*-

from page_objects import *
import time

class PositiveTests(unittest.TestCase):
    USEREMAIL = 'artur.pirozhkov.like.a.boss@mail.ru'
    PASSWORD = 'testirovanie'
    QUESTION = u'I hope now it is long enough? You need more symbols, really? WTF How much do you need? ' \
               u'Да вы блин серьезно?!'
    DESCRIPTION = u'Very strange. I need MORE description!\n' \
                  u'Are you serious?'
    FOTO = 'http://uu.appsforall.ru/542ee0c9be4f73.01671974.jpg'
    VIDEO = 'https://cloclo24.datacloudmail.ru/weblink/view/Gpdt/BnymkS35Q?etag=65D1C4B510DF51FF36E413F340F21E8FC45F4D58'
    CATEGORY = u'Программирование'
    SUBCATEGORY = 'Python'
    USERNAME = u'Артур Пирожков'

    def auth(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

    def ask_question(self, comments_off=True, notifications_off=True):
        ask_page = AskPage(self.driver)
        ask_page.open()
        ask_form = ask_page.form
        ask_form.set_question(self.QUESTION)
        ask_form.set_description(self.DESCRIPTION)
        if comments_off:
            ask_form.off_comments()
        if notifications_off:
            ask_form.off_notifications()
        ask_form.set_category(self.CATEGORY)
        ask_form.set_subcategory(self.SUBCATEGORY)
        # ask_form.submit()
        # А теперь вводим капчу

    def get_created_question_page(self):
        profile_page = ProfilePage(self.driver)
        profile_page.open()
        profile_list_form = profile_page.form
        url = profile_list_form.get_last_question_url()
        return QuestionPage(self.driver, url)

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
        self.auth()

    # Проверка правильного создержимого вопроса
    def test_question(self):
        self.ask_question()

        question_page = self.get_created_question_page()
        question_page.open()
        question_form = question_page.form
        self.assertEquals(question_form.get_question(), self.QUESTION)

    # Проверка правильного описания
    def test_description(self):
        self.ask_question()

        question_page = self.get_created_question_page()
        question_page.open()
        question_form = question_page.form
        self.assertEquals(question_form.get_question_description(), self.DESCRIPTION)

    # Проверка правильного авторства
    def test_author(self):
        self.ask_question()

        question_page = self.get_created_question_page()
        question_page.open()
        question_form = question_page.form
        self.assertEquals(question_form.get_username(), self.USERNAME)

    # Проверка правильная ли категория
    def test_category(self):
        self.ask_question()

        question_page = self.get_created_question_page()
        question_page.open()
        question_form = question_page.form
        self.assertEquals(question_form.get_category(), self.CATEGORY)

    # Проверка правильная ли подкатегория
    def test_subcategory(self):
        self.ask_question()

        question_page = self.get_created_question_page()
        question_page.open()
        question_form = question_page.form
        self.assertEquals(question_form.get_subcategory(), self.SUBCATEGORY)