# -*- coding: utf-8 -*-
import os

import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class SideBarForm(Component):
    PERIOD = "id('ColumnLeft')/div/a[text()='%s']"
    CATEGORY = "//div[@class='current-category']//a[text()='%s']"
    SUBCATEGORY = "//div[@class='current-category']//a[text()='%s']"

    def set_category(self, category_name):
        element = self.driver.find_element_by_xpath(self.CATEGORY % category_name)
        ActionChains(self.driver).move_to_element(element).click(element)

    def set_subcategory(self, subcategory_name):
        self.driver.find_element_by_xpath(self.SUBCATEGORY % subcategory_name).click()

    def set_period(self, perioud):
        self.driver.find_element_by_xpath(self.PERIOD % perioud).click()


class QuestionForm(Component):
    QUESTION = "//*[contains(@class,'q--qtext')]/index"
    QUESTION_DESCRIPTION = "//*[contains(@class,'q--qcomment')]"
    USERNAME = "//*[contains(@class,'q--user')]/b"
    QUESTION_FIELD = "//*[contains(@class,'page-question')]"
    DELETE = "//button[@data-type='delete-question']"
    CATEGORY = "//a[contains(@class,'list__title')]/span[@itemprop='title']"
    SUBCATEGORY = "//a[contains(@class,'selected')]/span[@itemprop='title']"

    def wait(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.QUESTION_FIELD))
        )

    def get_question(self):
        return self.driver.find_element_by_xpath(self.QUESTION).text

    def get_question_description(self):
        return self.driver.find_element_by_xpath(self.QUESTION_DESCRIPTION).text

    def get_username(self):
        return self.driver.find_element_by_xpath(self.USERNAME).text

    def delete(self):
        self.driver.find_element_by_xpath(self.DELETE).click()

    def get_category(self):
        return self.driver.find_element_by_xpath(self.CATEGORY).text

    def get_subcategory(self):
        return self.driver.find_element_by_xpath(self.SUBCATEGORY).text


class ProfileListForm(Component):
    LAST_QUESTION = "//div[@class='page-profile-list']/div[1]/a"

    def get_last_question_url(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.LAST_QUESTION))
        )
        return self.driver.find_element_by_xpath(self.LAST_QUESTION).get_attribute("href")


class TopToolBarForm(Component):
    SEARCH_TEXT = "//input[contains(@class, 'pm-toolbar__search__input')]"
    SUBMIT = "//button[contains(@class, 'js-submit-button')]"
    SEARCH_RESULTS_SUCCESS = "//div[@class='page-search']/div[@class='search-info']//b"
    SEARCH_RESULTS_FAIL = "//div[@class='search-page']"

    def search(self, text):
        self.driver.find_element_by_xpath(self.SEARCH_TEXT).send_keys(text)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.SEARCH_RESULTS_SUCCESS + '|' + self.SEARCH_RESULTS_FAIL))
        )


class QuestionInSearchForm(Component):

    def __init__(self, driver, xpath):
        super(QuestionInSearchForm, self).__init__(driver)
        self.TITLE = xpath + "/a[contains(@class, 'item__text')]"
        self.AUTHOR = xpath + "/div[@class='item__stats']/a[contains(@href, 'profile')]"
        self.CATEGORY = xpath + "//span[contains(@class, 'item__stat item__stat')]"
        self.LINK = xpath + "//a[contains(@class, 'item__answer')]"

    def get_title(self):
        return self.driver.find_element_by_xpath(self.TITLE).text

    def get_author(self):
        return self.driver.find_element_by_xpath(self.AUTHOR).text

    def get_category(self):
        return self.driver.find_element_by_xpath(self.CATEGORY).text

    # Да одно и то же, но смысл разный, и понятно, что достаем из формы
    def get_subcategory(self):
        return self.driver.find_element_by_xpath(self.CATEGORY).text


class SearchResultsForm(Component):
    QUESTIONS_LIST = "//div[contains(@class, 'list bordered')]"
    QUESTION_SELECTOR = QUESTIONS_LIST + "/div[./a[@href='/question/%s']]"
    MORE = "//button[contains(@class, 'btn-more')]"

    def get_question_form(self, id):
        return QuestionInSearchForm(self.driver, self.QUESTION_SELECTOR % id)

    def more_questions(self):
        self.driver.find_element_by_xpath(self.MORE).click()

    def check_question_exist(self, id):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.QUESTION_SELECTOR % id))
        )


class Page(object):
    BASE_URL = 'https://otvet.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class QuestionPage(Page):
    PATH = ''

    def __init__(self, driver, url):
        self.BASE_URL = url
        super(QuestionPage, self).__init__(driver)

    @property
    def form(self):
        question_form = QuestionForm(self.driver)
        question_form.wait()
        return question_form


class SearchPage(Page):
    PATH = '/search'

    @property
    def get_top_bar_form(self):
        return TopToolBarForm(self.driver)

    @property
    def get_side_bar_form(self):
        return SideBarForm(self.driver)

    @property
    def get_search_results_form(self):
        return SearchResultsForm(self.driver)
