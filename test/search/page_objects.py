# -*- coding: utf-8 -*-
import re
import urlparse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class SideBarForm(Component):
    PERIOD = "id('ColumnLeft')/div/a[text()='%s']"
    CATEGORY = "//div[@class='current-category']//a[text()='%s']"
    SUBCATEGORY = "//div[@class='current-category']//a[text()='%s']"
    FILTER_PATTERN = re.compile("https://otvet.mail.ru/search/[a-z]-[0-9]+/.+")

    def __init__(self, driver):
        super(SideBarForm, self).__init__(driver)
        self.top_bar = TopToolBarForm(driver)

    def get_url(self, xpath):
        WebDriverWait(self.driver, 10).until(
            lambda s: self.FILTER_PATTERN.match(self.driver.find_element_by_xpath(xpath).get_attribute("href")) is not None
        )
        return self.driver.find_element_by_xpath(xpath).get_attribute("href")

    def set_category(self, category_name):
        self.driver.get(self.get_url(self.CATEGORY % category_name))

    def set_subcategory(self, subcategory_name):
        self.driver.get(self.get_url(self.SUBCATEGORY % subcategory_name))

    def set_period(self, period):
        self.driver.get(self.get_url(self.PERIOD % period))


class QuestionForm(Component):
    ANSWERS = "//div[@class='container-for-answers']/div[contains(@class, ' answer')]"

    def get_number_of_answers(self):
        return self.driver.find_elements_by_xpath(self.ANSWERS).__len__()


class ProfileListForm(Component):
    LAST_QUESTION = "//div[@class='page-profile-list']/div[1]/a"
    WAIT_TIME = 10

    def get_last_question_url(self):
        WebDriverWait(self.driver, self.WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, self.LAST_QUESTION))
        )
        return self.driver.find_element_by_xpath(self.LAST_QUESTION).get_attribute("href")


class TopToolBarForm(Component):
    SEARCH_TEXT = "//input[contains(@class, 'pm-toolbar__search__input')]"
    SUBMIT = "//button[contains(@class, 'js-submit-button')]"
    SEARCH_RESULTS_SUCCESS = "//div[@class='page-search']/div[@class='search-info']//b"
    SEARCH_RESULTS_FAIL = "//div[@class='search-page']/p[contains(@class, 'smallBull')]"
    WAIT_TIME = 10
    PATTERN = re.compile("https://otvet.mail.ru/question/[0-9]+")
    FIRST_QUESTION = "//div[@class='search-component']/div/div/a[2]"

    def search(self, text):
        WebDriverWait(self.driver, self.WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, self.SEARCH_TEXT))
        )
        self.driver.find_element_by_xpath(self.SEARCH_TEXT).send_keys(text)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
        self.wait_for_result_to_load()

    def wait_for_result_to_load(self):
        WebDriverWait(self.driver, self.WAIT_TIME).until(
            lambda s: (EC.element_to_be_clickable((By.XPATH, self.SEARCH_RESULTS_FAIL)) and
                       len(self.driver.find_element_by_xpath(self.SEARCH_TEXT).text) != 0) or
                      (EC.presence_of_element_located((By.XPATH, self.SEARCH_RESULTS_SUCCESS)) and
                       self.PATTERN.match(self.driver.find_element_by_xpath(self.FIRST_QUESTION).get_attribute("href")) is not None)
        )


class QuestionInSearchForm(Component):

    def __init__(self, driver, xpath):
        super(QuestionInSearchForm, self).__init__(driver)
        self.xpath = xpath
        self.TITLE = xpath + "/a[contains(@class, 'item__text')]"
        self.AUTHOR = xpath + "/div[@class='item__stats']/a[contains(@href, 'profile')]"
        self.CATEGORY = xpath + "/div[@class='item__stats']/a[2]"
        self.LINK = xpath + "//a[contains(@class, 'item__answer')]"
        self.ANSWERS = self.LINK + "/span"

    def get_title(self):
        return self.driver.find_element_by_xpath(self.TITLE).text

    def get_author(self):
        return self.driver.find_element_by_xpath(self.AUTHOR).text

    def get_category(self):
        return self.driver.find_element_by_xpath(self.CATEGORY).text[1:-1]

    def get_answers(self):
        return self.driver.find_element_by_xpath(self.ANSWERS).text

    def go_to_question_page_and_get_form(self):
        link = self.driver.find_element_by_xpath(self.LINK).get_attribute("href")
        self.driver.get(link)
        return QuestionForm(self.driver)


class SearchResultsForm(Component):
    QUESTIONS_LIST = "//div[contains(@class, 'list bordered')]"
    QUESTION_SELECTOR = QUESTIONS_LIST + "/div[./a[@href='/question/%s']]"
    MORE = "//button[contains(@class, 'btn-more')]"
    WAIT_TIME = 10
    SORT_BY_TIME = "//a[text()='По дате']"
    QUESTIONS = QUESTIONS_LIST + "/div[contains(@class, 'item_similiar')]"
    DATE = "//div[@class='item__stats']/div[2]"
    FILTER_PATTERN = re.compile("https://otvet.mail.ru/search/([a-z]-[0-9]+/)?s-date/.+")

    def get_question_form(self, q_id):
        question_form = QuestionInSearchForm(self.driver, self.QUESTION_SELECTOR % q_id)
        return question_form

    def more_questions(self):
        self.driver.find_element_by_xpath(self.MORE).click()

    def check_question_exist(self, q_id):
        try:
            self.driver.find_element_by_xpath(self.QUESTION_SELECTOR % q_id)
            return True
        except:
            return False

    def set_sort_by_time(self):
        WebDriverWait(self.driver, 10).until(
            lambda s: self.FILTER_PATTERN.match(self.driver.find_element_by_xpath(self.SORT_BY_TIME).get_attribute("href")) is not None
        )
        self.driver.find_element_by_xpath(self.SORT_BY_TIME).click()
        TopToolBarForm(self.driver).wait_for_result_to_load()

    def get_questions(self):
        return self.driver.find_elements_by_xpath(self.QUESTIONS)

    def get_question_date(self, element):
        return element.find_element_by_xpath(self.DATE).text

    def get_dates(self):
        return self.driver.find_elements_by_xpath("//div[contains(@class, 'item__stats')]/div[2]")


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
