from basic_test import *
import time

class ExampleTest(unittest.TestCase):
    USEREMAIL = 'another95@mail.ru'
    PASSWORD = 'rfrltkf'

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
        time.sleep(1)
        auth_form = auth_page.form
        auth_form.open_form()
        time.sleep(1)
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        time.sleep(1)
        auth_form.submit()
        time.sleep(1000)
