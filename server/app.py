import time
import threading
from typing_extensions import runtime
from respect_validation import Validator as v
from flask import Flask, jsonify, url_for, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
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
    as_dict
)
from WebAutomation.diplom_work.services.mail import (
    MailMessage,
    connection as email_connection,
    get_email_data,
)
from pprint import pprint

# приложение по REST API
app = Flask(__name__)

origins = '*'
# чтобы работали запросы от клиента
CORS(app, resources={r"/*": {"origins": origins}})

# приложение по socket
socket_app = Flask(__name__)
socket_app.config['SECRET_KEY'] = conf['socket']['secret']
CORS(socket_app, resources={r"/*": {"origins": origins}})
socketio = SocketIO(socket_app)
# socketio.init_app(socket_app)

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database['user']}:{database['password']}@{database['host']}/{database['dbname']}"
# db = SQLAlchemy(app)

# сессия базы данных
session = Session()


@app.route("/email_services", methods=["GET"])
def email_services():
    email_services = session.query(Email).all()
    # print('Сервисы')
    # print('dumps', dumps(email_services))
    # print(email_services)
    email_services_list = [u.as_dict() for u in email_services]
    return jsonify(email_services_list)
    # return json.dumps(email_services)

@app.route('/email_service/<int:id>', methods=["POST"])
def update_email_service(id: int):
    data: dict = request.json['params']

    stmt = select(Email).where(Email.id == id)
    email = session.scalars(stmt).one()

    print(data)

    enabled = False if data['enabled'] else True

    print(enabled)

    try:
        email.enabled = enabled

        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(dict(error=500, message="Ошибка изменения настроек почтового агрегатора"))
    else:
        return jsonify(email.as_dict())

@app.route("/email_profiles", methods=["GET"])
def email_profiles():
    # email_profiles = session.query(EmailProfile).all()
    # email_alias = aliased(Email)
    # email_profile_alias = aliased(EmailProfile)

    # email_profiles = (
    #     session.query(
    #         email_alias,
    #         email_profile_alias,
    #         email_alias.id.label("email_id"),
    #         email_profile_alias.id.label("email_profile_id"),
    #     )
    #     .join(email_profile_alias, email_alias.id == email_profile_alias.email_id)
    #     .all()
    # )

    # stmt = (
    #     select(email_profile_alias, email_profile_alias.id.label("email_profile_id"), email_alias.id.label("email_id"))
    #     .join(email_alias, email_alias.id == email_profile_alias.email_id)
    # )

    # email_profiles = session.scalars(stmt).all()

    query = text("SELECT name, enabled, ms_update, logo, imap_server, pop_server, smtp_server, username, password, is_active, email.id AS \"email_id\", email_profile.id AS \"email_profile_id\" FROM email INNER JOIN email_profile ON email.id = email_profile.email_id")

    email_profiles = session.execute(query).all()

    print('email_profiles', email_profiles)

    # for email_profile in email_profiles:
    #     pprint(dir(email_profile))
    #     print('count', email_profile.count)
    #     print('index', email_profile.index)
    #     print('t', email_profile.t)
    #     print('tuple', email_profile.tuple)
    #     print('data', email_profile._data)
    #     print('fields', email_profile._fields)
    #     print('filter_on_values', email_profile._filter_on_values)
    #     print(email_profile._asdict())
    #     for key, value in email_profile._asdict().items():
    #         print(key, value)


    # email_profiles_list = [dict(name=u.name, enabled=u.enabled, ms_update=u.ms_update, logo=u.logo, imap_server=u.imap_server, pop_server=u.pop_server, smtp_server=u.smtp_server, email_id=u.email_id, email_profile_id=u.email_profile_id, username=u.username, password=u.password) for u in email_profiles]

    email_profiles_list = [u._asdict() for u in email_profiles]
    print('email_profiles_list', email_profiles_list)
    return jsonify(email_profiles_list)

@app.route("/email_profile/<int:id>", methods=["GET"])
def email_profile(id: int):
    stmt = select(EmailProfile).where(EmailProfile.id == id)
    profile = session.scalars(stmt).one().as_dict()
    return jsonify(profile)

@app.route('/email_profile', methods=["POST"])
def add_email_profile():
    data: dict = request.json['params']
    print('data', data)
    if not v.email().validate(data['username']):
        return jsonify(dict(error=500, message="Некорректный Email"))
    if data['password'] == "":
        return jsonify(dict(error=500, message="Некорректный пароль"))

    print(data)

    try:

        new_email_profile = EmailProfile(username=data['username'], password=data['password'], is_active=True, email_id=data['email_id'])

        print("Новый профиль", new_email_profile)

        session.add(new_email_profile)
        session.flush()
        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(dict(error=500, message="Ошибка добавления профиля"))
    else:
        return jsonify(new_email_profile.as_dict())

@app.route('/change_email_profile/<int:id>', methods=["POST"])
def change_email_profile(id: int):
    data: dict = request.json['params']
    print('data', data)
    if not v.email().validate(data['username']):
        return jsonify(dict(error=500, message="Некорректный Email"))
    if data['password'] == "":
        return jsonify(dict(error=500, message="Некорректный пароль"))

    is_active = True if data['isActive'] else False

    try:
        session = Session()

        print('Сессия')

        query = text(f'UPDATE email_profile SET username = :username, password = :password, is_active = :is_active WHERE id = :id')
        # query = query.bindparams(x=data['username'], y=data['password'], z=id)

        print('Выполнение запроса')

        session.execute(query, {'username': data['username'], 'password': data['password'], 'is_active': is_active, 'id': id})
        # session.flush()
        print('Коммит')
        session.commit()
        print('Закрытие соединения')
        session.close()
    except Exception as ex:
        print(ex)
        return jsonify(dict(error=500, message="Ошибка изменения профиля"))
    else:
        return jsonify('OK')


    # stmt = select(EmailProfile).where(EmailProfile.id == id)
    # profile = session.scalars(stmt).one()

    # profile = session.execute(query).one()._asdict()

    # print('old_profile', profile)

    # try:
    #     profile.username = data['username']
    #     profile.password = data['password']

    #     print('new_profile', profile)

    #     session.flush()
    #     session.commit()
    # except Exception as ex:
    #     print(ex)
    #     return jsonify(dict(error=500, message="Ошибка изменения профиля"))
    # else:
    #     return jsonify(profile.as_dict())

# Обработчик подключения клиента к серверу
@socketio.on('connect')
def connect_handler():
   print('Client connected')

# Обработчик отключения клиента от сервера
@socketio.on('disconnect')
def disconnect_handler():
   print('Client disconnected')

def save_db_email_message(
    email_service: Union[Email, EmailProfile],
    message: MailMessage,
    lock: Optional[threading.Lock],
):
    try:
        email_message = EmailMessage(
            email=message["msg_email"],
            sender=message["msg_from"],
            subject=message["msg_subj"],
            text=message["text"],
            attachments_count=message["attachments_count"],
            date=message["date"],
            to_id=email_service,
        )

        if not lock is None:
            lock.acquire()

        session.add(email_message)
        session.flush()
        session.commit()

        if not lock is None:
            lock.release()
    except Exception as ex:
        raise Exception("Ошибка добавления сообщения в БД", ex)


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
    pass
    # threads: List[threading.Thread] = []
    # # почты
    # # session = Session()
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

    # print("Email сервисы", email_services)


    # return

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
        logo="static/favicon-yandex-32x32.png"
    )
    google_email = Email(
        imap_server="imap.gmail.com",
        pop_server="pop.gmail.com",
        smtp_server="smtp.gmail.com",
        name="Gmail",
        logo="static/favicon-gmail-32x32.png"
    )
    mailru_email = Email(
        imap_server="imap.mail.ru",
        pop_server="pop.mail.ru",
        smtp_server="smtp.mail.ru",
        name="Mail.ru",
        logo="static/favicon-mailru-32x32.png"
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
    socketio.run(socket_app, port=conf['socket']['port'])
    # run_update()
    
    with app.app_context():
        
        app.run(port=conf['port'])
        session.close()


def test():
    if '--socket' in sys.argv:
        # запуск сокет-сервера
        print("Запуск сокет-сервера")
        print("Подключение к БД")
        engine.connect()
        print(f"Запуск сокет-сервера на порту {conf['socket']['port']}")
        socketio.run(socket_app, port=conf['socket']['port'])
        print("Завершение потока")
        print('Закрытие соединения с БД')
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
            app.run(debug=True, port=conf['port'])
            # t.start()
            # threads.append(t)
            # for t in threads:
            #     t.join()
            # Завершение потока
            print('Завершение потока')
            # закрытие соединения с БД
            print('Закрытие соединения с БД')
            session.close()  