# Generated by Selenium IDE
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class TestSnapmailcc():
    def setup_method(self):
        pass

    def teardown_method(self, method):
        pass

    def test_snapmailcc(self, chrome_browser):
        chrome_browser.get("https://www.snapmail.cc/#/")
        chrome_browser.find_element(By.LINK_TEXT, "Sign Up").click()
        chrome_browser.find_element(By.ID, "email").click()
        ss = str(int(time.time()))
        pre = "gehui19_"+ss
        email = pre+"@snapmail.cc"
        print(email)
        chrome_browser.find_element(By.ID, "email").send_keys(email)
        chrome_browser.find_element(By.ID, "password").send_keys("1983#gehui")
        chrome_browser.find_element(By.CSS_SELECTOR, ".btn:nth-child(1)").click()
        # element = chrome_browser.find_element(By.CSS_SELECTOR, ".btn:nth-child(1)")
        # actions = ActionChains(chrome_browser)
        # actions.move_to_element(element).perform()

# gehui19_1734358944@snapmail.cc
