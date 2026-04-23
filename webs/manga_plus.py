from base.base import BasePage
from web_config import WebConfig
from datetime import datetime

class MangaPlus(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # Locators
    _text = "//span[contains(text(), 'próximo capítulo')]"
    _chapter = "//p[@class='ChapterListItem-module_name_3h9dj']"

    def find_break_week(self):
        self.wait_for_element(locator=self._text, condition="visible")
        release_date = self.get_element(locator=self._text)
        release_text = self.get_text(element=release_date)

        parts = release_text.split("el")[1]
        if len(parts) < 2:
            raise ValueError(f"Format not supported for MangaPlus date: '{release_text}'")
        date_release = parts[1].strip()

        release_format = datetime.strptime(date_release, "%A, %b %d, %H:%M")
        year, week, _ = release_format.isocalendar()
        return f'W{week}'

    def find_chapter(self):
        self.wait_for_element(locator=self._chapter,condition="visible")
        chapter_number = self.get_elementList(locator=self._chapter)

        chapter_text = self.get_text(element=chapter_number[-1])

        if not chapter_text.startswith("#"):
            raise ValueError(f"Format not supported for chapter number: '{chapter_text}")

        chapter = chapter_text[1:]
        return int(chapter) + 1



