import os
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from unittest import skipUnless


@skipUnless(os.environ.get('DJANGO_SELENIUM_TESTS', False),
            "Skipping Selenium tests")
class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(FunctionalTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalTest, cls).tearDownClass()

    def test_index(self):
        self.selenium.get(self.live_server_url)
        self.selenium.get_screenshot_as_file('/tmp/website.png')
        wait = WebDriverWait(self.selenium, 10)
        print("TITLE:", self.selenium.title)
        wait.until(lambda selenium: self.selenium.title.lower().startswith('n'))
        self.assertIn("Grogan Burner Services", self.selenium.title)
