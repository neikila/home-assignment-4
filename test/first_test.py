from basic_test import *
import time

class ExampleTest(unittest.TestCase):
    USEREMAIL = 'another95@mail.ru'
    PASSWORD = 'rfrltkf'
    QUESTION = 'Strange question'
    DESCRIPTION = 'Very strange'

    def setUp(self):
        browser = 'CHROME'

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser)
                .copy()
        )

    def tearDown(self):
        pass
        # self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        time.sleep(1)

        ask_page = AskPage(self.driver)
        ask_page.open()

        ask_form = ask_page.form
        ask_form.set_question(self.QUESTION)
        ask_form.set_description(self.DESCRIPTION)
        ask_form.off_comments()
        ask_form.off_notifications()

        time.sleep(1000)
