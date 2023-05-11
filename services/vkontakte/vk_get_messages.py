from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
import requests
import conf
#%%
установить_вывод_всех_ячеек()
#%%
# исходные данные, из сайта https://vk.com/apps?act=manage
APP_ID = conf.APP_ID
APP_URL = conf.APP_URL
#%%
# данные API
API_VERSION = '5.131'
#%%
# запрос на получение access_token
response = requests.get(f"https://oauth.vk.com/authorize?client_id={APP_ID}&redirect_uri={APP_URL}&display=popup&scope=messages&response_type=token&v={API_VERSION}")
#%%
response.json()
#%%
ACCESS_TOKEN = conf.ACCESS_TOKEN

#%%
CODE = conf.CODE