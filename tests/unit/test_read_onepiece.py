import pytest
from utils.utils import Util
from webs.read_onepiece import ReadOnePiece

@pytest.fixture
def read_op_setup(web_mocker, mocker, mock_selenium):
    class ReadOnePieceSetUp:
        def __init__(self):
            self.read_op = web_mocker(ReadOnePiece)
            self.chapters_checked = 3

            self.selenium = mock_selenium

        def with_chapters(self, titles):
            containers = [mocker.MagicMock() for _ in titles]
            self.selenium.get_element_list.return_value = containers
            self.selenium.get_element.side_effect = containers
            self.selenium.get_text.side_effect = titles

            return self

        def with_chapter_found(self, chapter):
            mocker.patch.object(Util, "verify_text_contains", return_value=True)

            return self.with_chapters([chapter])

        def with_chapter_not_found(self):
            mocker.patch.object(Util, "verify_text_contains", return_value=False)

            return self.with_chapters(["Chapter 1168", "Chapter 1169", "Chapter 1170"])

    return ReadOnePieceSetUp()

class TestReadOnePiece:
    def test_chapter_found(self, read_op_setup):
        read_op_setup.with_chapter_found("Chapter 1171")
        result = read_op_setup.read_op.get_chapter_images("1171")

        assert result is True

    def test_chapter_not_found(self, read_op_setup):
        read_op_setup.with_chapter_not_found()
        result = read_op_setup.read_op.get_chapter_images("1171")

        assert result is False

    def test_check_chapter_limit(self, read_op_setup):
        read_op_setup.with_chapter_not_found()
        read_op_setup.read_op.get_chapter_images("1171")

        assert read_op_setup.selenium.get_text.call_count <= 3
