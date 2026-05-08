import pytest
from webs.opscans import OpScans

@pytest.fixture
def opscans_setup(web_mocker, mocker, mock_selenium):
    class OpScansSetUp:
        def __init__(self):
            self.opscans = web_mocker(OpScans)
            self.min_images = 10

            self.selenium = mock_selenium

        def with_images(self, count):
            self.element_list = [mocker.MagicMock() for mock in range(count)]
            self.selenium.get_element_list.return_value = self.element_list
            return self

        def consent_visible(self, visible=True):
            if visible:
                self.selenium.wait()
                self.selenium.element_click()
            else:
                self.selenium.wait.side_effect = Exception()

    return OpScansSetUp()

class TestOpscans:
    def test_chapter_images(self, opscans_setup):
        opscans_setup.with_images(12).consent_visible()
        result = opscans_setup.opscans.get_chapter_images()

        assert result is True

    def test_no_consent(self, opscans_setup):
        opscans_setup.consent_visible(False)

        with pytest.raises(Exception):
            opscans_setup.opscans.get_chapter_images()