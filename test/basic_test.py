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

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def set_login(self, login):
        # исправить на "хороший" wait
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, self.LOGIN)))
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class AskForm(Component):
    #TODO категории и пользовательское соглашение
    QUESTION = "//textarea[@id='ask-text']"
    DESCRIPTION = '//textarea[@placeholder="Введите текст пояснения"]'
    FOTO = '//span[text()="Фото"]'
    VIDEO = '//span[text()="Видео"]'
    CATEGORY = "select[@id='ask-categories']"
    SUBCATEGORY = "select[@id='ask-sub-category']"
    SWITCH_NOTIFICATION = 'input[type="checkbox"]#ask-receive-email'
    SWITCH_COMMENTS = 'input[type="checkbox"]#ask-allow-comments'
    TERMS = "//a[@href='https://help.mail.ru/otvety-help/agreement']"
    SUBMIT = "//a[@id='ask-q-only']"

    def set_question(self, question):
        self.driver.find_element_by_xpath(self.QUESTION).send_keys(question)

    def set_description(self, description):
        self.driver.find_element_by_xpath(self.DESCRIPTION).send_keys(description)

    def open_and_get_foto_form(self):
        self.driver.find_element_by_xpath(self.FOTO).click()
        return FotoForm(self.driver)

    def open_and_get_video_form(self):
        self.driver.find_element_by_xpath(self.VIDEO).click()
        return VideoForm(self.driver)

    def off_notifications(self):
        self.driver.find_element_by_css_selector(self.SWITCH_NOTIFICATION).click()

    def off_comments(self):
        self.driver.find_element_by_css_selector(self.SWITCH_COMMENTS).click()

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class FotoForm(Component):
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
