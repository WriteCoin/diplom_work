from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
import conf
#%%
установить_вывод_всех_ячеек()
#%%
# Создание экземпляра
mail = imaplib.IMAP4_SSL('imap.yandex.ru')
#%%
# Авторизация
mail.login(conf.EMAIL, conf.PASSWORD)
#%%
# Выбрать все входящие
mail.select("inbox")
#%%
# Получение указателей всех писем
result, data = mail.search(None, "ALL")
result, data
#%%
# Чтение последнего сообщения
ids = data[0]
id_list = ids.split()

typ, data = mail.fetch(id_list[-1], '(RFC822)')
data[0][1]
data
#%%
# Переменная письма
msg = data 
#%%
# Извлечение письма
msg = email.message_from_bytes(msg[0][1])
msg
#%%
# Дата получения, ID и Email отправителя
letter_date = email.utils.parsedate_tz(msg["Date"])
letter_id = msg["Message-ID"]
letter_from = msg["Return-path"]

letter_date
letter_id
letter_from
#%%
# Тема письма
if not msg["Subject"] is None:
    subject = decode_header(msg["Subject"])[0][0].decode()
else:
    subject = "Без темы"