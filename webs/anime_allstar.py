from base.base import BasePage
from utils.utils import Util
from PIL import Image
import pytesseract
from rapidfuzz import fuzz
import re
import cv2

class AllStar(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    def normalize(self, text):
        text = text.upper()
        text = re.sub(r'[^A-Z0-9 ]', '', text)
        return text

    # Clean the image to make it more readable
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        img = cv2.bilateralFilter(img, 11, 17, 17)
        img = cv2.bitwise_not(img)

        processed_path = "processed.png"
        cv2.imwrite(processed_path, img)
        return processed_path

    # Locators
    _link_chapters = "//div[@class='ast-post-format- blog-layout-4 ast-article-inner']"
    _extra_message = "//div[@class='ast-excerpt-container ast-blog-single-element']"
    _title_chapters = "//a[@rel='bookmark']"
    _chapter_images = "//div[@class='separator']"

    def ocr_chapter_title(self):

        element = self.get_element(self._link_chapters, locator_type="xpath")

        location = element.location
        size = element.size

        self.driver.save_screenshot("full.png")
        image = Image.open("full.png")

        left = location['x'] - 50
        top = location['y'] - 50
        right = left + size['width'] + 25
        bottom = top + size['height'] - 250

        cropped = image.crop((left, top, right, bottom))
        cropped.save("title.png")

        processed = self.preprocess_image("title.png")

        config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:()\''
        text = pytesseract.image_to_string(processed, lang='spa', config=config)

        return text.strip()

    def get_chapter_images(self, chapter):
        chapter_listed = False
        chapters_checked = 3
        min_images_required = 10
        original_window = self.driver.current_window_handle
        language_warning = "(EN JAPONES)"

        self.wait_for_element(self._link_chapters, condition="visible")
        # Check the thumbnail
        in_japanese = self.ocr_chapter_title()
        match_score = fuzz.partial_ratio(self.normalize(in_japanese), self.normalize(language_warning))
        print(f'{in_japanese} vs {language_warning}')
        print(f'Score: {match_score}')

        # Check if there's another warning in the text for the chapter
        list_of_titles = self.get_elementList(self._title_chapters)
        list_of_messages = self.get_elementList(self._extra_message)
        for i in range(chapters_checked):
            container = list_of_titles[i]
            info_message = list_of_messages[i]
            info_text = self.get_text(element=info_message)
            if info_text != "" or match_score > 75:
                print(info_text)
                print("This link won't be opened as it contains an old chapter or a new one not translated")
                continue
            else:
                title_text = self.get_text(element=container)
                chapter_listed = Util.verify_text_contains(self, actual_text=chapter, expected_text=title_text)
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
        if len(images_list) > min_images_required:
            return True

        return False