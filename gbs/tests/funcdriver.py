import os
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


def get_driver():
        if os.getenv("SAUCE_ACCESS_KEY"):
            # Set capabilities on sauce
            desired_cap = {
                'platform': "Mac OS X 10.12",
                'browserName': "safari",
                'version': "11",
            }

            # Add Travis metadata to the build
            job = os.environ.get('TRAVIS_JOB_NUMBER')
            if job is not None:
                desired_cap['tunnel-identifier'] = job
            build = os.environ.get("TRAVIS_BUILD_NUMBER")
            if build is not None:
                desired_cap['build'] = build
            tag = os.environ.get("TRAVIS_PYTHON_VERSION")
            if tag is not None:
                desired_cap['tags'] = [tag, "CI"]


            user = os.environ.get('SAUCE_USERNAME')
            key = os.environ.get('SAUCE_ACCESS_KEY')

            url = f'http://{user}:{key}@ondemand.saucelabs.com:80/wd/hub'

            return webdriver.Remote(command_executor=url, desired_capabilities=desired_cap)
        else:
            options = Options()
            options.add_argument('-headless')
            return webdriver.Firefox(options=options)
