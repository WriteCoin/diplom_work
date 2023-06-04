from get_app import app, session
from db import Messenger
from flask import jsonify, request
from sqlalchemy import select

@app.route("/messengers", methods=["GET"])
def messengers():
    messengers = session.query(Messenger).all()
    # print('Сервисы')
    # print('dumps', dumps(email_services))
    # print(email_services)
    messengers_list = [u.as_dict() for u in messengers]
    return jsonify(messengers_list)

    # return json.dumps(email_services)


@app.route("/messenger/<int:id>", methods=["POST"])
def update_messenger(id: int):
    data: dict = request.json["params"]

    stmt = select(Messenger).where(Messenger.id == id)
    messenger = session.scalars(stmt).one()

    print(data)

    # enabled = False if data["enabled"] else True
    enabled = data['enabled']
    limit = data['limit']
    ms_update = data['ms_update']

    print(enabled)

    try:
        messenger.enabled = enabled
        messenger.limit = limit
        messenger.ms_update = ms_update

        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(
            dict(error=500, message="Ошибка изменения настроек мессенджера")
        )
    else:
        return jsonify(messenger.as_dict())