from base.base import BasePage
from utils.utils import Util
from PIL import Image
import pytesseract
from rapidfuzz import fuzz
import re
import cv2

class TcbScans(BasePage):

    utils = Util()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _link_to_chapters = "post-details" # class
    _title_list = "post-title" # class
    _button_to_chapter = "more-link.button" # class

    _chapter_images = "//img[@decoding='async']"
    _first_image = "(//img[@decoding='async'])[1]"
    _chapter_title = "//h1[contains(text(), 'One Piece')]"

    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    def normalize(self, text):
        text = text.upper()
        text = re.sub(r'[^A-Z0-9 ]', '', text)
        return text

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_path = "processed.png"
        cv2.imwrite(processed_path, img)
        return processed_path

    def ocr_chapter_title(self):

        element = self.get_element(self._chapter_title, locator_type="xpath")

        location = element.location
        size = element.size

        self.driver.save_screenshot("full.png")
        image = Image.open("full.png")

        left = location['x']
        top = location['y'] + 835
        right = left + size['width'] + 250
        bottom = top + size['height'] + 6

        cropped = image.crop((left, top, right, bottom))
        cropped.save("title.png")

        processed = self.preprocess_image("title.png")

        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:\''
        text = pytesseract.image_to_string(processed, config=config)

        return text.strip()

    def get_chapter_images(self, chapter):
        chapter_listed = False
        # Open the list of chapters
        self.wait_for_element(self._link_to_chapters, locator_type="class", condition="visible")
        list_of_chapters = self.get_elementList(self._link_to_chapters, locator_type="class")

        for container in list_of_chapters:
            title = self.get_element(self._title_list, locator_type="class", parent=container)
            title_text = self.get_text(element=title)
            chapter_found = self.utils.verify_text_contains(chapter, title_text)
            if chapter_found:
                self.element_click(self._button_to_chapter, locator_type="class", parent=container)
                chapter_listed = True
                break
            else:
                continue

        # Actions in the Chapter Web
        if chapter_listed:
            self.wait_for_element(self._chapter_images, condition="visible")
            self.wait_for_element(self._chapter_title, condition="visible")

            current_list = self.get_elementList(self._chapter_images)
            chapter_number = self.ocr_chapter_title()
            match_score = fuzz.partial_ratio(self.normalize(chapter_number), self.normalize(chapter))
            print(f'Title: {chapter_number}\nChapter: {chapter}')
            print(f'Score: {match_score}')
            if len(current_list) > 10 and match_score > 75:
                return True
        else:
            return False