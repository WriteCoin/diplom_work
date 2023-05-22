from get_app import app, session
from db import Email
from flask import jsonify, request
from sqlalchemy import select

@app.route("/email_services", methods=["GET"])
def email_services():
    email_services = session.query(Email).all()
    # print('Сервисы')
    # print('dumps', dumps(email_services))
    # print(email_services)
    email_services_list = [u.as_dict() for u in email_services]
    return jsonify(email_services_list)

    # return json.dumps(email_services)


@app.route("/email_service/<int:id>", methods=["POST"])
def update_email_service(id: int):
    data: dict = request.json["params"]

    stmt = select(Email).where(Email.id == id)
    email = session.scalars(stmt).one()

    print(data)

    enabled = False if data["enabled"] else True

    print(enabled)

    try:
        email.enabled = enabled

        session.commit()
    except Exception as ex:
        print(ex)
        return jsonify(
            dict(error=500, message="Ошибка изменения настроек почтового агрегатора")
        )
    else:
        return jsonify(email.as_dict())