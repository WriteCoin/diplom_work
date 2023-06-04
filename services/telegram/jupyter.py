from telethon import TelegramClient, sync, events
from telethon.tl.types import User, TypeUserProfilePhoto, TypeUserStatus, UserProfilePhoto
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
import conf
importlib.reload(conf)
from pprint import pprint
#%% 
#%%
установить_вывод_всех_ячеек()
#%%
# Создание клиента телеграмма
client = TelegramClient(conf.SESSION_NAME, conf.API_ID, conf.API_HASH)
#%%
client
#%%
# Вход в клиент
await client.start(conf.PHONE_NUMBER)
#%%
user = await client.get_me()
#%%
user
#%%
user.stringify()
#%%
# Получение всех диалогов
dialogs = await client.get_dialogs()
# async def get_dialogs():
#     async for dialog in client.iter_dialogs():
#         dialog
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
#%%
# Отслеживание новых сообщений
@client.on(events.NewMessage())
async def normal_handler(event):
#    print(event.message)
    print(event.message.to_dict()['message'])
#%%
await client.run_until_disconnected()