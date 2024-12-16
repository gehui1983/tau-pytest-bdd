import time

from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

selenium_grid_url = "http://127.0.0.1:4444/wd/hub"


def add_cookie(drive):
    drive.add_cookie({'name': '_c_WBKFRo', 'value': 'IIVDvw4Gxoqfo3XaOtYmuZ7836waFhBmwz8PuDbi'})

    drive.add_cookie({'name': '_nb_ioWEgULi', 'value': ''})

    drive.add_cookie({'name': 'acw_tc', 'value': '0bde430217342649157051086ea27ac05f06e94c92f81472bf8e264f9dc0d3'})
    js = 'window.localStorage.setItem("token","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJGSU5fUCIsImlhdCI6MTczNDE1NTEzOCwiZXhwIjoxNzM0NzU5OTM4LCJ1c2VyTm8iOiJ3YW5nbWF6aSIsInVzZXJJZCI6IjQifQ.IDx7-OtVuqry6k4OPuylOZa3JVBsLKXE_oN2xF59R94") '
    drive.execute_script(js)
    drive.refresh()


myproxy = "192.168.3.241:8888"
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
# options.set_capability("sslCertificate", "/home/james/charles-ssl-proxying-certificate.pem")
ss = str(int(time.time()))
with webdriver.Remote(command_executor=selenium_grid_url, options=options) as driver:
    driver.maximize_window()
    driver.get(url='https://op.xhdigit.com/')
    add_cookie(driver)
    driver.get(url="https://op.xhdigit.com/#/product")
    driver.save_screenshot("xhdigit-" + ss + "-1-" + ".png")
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/div[2]/button").click()

    element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH,
                                                                       '/html/body/div/div/div[1]/ul/li[1]/div'))

    print(element)
    driver.save_screenshot("xhdigit-" + ss + "-2-" + ".png")
