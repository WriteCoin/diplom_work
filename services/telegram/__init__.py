from telethon.sync import TelegramClient
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
import conf
importlib.reload(conf)
from pprint import pprint
#%%
установить_вывод_всех_ячеек()
#%%
# Создание клиента телеграмма
client = TelegramClient(conf.SESSION_NAME, conf.API_ID, conf.API_HASH)
#%%
# Вход в клиент
await client.start(conf.PHONE_NUMBER)
#%%
# Получение всех диалогов
dialogs = await client.get_dialogs()
#%%
dialogs
#%%
# Отображение имен и ID всех диалогов
for dialog in dialogs:
    dialog.name, 'has ID', dialog.id
    messages = await client.get_messages(dialog.input_entity, limit=200)
    pprint("Messages", messages)
    # print("====================================================================")
#%%
await client.log_out()