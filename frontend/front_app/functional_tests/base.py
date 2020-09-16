import os
import socket
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.conf import settings

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8001'

class FunctionalTest(StaticLiveServerTestCase):
    live_server_url = 'http://{}:8001'.format(
        socket.gethostbyname(socket.gethostname())
    )

    def setUp(self):
        settings.DEBUG = True
        self.browser = webdriver.Remote(
            command_executor="http://hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_home(self):
        self.browser.get(self.live_server_url)
