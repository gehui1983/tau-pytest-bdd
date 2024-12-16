from selenium.common import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class LoginObject:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def search_input(self) -> WebElement:
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.ID, 'kw'))
        return self.driver.find_element(by=By.ID, value="kw")

    def search_button(self) -> WebElement:
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.ID, 'su'))
        return self.driver.find_element(by=By.ID, value="su")

    def validate(self) -> bool:
        # WebDriverWait(self.driver, 10).until(lambda x: x.find_element(By.LINK_TEXT, 'china - 百度翻译'))
        is_disappeared = WebDriverWait(self.driver, 10, 1,
                                       ElementNotVisibleException).until_not(
            lambda x: x.find_element(By.LINK_TEXT,
                                     'china - 百度翻译').is_displayed())
        # is_disappeared = WebDriverWait(self.driver, 10, 1,
        #                                ElementNotVisibleException).until_not(
        #     lambda x: x.find_element(By.ID,
        #                              'su').is_displayed())
        return is_disappeared
