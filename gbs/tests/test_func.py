import os
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from unittest import skipUnless


@skipUnless(os.environ.get('DJANGO_SELENIUM_TESTS', False),
            "Skipping Selenium tests")
class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = WebDriver(options=options)

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
