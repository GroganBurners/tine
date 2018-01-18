import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from unittest import skipUnless
from gbs.tests.funcdriver import FuncDriver


@skipUnless(os.environ.get('DJANGO_SELENIUM_TESTS', False),
            "Skipping Selenium tests")
class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        cls.selenium = FuncDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalTest, cls).tearDownClass()

    def test_index(self):
        print(self.live_server_url)
        self.selenium.get(self.live_server_url)
        self.selenium.get_screenshot_as_file('/tmp/website.png')
        wait = WebDriverWait(self.selenium, 10)
        print("TITLE:", self.selenium.title)
        wait.until(
            lambda selenium: self.selenium.title.lower().startswith('g'))
        self.assertIn("Grogan Burner Services", self.selenium.title)
