# веб-автоматизация VK, для авторизации, создания приложения и получения всех необходимых данных
# импорт библиотек
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
from for_selenium.driver.script import FindOptions, Script, By
import for_selenium.driver.script
importlib.reload(for_selenium.driver.script)
from selenium.webdriver import Chrome, ChromeOptions
import undetected_chromedriver as uc
import conf
import json
#%%
driver = Chrome()
#%%
# служебные блоки
# объявление объекта скрипта
script = Script(url="https://vk.com")
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
script.wait_page_load()