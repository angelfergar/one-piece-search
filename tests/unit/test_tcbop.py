import pytest
from utils.utils import Util
from webs.tcb_op import TcbOp

@pytest.fixture
def tcbop_setup(web_mocker, mocker, mock_selenium):
    class TcbOpSetUp:
        def __init__(self):
            self.tcbop = web_mocker(TcbOp)
            self.chapters_checked = 3

            self.selenium = mock_selenium


        def with_chapters(self, titles):
            containers = [mocker.MagicMock() for _ in titles]
            self.selenium.get_element_list.return_value = containers
            self.selenium.get_element.side_effect = containers
            self.selenium.get_text.side_effect = titles

            return self

        def with_chapter_found(self, chapters):
            mocker.patch.object(Util, "verify_text_contains", return_value=True)

            return self.with_chapters([chapters])

        def with_chapter_not_found(self):
            mocker.patch.object(Util, "verify_text_contains", return_value=False)

            return self.with_chapters(["Chapter 1168", "Chapter 1169", "Chapter 1170"])

    return TcbOpSetUp()

class TestTcbOp:
    def test_chapter_found(self, tcbop_setup):
        tcbop_setup.with_chapter_found("Chapter 1171")
        result = tcbop_setup.tcbop.get_chapter_images("1171")

        assert result is True

    def test_chapter_not_found(self, tcbop_setup):
        tcbop_setup.with_chapter_not_found()
        result = tcbop_setup.tcbop.get_chapter_images("1171")

        assert result is False

    def test_check_chapter_limit(self, tcbop_setup):
        tcbop_setup.with_chapter_not_found()
        tcbop_setup.tcbop.get_chapter_images("1171")

        assert tcbop_setup.selenium.get_text.call_count <= 3