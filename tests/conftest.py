import pytest
from base.selenium_driver import SeleniumDriver
from webs.manga_plus import MangaPlus

# Class Helpers
class SeleniumMocks:
    def __init__(self, mocker):
        self.wait = mocker.patch.object(SeleniumDriver, "wait_for_element")
        self.get_element_list = mocker.patch.object(SeleniumDriver, "get_elementList")
        self.get_text = mocker.patch.object(SeleniumDriver, "get_text")
        self.get_element = mocker.patch.object(SeleniumDriver, "get_element")

# Fixtures
@pytest.fixture
def manga_plus(mocker):
    mocker.patch.object(MangaPlus, "__init__", lambda self, d: None)
    page = MangaPlus.__new__(MangaPlus)
    page.driver = mocker.MagicMock()
    return page

@pytest.fixture
def mock_selenium(mocker):
    return SeleniumMocks(mocker)