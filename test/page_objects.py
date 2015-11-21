# -*- coding: utf-8 -*-
import os

import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SUBMIT = '//input[@value="Войти"]'
    LOGIN_BUTTON = "//a[@id='PH_authLink']"
    EXIT = "//a[@id='PH_logoutLink']"

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.LOGIN))
        )

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.EXIT))
        )



class AskForm(Component):
    # TODO категории и пользовательское соглашение
    QUESTION = "//textarea[@id='ask-text']"
    DESCRIPTION = '//textarea[@placeholder="Введите текст пояснения"]'
    FOTO = '//span[text()="Фото"]'
    VIDEO = '//span[text()="Видео"]'
    CATEGORY = "//select[@id='ask-categories']"
    SUBCATEGORY = "//select[@id='ask-sub-category']"
    OPTION = "/option[text()='%s']"
    SWITCH_NOTIFICATION = "//input[@id='ask-receive-email']"
    SWITCH_COMMENTS = "//input[@id='ask-allow-comments']"
    TERMS = "//a[@href='https://help.mail.ru/otvety-help/agreement']"
    # TODO У меня такого SUBMIT нет
    SUBMIT = "//a[@id='ask-q-only']"
    SUBMIT_QUESTION = "//div[@class='ask-submit']/button"

    def wait_for_upload(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, self.SWITCH_COMMENTS))
        )

    def set_question(self, question):
        self.driver.find_element_by_xpath(self.QUESTION).send_keys(question)

    def set_description(self, description):
        self.driver.find_element_by_xpath(self.DESCRIPTION).send_keys(description)

    def open_and_get_foto_form(self):
        self.driver.find_element_by_xpath(self.FOTO).click()
        return PhotoForm(self.driver)

    def open_and_get_video_form(self):
        self.driver.find_element_by_xpath(self.VIDEO).click()
        return VideoForm(self.driver)

    def off_notifications(self):
        self.driver.find_element_by_xpath(self.SWITCH_NOTIFICATION).click()

    def off_comments(self):
        self.driver.find_element_by_xpath(self.SWITCH_COMMENTS).click()

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_QUESTION).click()

    def set_category(self, category_name):
        self.driver.find_element_by_xpath(self.CATEGORY + (self.OPTION % category_name)).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.SUBCATEGORY))
        )

    def set_subcategory(self, subcategory_name):
        self.driver.find_element_by_xpath(self.SUBCATEGORY + (self.OPTION % subcategory_name)).click()


class Question(Component):
    QUESTION = "//h1[@class='q--qtext entry-title']/index"
    QUESTION_DESCRIPTION = "//div[@class='q--qcomment h4 entry-content']"
    USERNAME = "//a[@class='q--user h5 author']/b"

    def get_question(self):
        return self.driver.find_element_by_xpath(self.QUESTION).text

    def get_question_description(self):
        return self.driver.find_element_by_xpath(self.QUESTION_DESCRIPTION).text

    def get_username(self):
        return self.driver.find_element_by_xpath(self.USERNAME).text


class PhotoForm(Component):
    CHOOSE_LINK = '//span[text()="укажите ссылку в сети"]'
    LINK = '//input[@placeholder="Укажите ссылку на изображение"]'

    def choose_link(self):
        self.driver.find_element_by_xpath(self.CHOOSE_LINK).click()

    def set_link(self, link):
        self.driver.find_element_by_xpath(self.LINK).send_keys(link)


# TODO Открывается в новом окне. Наверняка будут проблемы
class VideoForm(Component):
    LINK = '//input[@data-type="video-input-link"]'
    SUBMIT = '//button[@data-type="video-button-link"]'

    def set_link(self, link):
        self.driver.find_element_by_xpath(self.LINK).send_keys(link)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class Page(object):
    BASE_URL = 'https://otvet.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)


class AskPage(Page):
    PATH = 'ask'

    @property
    def form(self):
        return AskForm(self.driver)


class QuestionPage(Page):
    PATH = "question/184484161"

    @property
    def form(self):
        return Question(self.driver)