# веб-автоматизация VK, для авторизации, создания приложения и получения всех необходимых данных
# импорт библиотек
from selenium.webdriver.remote.webelement import WebElement
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
from WebAutomation.for_selenium.driver.script import FindOptions, Script, By
import for_selenium.driver.script
importlib.reload(for_selenium.driver.script)
# from selenium.webdriver import Chrome, ChromeOptions
from urllib.parse import urlparse
import undetected_chromedriver as uc
import conf
import json
#%%
установить_вывод_всех_ячеек()
#%%
# загрузка информации об аккаунтах
with open('conf.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)
    data
account = data['accounts'][0]
phone = account['phone']
password = account['password']
email = account['email']
client_id = account['client_id']
client_secret = account['client_secret']
access_token = account['access_token']
login = phone if not email else email
#%%
# служебные блоки
# объявление объекта скрипта
script = Script(url="https://vk.com", cookie_path=f"cookies/{login}")
#%%
# запуск браузера

driver = uc.Chrome()
#%%
# обновление скрипта
script.set_driver(driver)
#%%
# авторизация
# загрузка первой страницы
driver.get(conf.URL)
#%%
# первая форма
login_el = script.wait_element(FindOptions(By.ID, 'index_email'))
login_el
password_el = script.wait_element(FindOptions(By.NAME, 'password'))
button_el = script.wait_element(FindOptions(By.CSS_SELECTOR, 'button[type="submit"]'))

login_el.send_keys(login)
if password_el.get_attribute('style') != 'display: none;':
    password_el.send_keys(password)
button_el.click()
#%%
# форма по VK ID
script.wait_page_load()
if driver.title == 'VK ID':
    password_el = script.wait_element(FindOptions(By.CSS_SELECTOR, 'input[type="password"]'))
    password_el.send_keys(password)
    script.wait_element(FindOptions(By.CSS_SELECTOR, 'button[type="submit"]')).click()
#%%
## Главная страница
# ожидание уведомления с подтверждением номера
try:
    def frame_predicate(frame: WebElement):
        src = frame.get_attribute('src')
        parsed_url = urlparse(src)
        return parsed_url.netloc + parsed_url.path == "id.vk.com/auth"
    script.wait_elements(FindOptions(By.TAG_NAME, 'iframe'))
    frame = find(frame_predicate, script.wait_elements(FindOptions(By.TAG_NAME, 'iframe'), 5.))
    frame
    # script.wait_element_by_inner_html(FindOptions(By.I, "span"), "Проверьте актуальность номера телефона, чтобы защитить свою страницу", 10., 1.)
    # driver.find_element_by_xpath("//div[contains(@id, 'footer')]")
    # driver.find_element_by_xpath("//*[contains(text(), 'Проверьте актуальность номера телефона, чтобы защитить свою страницу')]")
    # with script.work_frame(frame) as frame:
    #     script.wait_element(FindOptions(By.XPATH, "//*[normalize-space(.)='Проверьте актуальность номера телефона, чтобы защитить свою страницу']"), 5., 1.)
        # script.wait_element(FindOptions(By.CSS_SELECTOR, "div[aria-label=\"Закрыть\"] > svg"), 5.).click()
except Exception as e:
    print(e)
#%%
script.wait_page_load()
#%%
