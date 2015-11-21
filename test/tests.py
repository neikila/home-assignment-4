from page_objects import *
import time

class PositiveTests(unittest.TestCase):
    USEREMAIL = 'artur.pirozhkov.like.a.boss@mail.ru'
    PASSWORD = 'testirovanie'
    QUESTION = 'Test question'
    DESCRIPTION = 'Very strange'
    FOTO = 'http://uu.appsforall.ru/542ee0c9be4f73.01671974.jpg'
    VIDEO = 'https://cloclo24.datacloudmail.ru/weblink/view/Gpdt/BnymkS35Q?etag=65D1C4B510DF51FF36E413F340F21E8FC45F4D58'

    def auth(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

    def tearDown(self):
        pass
        # self.driver.quit()

    def setUp(self):
        browser = 'CHROME'

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser)
                .copy()
        )
        self.auth()

    def test(self):
        time.sleep(1)

        ask_page = AskPage(self.driver)
        ask_page.open()

        ask_form = ask_page.form
        ask_form.wait_for_upload()
        ask_form.set_question(self.QUESTION)
        ask_form.set_description(self.DESCRIPTION)
        ask_form.off_comments()
        ask_form.off_notifications()

        time.sleep(1000)
