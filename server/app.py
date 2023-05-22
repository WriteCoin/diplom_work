import time
import threading
from typing_extensions import runtime
from respect_validation import Validator as v
from flask import Flask, jsonify, url_for, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from get_app import app, socketio, session, socket_app
from sqlalchemy import select
from get_conf import conf

# from flask_sqlalchemy import SQLAlchemy
from WebAutomation.general_utils import *
from sqlalchemy import text
from sqlalchemy.ext.serializer import dumps
from sqlalchemy.orm import aliased
from db import (
    Email,
    EmailProfile,
    Messenger,
    Session,
    Base,
    engine,
    all_models,
    metadata,
    EmailMessage,
    as_dict,
)
from WebAutomation.diplom_work.services.mail import (
    MailMessage,
    connection as email_connection,
    get_email_data,
)
from pprint import pprint
import routes.email_service_router
import routes.email_profile_router
import routes.email_message_router


# Обработчик подключения клиента к серверу
@socketio.on("connect")
def connect_handler():
    print("Client connected")


# Обработчик отключения клиента от сервера
@socketio.on("disconnect")
def disconnect_handler():
    print("Client disconnected")


def email_service_update(
    email_service: Union[Email, EmailProfile], lock: threading.Lock
):
    while True:
        if email_service.enabled:
            try:
                imap = email_connection(
                    email_service.imap_server,
                    email_service.username,
                    email_service.password,
                )
            except Exception as ex:
                print(ex)
            else:
                try:
                    data = get_email_data(
                        imap, "INBOX", "UNSEEN", "ALL", save_db_email_message
                    )
                except Exception as ex:
                    print("Ошибка при получении писем", ex)
        time.sleep(email_service.ms_update)


def messenger_update(messenger: Messenger, lock: threading.Lock):
    pass


def run_update():
    threads: List[threading.Thread] = []
    # почты
    # session = Session()
    # email_alias = aliased(Email)
    # email_profile_alias = aliased(EmailProfile)

    # email_services = (
    #     session.query(
    #         email_alias.id.label("email_id"),
    #         email_profile_alias.id.label("email_profile_id"),
    #     )
    #     .join(email_profile_alias, email_alias.id == email_profile_alias.email_id)
    #     .all()
    # )

    query = text(
        "SELECT * FROM email INNER JOIN email_profile ON email.id = email_profile.email_id"
    )

    email_services = session.execute(query).all()

    print("Email сервисы", email_services)

    return

    # for email_service in email_services:
    #     lock = threading.Lock()
    #     t = threading.Thread(target=email_service_update, args=(email_service, lock))
    #     t.start()
    #     threads.append(t)
    # # мессенджеры
    # messengers = Messenger.query.all()
    # for messenger in messengers:
    #     lock = threading.Lock()
    #     t = threading.Thread(target=messenger_update, args=(messenger, lock))
    #     t.start()
    #     threads.append(t)
    # # запуск потоков
    # for thread in threads:
    #     thread.join()


# def resource_path(path: str):
#     return os.path.join(os.path.abspath(os.getcwd()), f"public/{path}")


def add_services():
    # Почты
    yandex_email = Email(
        imap_server="imap.yandex.ru",
        pop_server="pop.yandex.ru",
        smtp_server="smtp.yandex.ru",
        name="Yandex",
        logo="static/favicon-yandex-32x32.png",
    )
    google_email = Email(
        imap_server="imap.gmail.com",
        pop_server="pop.gmail.com",
        smtp_server="smtp.gmail.com",
        name="Gmail",
        logo="static/favicon-gmail-32x32.png",
    )
    mailru_email = Email(
        imap_server="imap.mail.ru",
        pop_server="pop.mail.ru",
        smtp_server="smtp.mail.ru",
        name="Mail.ru",
        logo="static/favicon-mailru-32x32.png",
    )

    # Мессенджеры

    session.add_all([yandex_email, google_email, mailru_email])


def app_run(debug, port):
    app.run(debug=debug, port=port)


def main():
    engine.connect()
    # for model in all_models:
    #     print(model)
    #     if hasattr(model, '__tablename__') and getattr(model, '__abstract__', False):
    #         print(model, 'К удалению')
    #         # model.metadata.drop_all(engine)
    #         metadata.drop_all(engine, tables=[model.__table__])
    Base.metadata.create_all(bind=engine)
    add_services()
    session.flush()
    session.commit()
    print(f"Запуск сокет-сервера на порту {conf['socket']['port']}")
    socketio.run(socket_app, port=conf["socket"]["port"])
    # run_update()

    with app.app_context():
        app.run(port=conf["port"])
        session.close()


def test():
    if "--socket" in sys.argv:
        # запуск сокет-сервера
        print("Запуск сокет-сервера")
        print("Подключение к БД")
        engine.connect()
        print(f"Запуск сокет-сервера на порту {conf['socket']['port']}")
        socketio.run(socket_app, port=conf["socket"]["port"])
        print("Завершение потока")
        print("Закрытие соединения с БД")
        session.close()
    else:
        # запуск сервера с REST API
        print("Запуск сервера с REST API")
        engine.connect()
        print("Пересоздание таблиц и добавление данных")
        Base.metadata.drop_all(bind=engine)
        session.flush()
        Base.metadata.create_all(bind=engine)
        add_services()

        session.commit()
        # Запуск потоков обновления сообщений
        with app.app_context():
            # for model in all_models:
            #     print(model)
            #     if hasattr(model, '__tablename__') and getattr(model, '__abstract__', False):
            #         print(model, 'К удалению')
            #         # model.metadata.drop_all(engine)
            #         metadata.drop_all(engine, tables=[model.__table__])

            # запуск потоков
            # threads = []

            # Запуск дополнительных потоков
            # lock = threading.Lock()
            # t = threading.Thread(target=run_update, args=(lock,))
            # t.start()
            # threads.append(t)

            # запуск Flask-приложения
            # t = threading.Thread(target=app_run, args=(True,conf['port']))
            # socketio.run(app)
            app.run(debug=True, port=conf["port"])
            # t.start()
            # threads.append(t)
            # for t in threads:
            #     t.join()
            # Завершение потока
            print("Завершение потока")
            # закрытие соединения с БД
            print("Закрытие соединения с БД")
            session.close()
