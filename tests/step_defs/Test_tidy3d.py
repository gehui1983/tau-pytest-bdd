import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def wait(driver) -> bool:
    try:
        WebDriverWait(driver, 100).until(lambda x: x.find_element(By.XPATH,
                              '//*[@id="cdk-overlay-0"]/nz-modal-confirm-container/div/div/div/div/div[2]/button'))
    except TimeoutException:
        return False

    return True


def test_tidy3d(chrome_browser):
    chrome_browser.maximize_window()
    ss = str(int(time.time()))
    chrome_browser.get(url="https://tidy3d.simulation.cloud/")
    element = WebDriverWait(chrome_browser, 10).until(lambda x: x.find_element(By.XPATH, '//*[@id="email"]'))
    print(element)
    chrome_browser.find_element(by=By.XPATH, value='//*[@id="email"]').send_keys("ihvuligagam123@snapmail.cc")

    chrome_browser.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys("1983#GEhui")
    chrome_browser.save_screenshot("tidy3d-" + ss + "-01" + ".png")
    chrome_browser.find_element(by=By.XPATH, value='//*[@id="sign-in-with-email"]').click()
    while True:
        print("Hello")
        if wait(chrome_browser):
            print("True")
            break
    # last_height = None
    # while True:
    #     new_height = driver.execute_script(
    #         "return document.documentElement.scrollHeight || document.body.scrollHeight;")
    #     if last_height == new_height:
    #         break
    #     last_height = new_height
    if chrome_browser.execute_script("return document.readyState") == "complete":
        print("jiaziai finiash")

    chrome_browser.save_screenshot("tidy3d-" + ss + "-02" + ".png")
    confirm = chrome_browser.find_element(By.XPATH,
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
