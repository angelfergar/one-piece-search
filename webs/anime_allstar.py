import time

from base.base import BasePage
from utils.utils import Util
from PIL import Image
import pytesseract
from rapidfuzz import fuzz
import re
import cv2
import numpy as np


class AllStar(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # Locators
    _link_chapters = "//div[@class='ast-post-format- blog-layout-4 ast-article-inner']"
    _extra_message = "//div[@class='ast-excerpt-container ast-blog-single-element']"
    _title_chapters = "//a[@rel='bookmark']"
    _chapter_images = "//div[@class='separator']"
    _new_chapter_images = "//div[@class='entry-content clear']/p"

    def normalize(self, text):
        text = text.upper()
        text = re.sub(r'[^A-Z0-9 ]', '', text)
        return text

    # Clean the image to make it more readable
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        thresh = cv2.bitwise_not(thresh)

        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1)

        thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        processed_path = "processed.png"
        cv2.imwrite(processed_path, thresh)

        return processed_path

    def capture_thumbnail_image(self):
        element = self.get_element(self._link_chapters, locator_type="xpath")
        location = element.location
        size = element.size

        self.driver.save_screenshot("full.png")
        image = Image.open("full.png")
        cropped_path = "title.png"

        left = location['x'] - 50
        top = location['y'] - 50
        right = left + size['width'] + 25
        bottom = top + size['height'] - 245

        cropped = image.crop((left, top, right, bottom))
        cropped.save(cropped_path)

        processed_path = self.preprocess_image(cropped_path)
        return processed_path

    def ocr_chapter_title(self, processed_path, language='spa'):
        config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:()\''
        text = pytesseract.image_to_string(processed_path, lang=language, config=config)
        print(text)
        return text.strip()

    def get_chapter_images(self, chapter):
        chapters_checked = 3
        min_images_required = 5
        language_warning = "(EN JAPONES)"
        spoiler_warning = "(SPOILER)"
        match_threshold = 75

        original_window = self.driver.current_window_handle
        chapter_listed = False

        self.wait_for_element(self._link_chapters, condition="visible")
        # Check the thumbnail
        processed_path = self.capture_thumbnail_image()
        in_japanese = self.ocr_chapter_title(processed_path)
        spoiler = self.ocr_chapter_title(processed_path, language='eng')

        match_score_jp = fuzz.ratio(self.normalize(in_japanese), self.normalize(language_warning))
        match_score_spoiler = fuzz.ratio(self.normalize(spoiler), self.normalize(spoiler_warning))

        is_japanese = match_score_jp > match_threshold
        is_spoiler = match_score_spoiler > match_threshold

        print(f'{in_japanese} vs {language_warning}')
        print(f'Score: {match_score_jp}')
        print(f'{in_japanese} vs {spoiler_warning}')
        print(f'Score: {match_score_spoiler}')

        # Check if there's another warning in the text for the chapter
        list_of_titles = self.get_elementList(self._title_chapters)
        list_of_messages = self.get_elementList(self._extra_message)

        for i in range(chapters_checked):
            container = list_of_titles[i]
            info_text = ""
            if list_of_messages:
                info_message = list_of_messages[i]
                info_text = self.get_text(element=info_message)

            is_warned = bool(info_text)
            if is_warned or is_spoiler or is_japanese:
                print("This link won't be opened as it contains an old chapter or a new one not translated")
                continue

            title_text = self.get_text(element=container)
            chapter_listed = Util.verify_text_contains(actual_text=chapter, expected_text=title_text)
            if chapter_listed:
                self.element_click(element=container)
                break
        if not chapter_listed:
            return False

        # There's a pop up, so we have to return to the One Piece tab
        all_windows = self.driver.window_handles
        for handle in all_windows:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                break

        # Check if there's a reasonable number of pages
        element = self.wait_for_element(locator=self._chapter_images, condition="click")
        if element:
            images_list = self.get_elementList(self._chapter_images)
        else:
            self.wait_for_element(locator=self._new_chapter_images, condition="click")
            images_list = self.get_elementList(self._new_chapter_images)

        return bool(images_list and len(images_list) > min_images_required)