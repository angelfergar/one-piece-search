import pytest

# Specific Fixtures

@pytest.fixture
def chapter_mocker(mocker, mock_selenium):
    class ChapterMocker:
        def __init__(self):
            self.elements = [mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock()]
            self.element = mocker.MagicMock()

            self.selenium = mock_selenium

        def as_list(self):
            self.selenium.get_element_list.return_value = self.elements
            self.last_element = self.elements[-1]
            return self

        def as_element(self):
             self.selenium.get_element.return_value = self.element
             return self

        def with_text(self, text):
            self.selenium.get_text.return_value = text
            return self

    return ChapterMocker()

# Tests
class TestFindChapter:
    def test_find_last_item(self, manga_plus, chapter_mocker):
        chapter_mocker.as_list().with_text("#1170")
        manga_plus.find_chapter()

        chapter_mocker.selenium.get_text.assert_called_once_with(element=chapter_mocker.last_element)

    def test_get_next_chapter(self, manga_plus, chapter_mocker):
        chapter_mocker.as_list().with_text("#1170")
        result = manga_plus.find_chapter()

        assert result == 1171

    def test_chapter_format(self, manga_plus, chapter_mocker):
        chapter_mocker.as_list().with_text("1170")

        with pytest.raises(ValueError, match="Format not supported for chapter number:"):
            manga_plus.find_chapter()

class TestFindBreakWeek:
    def test_week_format(self, manga_plus, chapter_mocker):
        chapter_mocker.as_element().with_text("El próximo capítulo llega el Sunday, May 10, 17:00")
        result = manga_plus.find_break_week()

        assert result == "W19"

    def test_error_without_separator(self, manga_plus, chapter_mocker):
        chapter_mocker.as_element().with_text("próximo capítulo llega Sunday, May 10, 17:00")

        with pytest.raises(ValueError, match = "Format not supported for MangaPlus date: "):
            manga_plus.find_break_week()




