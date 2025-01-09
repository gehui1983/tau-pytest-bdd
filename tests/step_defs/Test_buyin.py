import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def add_cookie(drive):
    cookie = '''passport_csrf_token=123e1557e047eaa939af301781d81a62; passport_csrf_token_default=123e1557e047eaa939af301781d81a62; ttwid=1%7CIA6afkepGpD2f1dvRzgenrBI13tIZTbcYsyf9kUheM8%7C1735034580%7Cfb3d6ded6fd58c210f976fe03acb4e19a91e3db095213fbbadbd035ac9092ddc; uid_tt=1717e809e702e47e5cc24fc5fed8a668; uid_tt_ss=1717e809e702e47e5cc24fc5fed8a668; sid_tt=d1d47c7811689c0167956d0842dde65c; sessionid=d1d47c7811689c0167956d0842dde65c; sessionid_ss=d1d47c7811689c0167956d0842dde65c; is_staff_user=false; store-region=cn-zj; store-region-src=uid; odin_tt=10cecf85e3efb853e39d0621cd29af5027f50c7ae96e60b884166b6108736e7e304fdda27e463d3fb2d0cb51d67c01a9da1a2d98869aeb6f9522fb8616554bb6; sid_guard=d1d47c7811689c0167956d0842dde65c%7C1735034584%7C5183999%7CSat%2C+22-Feb-2025+10%3A03%3A03+GMT; sid_ucp_v1=1.0.0-KDc3MTQ5MTljYzFhN2E1ZmIyN2E0NTI3ZGQ1NWFjODhiOTBmYzk4MzIKGAit_cDa-ozhBxDYjaq7BhiPESAMOAhAJhoCbGYiIGQxZDQ3Yzc4MTE2ODljMDE2Nzk1NmQwODQyZGRlNjVj; ssid_ucp_v1=1.0.0-KDc3MTQ5MTljYzFhN2E1ZmIyN2E0NTI3ZGQ1NWFjODhiOTBmYzk4MzIKGAit_cDa-ozhBxDYjaq7BhiPESAMOAhAJhoCbGYiIGQxZDQ3Yzc4MTE2ODljMDE2Nzk1NmQwODQyZGRlNjVj; BUYIN_SASID=SID2_7451913467422146867'''
    arr = cookie.split("; ")
    for a in arr:
        drive.add_cookie({'name': a.split('=')[0], 'value': a.split('=')[1]})
    print(drive.get_cookies())
    # drive.refresh()


ss = str(int(time.time()))


def test_buyin(chrome_browser):
    chrome_browser.maximize_window()
    chrome_browser.get(url='https://buyin.jinritemai.com/dashboard/merch-picking-library?pre_universal_page_params_id=&universal_page_params_id=595b55da-d0b6-495b-a37e-13524b948e8c')
    add_cookie(chrome_browser)
    chrome_browser.get(url='https://buyin.jinritemai.com/dashboard/merch-picking-library?pre_universal_page_params_id=&universal_page_params_id=595b55da-d0b6-495b-a37e-13524b948e8c')

    time.sleep(20)
    chrome_browser.save_screenshot("buyin-" + ss + "-1-" + ".png")
