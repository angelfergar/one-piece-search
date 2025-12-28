from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

# Generic methods for Selenium
class SeleniumDriver():

    def __init__(self, driver):
        self.driver = driver

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "partial_link":
            return By.PARTIAL_LINK_TEXT
        elif locator_type == "css":
            return By.CSS_SELECTOR
        else:
            print(f"Locator type: {locator_type} not found")
        return False

    def get_element(self, locator, locator_type="xpath", element=None, parent=None):
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            if parent is not None:
                search_context = parent
            else:
                search_context = self.driver

            element = search_context.find_element(by_type, locator)
        except:
            print(f"Element not found with locator: {locator} and locatorType: {locator_type}")
        return element

    def get_elementList(self, locator, locator_type="xpath", element_list=None):
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element_list = self.driver.find_elements(by_type, locator)
        except:
            print(f"Element list not found with locator: {locator} and locatorType: {locator_type}")
        return element_list

    def element_click(self, locator=None, locator_type="xpath", element=None, parent=None):
        try:
            if locator:
                if parent is not None:
                    element = self.get_element(locator, locator_type, parent=parent)
                else:
                    element = self.get_element(locator, locator_type)
            element.click()
        except:
            print(f"Could not click on element with locator: {locator} and locatorType: {locator_type}")

    def isElement_displayed(self, locator, locator_type="xpath", element=None):
        is_displayed = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
                if element is not None:
                    is_displayed = element.is_displayed()
                else:
                    print(f"Element not displayed with locator: {locator} and locatorType: {locator_type}")
                return is_displayed
        except:
            self.log.error(f"Element not found with locator: {locator} and locatorType: {locator_type}")
            return False

    def wait_for_element(self, locator, locator_type="xpath", condition="present",timeout=10, poll_frequency=0.5, element=None):
        """
        List of conditions:
        1. present  - presence_of_element_located
        2. visible - visibility_of_element_located
        3. click - element_to_be_clickable
        """
        try:
            if locator:
                by_type = self.get_by_type(locator_type)
                wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency, ignored_exceptions=
                [
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException
                ])
                if condition == "present":
                    element = wait.until(EC.presence_of_element_located((by_type, locator)))
                elif condition == "visible":
                    element = wait.until(EC.visibility_of_element_located((by_type, locator)))
                elif condition == "click":
                    element = wait.until(EC.element_to_be_clickable((by_type, locator)))
                else:
                    print(f"Invalid condition: {condition} - Use 'present', 'visible', or 'click'")
        except:
            print(f"Element not found with locator: {locator} and locatorType: {locator_type}")
        return element

    def switch_frame(self, id="", name="", index=None):
        if id:
            self.driver.switch_to.frame(id)
        elif name:
            self.driver.switch_to.frame(name)
        else:
            self.driver.switch_to.frame(index)

    # Method to go back to the main frame of the web
    def switchTo_defaultContent(self):
        self.driver.switch_to.default_content()

    # Generic method to obtain the text from the elements in the web
    def get_text(self, locator=None, locator_type="xpath", element=None):
        text = ""
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
                text = text.strip()
            if text:
                text = text.strip()
            else:
                print(f"Element had no visible text.")
        except:
            print(f"Failed to get the text in the element with locator: {locator} and locatorType: {locator_type}")
            text = None
        return text

    def getElement_attributeValue(self, attribute, locator=None, locator_type="xpath", element=None):
        value = None
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            value = element.get_attribute(attribute)
            print(f"Got the value for the attribute: {attribute}  of the element with locator: {locator}"
                  f" and locatorType: {locator_type}")
        except:
            print(f"Could not get the value for the attribute: {attribute}  of the element with locator: {locator}"
                  f" and locatorType: {locator_type}")
        return value

    def scroll_toElement(self, locator=None, locator_type="xpath", element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            print(f"Page was scrolled to element with locator: {locator} and locatorType: {locator_type}")
        except:
            print(f"Could not scroll to element with locator: {locator} and locatorType: {locator_type}")

    def scroll_web(self, direction):
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0,-12250);")
            print(f"Page was scrolled {direction}")
        elif direction == "down":
            self.driver.execute_script("window.scrollBy(0,12250);")
            print(f"Page was scrolled {direction}")