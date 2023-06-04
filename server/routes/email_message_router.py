from functools import partial
from get_app import app, get_email_connections
from db import Session, EmailMessage, Email, EmailProfile
from flask import jsonify, request, make_response, g
from sqlalchemy import text
from WebAutomation.general_utils import *
from WebAutomation.diplom_work.services.mail import (
    connection,
    get_email_data,
    MailMessage,
)
from routes.email_profile_router import create_email_connection
from pprint import pprint


def save_db_email_message(message: MailMessage, email_profile_id: int):
    try:
        session = Session()

        print("Сессия сохранения нового сообщения")

        pprint("Новое сообщение", message)

        print("Сохранение в БД")

        email_message = EmailMessage(
            email=message["msg_email"],
            sender=message["msg_from"],
            subject=message["msg_subj"],
            text=message["text"],
            attachments_count=message["attachments_count"],
            date=message["date"],
            to_id=email_profile_id,
        )

        session.add(email_message)
        session.flush()
        session.commit()
    except Exception as ex:
        raise Exception("Ошибка добавления сообщения в БД", ex)


@app.route("/email_messages", methods=["GET"])
def email_messages():
    email_id = request.args.get("profile[email_id]")
    email_profile_id = request.args.get("profile[email_profile_id]")
    enabled = request.args.get("profile[enabled]")
    imap_server = request.args.get("profile[imap_server]")
    is_active = request.args.get("profile[is_active]")
    logo = request.args.get("profile[logo]")
    limit = request.args.get("profile[limit]")
    ms_update = request.args.get("profile[ms_update]")
    name = request.args.get("profile[name]")
    password = request.args.get("profile[password]")
    pop_server = request.args.get("profile[pop_server]")
    smtp_server = request.args.get("profile[smtp_server]")
    username = request.args.get("profile[username]")

    
    try:
        connections = get_email_connections()

        if (
            not str(email_profile_id) in connections
            or "error" in connections[str(email_profile_id)]
        ):
            conn = create_email_connection(
                email_profile_id, imap_server, username, password
            )
        else:
            conn = connections[email_profile_id]["connection"]

    except Exception as ex:
        message = "Ошибка при подключении к Email-профилю"
        print(message, ex)
        print(traceback.format_exc())
        return jsonify(
            dict(error=500, message=message)
        )

    try:
        data = get_email_data(
            conn,
            "INBOX",
            "UNSEEN",
            "ALL",
            partial(save_db_email_message, email_profile_id=int(email_profile_id)),
        )
    except Exception as ex:
        message = "Ошибка при получении писем"
        print(message, ex)
        print(traceback.format_exc())
        return jsonify(dict(error=500, message=message))

    try:

        session = Session()

        print("Сессия получения сообщений")

        query = text(
            "SELECT * FROM email_message INNER JOIN email_profile ON email_message.to_id = email_profile.id INNER JOIN email ON email.id = email_profile.email_id WHERE to_id = :profile_id"
        )

        all_email_messages = session.execute(query, {"profile_id": email_profile_id}).all()

        query = text(
            "SELECT * FROM email_message INNER JOIN email_profile ON email_message.to_id = email_profile.id INNER JOIN email ON email.id = email_profile.email_id WHERE to_id = :profile_id AND is_read = FALSE"
        )

        new_email_messages = session.execute(query, {"profile_id": email_profile_id}).all()

        session.close()

        all_email_messages_list = [u.as_dict() for u in all_email_messages]
        new_email_messages_list = [u.as_dict() for u in new_email_messages]

        email_messages = {
            "all_email_messages": all_email_messages_list,
            "new_email_messages": new_email_messages_list,
        }
    except Exception as ex:
        message = "Ошибка при получении писем из базы данных"
        print(message, ex)
        print(traceback.format_exc())
        return jsonify(dict(error=500, message=message))
    else:
        response = jsonify(email_messages)
        return response
