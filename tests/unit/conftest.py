import pytest
from base.selenium_driver import SeleniumDriver

# Class Helpers
class SeleniumMocks:
    def __init__(self, mocker):
        self.wait = mocker.patch.object(SeleniumDriver, "wait_for_element")
        self.get_element_list = mocker.patch.object(SeleniumDriver, "get_elementList")
        self.get_text = mocker.patch.object(SeleniumDriver, "get_text")
        self.get_element = mocker.patch.object(SeleniumDriver, "get_element")
        self.element_click = mocker.patch.object(SeleniumDriver, "element_click")

# Fixtures
@pytest.fixture
def mock_selenium(mocker):
    return SeleniumMocks(mocker)

@pytest.fixture
# For instantiate each Web
def web_mocker(mocker):
    def instantiate_browser(clss, driver="driver"):
        mocker.patch.object(clss, "__init__", lambda self, d: None)
        page = clss.__new__(clss)
        setattr(page, driver,mocker.MagicMock())

        return page

    return instantiate_browser