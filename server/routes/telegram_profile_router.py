from get_app import app, session, get_email_connections, create_email_connection
from flask import request, jsonify, g
from sqlalchemy import text, select
from db import TelegramProfile, Session, Messenger, TelegramProfileAuthData
from respect_validation import Validator as v


@app.route("/telegram_profiles", methods=["GET"])
def telegram_profiles():
    is_active = request.args.get("isActive", False, type=bool)

    if not is_active:
        print("Получение всех профилей")

        query = text(
            "SELECT * FROM messenger, telegram_profile INNER JOIN telegram_profile_auth_data ON telegram_profile_auth_data.profile_id = telegram_profile.id WHERE messenger.name = 'Telegram'"
        )

        telegram_profiles = session.execute(query).all()

        print("telegram_profiles", telegram_profiles)

        telegram_profiles_list = [u._asdict() for u in telegram_profiles]
        print("telegram_profiles_list", telegram_profiles_list)
        return jsonify(telegram_profiles_list)
    else:
        print("Получение активированных профилей включенных почт")

        query = text(
            "SELECT * FROM messenger, telegram_profile INNER JOIN telegram_profile_auth_data ON telegram_profile_auth_data.profile_id = telegram_profile.id WHERE is_active = TRUE AND enabled = TRUE AND messenger.name = 'Telegram'"
        )

        telegram_profiles = session.execute(query).all()

        print("telegram_profiles", telegram_profiles)

        telegram_profiles_list = [u._asdict() for u in telegram_profiles]
        print("telegram_profiles_list", telegram_profiles_list)
        return jsonify(telegram_profiles_list)


@app.route("/telegram_profile/<int:id>", methods=["GET"])
def telegram_profile(id: int):
    try:
        query = text(
            "SELECT * FROM messenger, telegram_profile INNER JOIN telegram_profile_auth_data ON telegram_profile_auth_data.profile_id = telegram_profile.id WHERE telegram_profile.id = :id AND messenger.name = 'Telegram'"
        )

        profile = session.execute(query, { 'id': id }).one()._asdict()
    except Exception as ex:
        message = "Ошибка получения данных профиля"
        print(message, ex)
        return jsonify(dict(error=500, message=message))
    else:
        return jsonify(profile)


@app.route("/telegram_profile", methods=["POST"])
def add_telegram_profile():
    data: dict = request.json["params"]

    phone = data['phone']
    session_name = data['session_name']
    api_id = data['api_id']
    api_hash = data['api_hash']

    # print("data", data)
    # if not v.email().validate(data["username"]):
    #     return jsonify(dict(error=500, message="Некорректный Email"))
    # if data["password"] == "":
    #     return jsonify(dict(error=500, message="Некорректный пароль"))

    print("data", data)

    is_active = False

    try:
        new_telegram_profile = TelegramProfile()

        session.add(new_telegram_profile)
        session.flush()

        new_telegram_profile_auth_data = TelegramProfileAuthData(
            phone=phone,
            session_name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            profile_id=new_telegram_profile.id
        )

        session.add(new_telegram_profile_auth_data)
        session.flush()

        stmt = (
            select(TelegramProfileAuthData)
            .join(TelegramProfile.auth_data)
            .where(TelegramProfileAuthData.phone == phone)
        )

        result_profile = session.scalars(stmt).one().as_dict()

        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(dict(error=500, message="Ошибка добавления профиля"))

    # подключение к почтовому сервису

    return jsonify(result_profile)


@app.route("/change_telegram_profile/<int:id>", methods=["POST"])
def change_telegram_profile(id: int):
    data: dict = request.json["params"]
    print("data", data)

    phone = data['phone']
    session_name = data['session_name']
    api_id = data['api_id']
    api_hash = data['api_hash']

    is_active = True if data["isActive"] else False

    try:
        session = Session()

        print("Сессия")

        stmt = (
            select(TelegramProfileAuthData)
            .join(TelegramProfile.auth_data)
            .where(TelegramProfileAuthData.profile_id == id)
        )

        old_profile = session.scalars(stmt).one().as_dict()

        print("Старый профиль", old_profile)
        if old_profile.is_active != is_active:
            print("Флаг активации изменен")
            print("Зануление переключателей всех остальных аккаунтов")
            query = text(f"UPDATE telegram_profile_auth_data SET is_active = FALSE WHERE id != :id")

            session.execute(query, {"id": id})

        print("Обновление информации об аккаунте")

        query = text(
            f"UPDATE telegram_profile_auth_data SET phone = :phone, session_name = :session_name, is_active = :is_active, api_id = :api_id, api_hash = :api_hash WHERE id = :id"
        )

        print("Выполнение запроса UPDATE")

        session.execute(
            query,
            {
                "phone": phone,
                "session_name": session_name,
                "is_active": is_active,
                "api_id": api_id,
                "api_hash": api_hash,
                "id": id,
            },
        )

        print("Запрос на получение измененного профиля")

        query = text(
            "SELECT * FROM messenger, telegram_profile INNER JOIN telegram_profile_auth_data ON telegram_profile_auth_data.profile_id = telegram_profile.id WHERE telegram_profile.id = :id AND messenger.name = 'Telegram'"
        )

        new_profile = session.execute(query, { 'id': id }).one()

        print("new_profile", new_profile)

        # session.flush()
        print("Коммит")
        session.commit()
        print("Закрытие соединения")
        session.close()

    except Exception as ex:
        message = "Ошибка изменения профиля"
        print(message, ex)
        return jsonify(dict(error=500, message=message))

    try:
        if is_active:
            # создание соединения
            create_email_connection(id, new_profile.imap_server, username, password)

    except Exception as ex:
        message = "Ошибка при подключении к Telegram-профилю"
        print(message, ex)
        return jsonify(
            dict(error=500, message=message)
        )
    else:
        return jsonify("OK")