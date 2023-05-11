import telegram
from telegram.ext import Updater
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
import conf
#%%
установить_вывод_всех_ячеек()
#%% 
bot_token = conf.BOT_TOKEN
bot_chatID = conf.BOT_CHAT_ID
#%%
bot = telegram.Bot(token=bot_token)
#%%
bot
#%%
updates = bot.get_updates()
#%%
updates
#%%
for update in updates:
    if update.message:
        print(update.message.text)
#%%
# Получаем информацию о чате
chat_info = bot.get_chat(chat_id=bot_chatID)
#%%
for attr in dir(chat_info):
    attr, getattr(chat_info, attr)
#%%
# название чата
chat_title = chat_info.title
print(chat_title)
# название собеседника - если название чата None
chat_info.full_name
chat_info.first_name, chat_info.last_name
#%%
# Получаем информацию о пользователях в чате
chat_members = bot.get_chat_member_count(chat_id=bot_chatID)
chat_members
#%%
# Получаем последние сообщения в чате
chat_info.pinned_message
latest_messages = bot.get_history(chat_id=bot_chatID, limit=200)
latest_messages