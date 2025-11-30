import pytesseract
import cv2

class Util():

    def verify_list_length(self, expected_list, actual_list):
        expected_length = len(expected_list)
        actual_length = len(actual_list)
        if expected_length == actual_length:
            return True
        else:
            print("The list's length is not the same as the expected")
            return False

    def verify_text_contains(self, actual_text, expected_text):
        print(actual_text)
        print(expected_text)
        if actual_text.lower() in expected_text.lower():
            return True
        else:
            print("Text does not contain the expected content")
            return False

    def get_image_number(self):
        # Grayscale, Gaussian blur, Otsu's threshold
        image = cv2.imread('my_image.png')
        y = 300
        x = 0
        h = 200
        w = 1000
        image = image[y:y + h, x:x + w]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(invert)
        print("Text: " + text)
        return text