import time

from selenium import webdriver
from selenium.common import TimeoutException, ElementNotVisibleException
from selenium.webdriver import Proxy, DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

selenium_grid_url = "http://127.0.0.1:4444/wd/hub"


def options():
    myproxy = "192.168.3.241:7890"
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': myproxy,
        'ftpProxy': myproxy,
        "sslProxy": myproxy,
        'noProxy': 'localhost,127.0.0.1'
    })
    options = ChromeOptions()
    options.set_capability("browserVersion", "131.0")
    options.set_capability("browserName", "chrome")
    options.set_capability("proxy", proxy.to_capabilities())
    return options


def wait(driver) -> bool:
    try:
        WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH,
                      '//*[@id="cdk-overlay-0"]/nz-modal-confirm-container/div/div/div/div/div[2]/button'))
    except TimeoutException:
        return False

    return True

with webdriver.Remote(command_executor=selenium_grid_url, options=options()) as driver:
    driver.maximize_window()
    ss = str(int(time.time()))
    driver.get(url="https://tidy3d.simulation.cloud/")
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="email"]'))
    print(element)
    driver.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys("ihvuligagam123@snapmail.cc")

    driver.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys("1983#GEhui")
    driver.save_screenshot("tidy3d-" + ss + "-01" + ".png")
    driver.find_element(by=By.XPATH, value='//*[@id="sign-in-with-email"]').click()
    while True:
        print("Hello")
        if wait(driver):
            print("True")
            break
    # last_height = None
    # while True:
    #     new_height = driver.execute_script(
    #         "return document.documentElement.scrollHeight || document.body.scrollHeight;")
    #     if last_height == new_height:
    #         break
    #     last_height = new_height
    if driver.execute_script("return document.readyState") == "complete":
        print("jiaziai finiash")

    driver.save_screenshot("tidy3d-" + ss + "-02" + ".png")
    confirm = driver.find_element(By.XPATH,
                                  '//*[@id="cdk-overlay-0"]/nz-modal-confirm-container/div/div/div/div/div[2]/button')
    print(confirm)
    confirm.click()
    # webdriver.ActionChains(driver).move_to_element(confirm).click(confirm).perform()

    # driver.save_screenshot("tidy3d-" + ss + "-03" + ".png")
    # is_disappeared = WebDriverWait(driver, 100, 1,
    #                                ElementNotVisibleException).until_not(
    #     lambda x: x.find_element(By.XPATH,
    #                              '//*[@id="cdk-overlay-0"]/nz-modal-confirm-container/div/div/div').is_displayed())
    # print(is_disappeared)
    # if is_disappeared:
    #     driver.save_screenshot("tidy3d-" + ss + "-04" + ".png")
