from basic_test import *
import time

class ExampleTest(unittest.TestCase):
    def setUp(self):
        browser = 'CHROME'

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser)
                .copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = Page(self.driver)
        auth_page.open()
