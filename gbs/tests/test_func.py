import os
import sys
from unittest import skipUnless

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

RUN_LOCAL = os.environ.get("RUN_TESTS_LOCAL") == "True"


if RUN_LOCAL:
    # could add Chrome, PhantomJS etc... here
    browsers = ["Firefox"]
else:
    if os.getenv("SAUCE_ACCESS_KEY"):
        from sauceclient import SauceClient

        USERNAME = os.environ.get("SAUCE_USERNAME")
        ACCESS_KEY = os.environ.get("SAUCE_ACCESS_KEY")
        sauce = SauceClient(USERNAME, ACCESS_KEY)

    browsers = [
        {"platform": "macOS 10.14", "browserName": "chrome", "version": "79.0"},
        {
            "platform": "Windows 10",
            "browserName": "MicrosoftEdge",
            "version": "17.17134",
        },
        {"platform": "macOS 10.14", "browserName": "firefox", "version": "72.0"},
    ]


def on_platforms(platforms, local):
    if local:

        def decorator(base_class):
            module = sys.modules[base_class.__module__].__dict__
            for i, platform in enumerate(platforms):
                d = dict(base_class.__dict__)
                d["browser"] = platform
                name = "%s_%s" % (base_class.__name__, i + 1)
                module[name] = type(name, (base_class,), d)
            pass

        return decorator

    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d["desired_capabilities"] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = type(name, (base_class,), d)

    return decorator


@on_platforms(browsers, RUN_LOCAL)
@skipUnless(os.environ.get("DJANGO_SELENIUM_TESTS", False), "Skipping Selenium tests")
class HelloSauceTest(StaticLiveServerTestCase):
    """
    Runs a test using travis-ci and saucelabs
    """

    def setUp(self):
        if RUN_LOCAL:
            self.setUpLocal()
        else:
            self.setUpSauce()

    def tearDown(self):
        if RUN_LOCAL:
            self.tearDownLocal()
        else:
            self.tearDownSauce()

    def setUpSauce(self):
        if os.getenv("TRAVIS"):
            self.desired_capabilities["name"] = self.id()
            self.desired_capabilities["tunnel-identifier"] = os.environ[
                "TRAVIS_JOB_NUMBER"
            ]
            self.desired_capabilities["build"] = os.environ["TRAVIS_BUILD_NUMBER"]
            self.desired_capabilities["tags"] = [
                os.environ["TRAVIS_PYTHON_VERSION"],
                "CI",
            ]

        print(self.desired_capabilities)

        if os.getenv("SAUCE_ACCESS_KEY"):
            sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
            self.driver = webdriver.Remote(
                desired_capabilities=self.desired_capabilities,
                command_executor=sauce_url % (USERNAME, ACCESS_KEY),
            )
            self.driver.implicitly_wait(5)

    def setUpLocal(self):
        self.driver = getattr(webdriver, self.browser)()
        self.driver.implicitly_wait(3)

    def tearDownLocal(self):
        self.driver.quit()

    def tearDownSauce(self):
        print(
            "\nLink to your job: \n "
            "https://saucelabs.com/jobs/%s \n" % self.driver.session_id
        )
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

    def test_sauce(self):
        self.driver.get(self.live_server_url + "/admin")
        wait = WebDriverWait(self.driver, 15)
        wait.until(lambda driver: self.driver.title.lower().startswith("l"))
        self.assertIn("Log in", self.driver.title)

    def test_homepage(self):
        self.driver.get(self.live_server_url)
        self.driver.get_screenshot_as_file("/tmp/website.png")
        wait = WebDriverWait(self.driver, 15)
        wait.until(lambda driver: self.driver.title.lower().startswith("g"))
        self.assertIn("Grogan Burner Services", self.driver.title)
