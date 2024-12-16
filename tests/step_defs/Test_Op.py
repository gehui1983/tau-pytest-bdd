import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def add_cookie(drive):
    drive.add_cookie({'name': '_c_WBKFRo', 'value': 'IIVDvw4Gxoqfo3XaOtYmuZ7836waFhBmwz8PuDbi'})

    drive.add_cookie({'name': '_nb_ioWEgULi', 'value': ''})

    drive.add_cookie({'name': 'acw_tc', 'value': '0bde430217342649157051086ea27ac05f06e94c92f81472bf8e264f9dc0d3'})
    js = 'window.localStorage.setItem("token","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJGSU5fUCIsImlhdCI6MTczNDE1NTEzOCwiZXhwIjoxNzM0NzU5OTM4LCJ1c2VyTm8iOiJ3YW5nbWF6aSIsInVzZXJJZCI6IjQifQ.IDx7-OtVuqry6k4OPuylOZa3JVBsLKXE_oN2xF59R94") '
    drive.execute_script(js)
    drive.refresh()


ss = str(int(time.time()))


def test_op(chrome_browser):
    chrome_browser.maximize_window()
    chrome_browser.get(url='https://op.xhdigit.com/')
    add_cookie(chrome_browser)
    chrome_browser.get(url="https://op.xhdigit.com/#/product")
    chrome_browser.save_screenshot("xhdigit-" + ss + "-1-" + ".png")
    chrome_browser.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/div[2]/button").click()

    element = WebDriverWait(chrome_browser, 10).until(lambda x: x.find_element(By.XPATH,
                                                                               '/html/body/div/div/div[1]/ul/li[1]/div'))
    print(element)
    chrome_browser.save_screenshot("xhdigit-" + ss + "-2-" + ".png")
