import os
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


class FuncDriver():
    def __init__(self):
        if os.getenv("SAUCE_ACCESS_KEY"):
            desired_cap = {
                'platform': "Mac OS X 10.9",
                'browserName': "chrome",
                'version': "31",
            }

            user = os.environ.get('SAUCE_USERNAME')
            key = os.environ.get('SAUCE_ACCESS_KEY')

            url = f'http://{user}:{key}@ondemand.saucelabs.com:80/wd/hub'

            self = webdriver.Remote(command_executor=url, desired_capabilities=desired_cap)
        else:
            options = Options()
            options.add_argument('-headless')
            self = webdriver.Firefox(options=options)
