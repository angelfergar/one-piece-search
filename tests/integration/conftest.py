import pytest
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

samples_dir = os.path.join(os.path.dirname(__file__), "samples")

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1920, 1080)
    yield driver
    return driver

@pytest.fixture
def navigate(driver):
    def _navigate(filename):
        path = os.path.join(samples_dir, filename)
        url = "file:///" + path.replace("\\", "/")
        driver.get(url)
        return driver
    return _navigate
