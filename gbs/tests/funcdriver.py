import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.safari.options import Options as SafariOptions


def get_driver():
    if os.getenv("SAUCE_ACCESS_KEY"):
        # Set capabilities on sauce
        desired_cap = {
            "platformName": "macOS 10.14",
            "browserName": "safari",
            "browserVersion": "12.0",
        }

        sauce_options = {}

        # Add Travis metadata to the build
        job = os.environ.get("TRAVIS_JOB_NUMBER")
        if job is not None:
            sauce_options["tunnel-identifier"] = job
        build = os.environ.get("TRAVIS_BUILD_NUMBER")
        if build is not None:
            sauce_options["build"] = build
        tag = os.environ.get("TRAVIS_PYTHON_VERSION")
        if tag is not None:
            sauce_options["tags"] = [tag, "CI"]

        user = os.environ.get("SAUCE_USERNAME")
        key = os.environ.get("SAUCE_ACCESS_KEY")

        url = f"http://{user}:{key}@ondemand.saucelabs.com:80/wd/hub"
        print(desired_cap)

        options = SafariOptions()
        for name, value in desired_cap.items():
            options.set_capability(name, value)
        options.set_capability("sauce:options", sauce_options)
        return webdriver.Remote(command_executor=url, options=options)
    else:
        options = Options()
        options.add_argument("-headless")
        return webdriver.Firefox(options=options)
