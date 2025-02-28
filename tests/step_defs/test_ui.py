from selenium.webdriver import Proxy
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType

options = ChromeOptions()
options.set_capability('se:recordVideo', True)
options.set_capability('se:screenResolution', '1920x1080')
options.set_capability('se:name', 'test_visit_basic_auth_secured_page (ChromeTests)')
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': '192.168.3.241:8889',
    'sslProxy': '192.168.3.241:8889',
    'ftpProxy': '192.168.3.241:8889'
})

options.proxy=proxy
driver = webdriver.Remote(options=options, command_executor="http://localhost:4444")
driver.maximize_window()
driver.get("https://www.baidu.com")
driver.save_screenshot(filename="./shub.png")
driver.quit()