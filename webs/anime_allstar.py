from base.base import BasePage
from utils.utils import Util
from time import sleep

class AllStar(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _link_chapters = "//div[@class='ast-post-format- blog-layout-4 ast-article-inner']"
    _title_chapters = "//a[@rel='bookmark']"
    _chapter_images = "//div[@class='separator']"

    def get_chapter_images(self, chapter):
        chapter_listed = False
        chapters_checked = 3
        original_window = self.driver.current_window_handle
        self.wait_for_element(self._link_chapters, condition="visible")
        list_of_titles = self.get_elementList(self._title_chapters)
        for  i in range(chapters_checked):
            container = list_of_titles[i]
            title_text = self.get_text(element=container)
            chapter_listed = self.utils.verify_text_contains(chapter, title_text)
            if chapter_listed:
                self.element_click(element=container)
                break
        # There's a pop up, so we have to return to the One Piece tab
        all_windows = self.driver.window_handles
        for handle in all_windows:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break
        # Check if there's a reasonable number of pages
        self.wait_for_element(self._chapter_images,condition="visible")
        images_list = self.get_elementList(self._chapter_images)
        if len(images_list) > 10:
            return True

        return False