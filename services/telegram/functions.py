from telethon import TelegramClient, sync, events
from telethon.tl.types import User, TypeUserProfilePhoto, TypeUserStatus, UserProfilePhoto, TypeBotInlineMessage
from WebAutomation.general_utils import *
from WebAutomation.general_utils.jupyter import установить_вывод_всех_ячеек
from conf import PHONE_NUMBER, SESSION_NAME, API_ID, API_HASH
import asyncio

async def connection(phone, session_name, api_id, api_hash, user_func: Callable[[User], None] = None, message_func: Callable[[dict], None] = None):
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(phone)

    user = await client.get_me()

    if not user_func is None:
        await user_func(user)

    # Отслеживание новых сообщений
    @client.on(events.NewMessage())
    async def message_handler(event):
    #    print(event.message)
        msg = event.message.to_dict()
        print('msg', msg)
        print('message', msg['message'])
        if not message_func is None:
            message_func(msg)
    await client.run_until_disconnected()

    print("Завершение функции")

if '-t' in sys.argv and __name__ == '__main__':
    # Тестовый режим запуска
    pass
elif __name__ == '__main__':
    # Релизный режим запуска
    asyncio.run(connection(PHONE_NUMBER, SESSION_NAME, API_ID, API_HASH))