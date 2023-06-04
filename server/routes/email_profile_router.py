from get_app import app, session, get_email_connections, create_email_connection
from flask import request, jsonify, g
from sqlalchemy import text, select
from db import EmailProfile, Session, Email
from respect_validation import Validator as v


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

    is_active = request.args.get("isActive", False, type=bool)

    if not is_active:
        print("Получение всех профилей")

        query = text(
            'SELECT name, enabled, ms_update, email.limit as "limit", logo, imap_server, pop_server, smtp_server, username, password, is_active, email.id AS "email_id", email_profile.id AS "email_profile_id" FROM email INNER JOIN email_profile ON email.id = email_profile.email_id'
        )

        email_profiles = session.execute(query).all()

        print("email_profiles", email_profiles)

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
        print("email_profiles_list", email_profiles_list)
        return jsonify(email_profiles_list)
    else:
        print("Получение активированных профилей включенных почт")

        query = text(
            'SELECT name, enabled, ms_update, email.limit as "limit", logo, imap_server, pop_server, smtp_server, username, password, is_active, email.id AS "email_id", email_profile.id AS "email_profile_id" FROM email INNER JOIN email_profile ON email.id = email_profile.email_id WHERE is_active = TRUE AND enabled = TRUE'
        )

        email_profiles = session.execute(query).all()

        print("email_profiles", email_profiles)

        email_profiles_list = [u._asdict() for u in email_profiles]
        print("email_profiles_list", email_profiles_list)
        return jsonify(email_profiles_list)


@app.route("/email_profile/<int:id>", methods=["GET"])
def email_profile(id: int):

    try:
        query = text(
            'SELECT name, enabled, ms_update, email.limit as "limit", logo, imap_server, pop_server, smtp_server, username, password, is_active, email.id AS "email_id", email_profile.id AS "email_profile_id" FROM email INNER JOIN email_profile ON email.id = email_profile.email_id WHERE email_profile.id = :id'
        )

        profile = session.execute(query, { 'id': id }).one()._asdict()

        # stmt = select(EmailProfile).where(EmailProfile.id == id)
        # profile = session.scalars(stmt).one().as_dict()
    except Exception as ex:
        message = "Ошибка получения данных профиля"
        print(message, ex)
        return jsonify(dict(error=500, message=message))
    else:
        return jsonify(profile)


@app.route("/email_profile", methods=["POST"])
def add_email_profile():
    data: dict = request.json["params"]
    print("data", data)
    if not v.email().validate(data["username"]):
        return jsonify(dict(error=500, message="Некорректный Email"))
    if data["password"] == "":
        return jsonify(dict(error=500, message="Некорректный пароль"))

    print("data", data)

    is_active = False

    try:
        new_email_profile = EmailProfile(
            username=data["username"],
            password=data["password"],
            is_active=is_active,
            email_id=data["email_id"],
        )

        print("Новый профиль", new_email_profile)

        session.add(new_email_profile)
        session.flush()
        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(dict(error=500, message="Ошибка добавления профиля"))

    # подключение к почтовому сервису

    return jsonify(new_email_profile.as_dict())


@app.route("/change_email_profile/<int:id>", methods=["POST"])
def change_email_profile(id: int):
    data: dict = request.json["params"]
    print("data", data)

    username = data["username"]
    password = data["password"]

    if not v.email().validate(username):
        return jsonify(dict(error=500, message="Некорректный Email"))
    if password == "":
        return jsonify(dict(error=500, message="Некорректный пароль"))

    is_active = True if data["isActive"] else False

    try:
        session = Session()

        print("Сессия")

        old_profile = session.query(EmailProfile).where(EmailProfile.id == id).one()

        print("Старый профиль", old_profile)
        if old_profile.is_active != is_active:
            print("Флаг активации изменен")
            print("Зануление переключателей всех остальных аккаунтов")
            query = text(f"UPDATE email_profile SET is_active = FALSE WHERE id != :id")

            session.execute(query, {"id": id})

        print("Обновление информации об аккаунте")

        query = text(
            f"UPDATE email_profile SET username = :username, password = :password, is_active = :is_active WHERE id = :id"
        )

        print("Выполнение запроса UPDATE")

        session.execute(
            query,
            {
                "username": username,
                "password": password,
                "is_active": is_active,
                "id": id,
            },
        )

        print("Запрос на получение измененного профиля")

        query = text(
            'SELECT name, enabled, ms_update, email.limit as "limit", logo, imap_server, pop_server, smtp_server, username, password, is_active, email.id AS "email_id", email_profile.id AS "email_profile_id" FROM email INNER JOIN email_profile ON email.id = email_profile.email_id WHERE email_profile.id = :id'
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
        message = "Ошибка при подключении к Email-профилю"
        print(message, ex)
        return jsonify(
            dict(error=500, message=message)
        )
    else:
        return jsonify("OK")

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
