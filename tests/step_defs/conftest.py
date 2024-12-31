from pytest_bdd import given
# Constants
import pytest
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.proxy import ProxyType
DUCKDUCKGO_HOME = 'https://duckduckgo.com/'


# Hooks

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f'Step failed: {step}')


# Fixtures

@pytest.fixture
def browser():
    # For this example, we will use Firefox
    # You can change this fixture to use other browsers, too.
    # A better practice would be to get browser choice from a config file.
    b = webdriver.Firefox()
    b.implicitly_wait(10)
    yield b
    b.quit()


# Shared Given Steps

@given('the DuckDuckGo home page is displayed', target_fixture='ddg_home')
def ddg_home(browser):
    browser.get(DUCKDUCKGO_HOME)





@pytest.fixture
def chrome_browser():
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
    # options.set_capability("proxy", proxy.to_capabilities())
    options.set_capability("se:downloadsEnabled", False)
    # se:downloadsEnabled
    options.add_experimental_option("prefs", {
        "download.default_directory": "/tmp/",
        "download.prompt_for_download": False,
        "profile.default_content_settings.popups": 0,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    with webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options) as driver:
        driver.maximize_window()
        driver.implicitly_wait(time_to_wait=3.0)
        yield driver
