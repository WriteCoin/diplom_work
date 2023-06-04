from get_app import app, session
from db import Messenger
from flask import jsonify, request, redirect
from sqlalchemy import select

@app.route("/auth/discord/login", methods=["GET"])
def discord_login():
    url = "https://discord.com/api/oauth2/authorize?client_id=1113611056967864320&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauth%2Fdiscord%2Fcallback&response_type=code&scope=identify%20messages.read"

    redirect(url)

    # messengers = session.query(Messenger).all()
    # # print('Сервисы')
    # # print('dumps', dumps(email_services))
    # # print(email_services)
    # messengers_list = [u.as_dict() for u in messengers]
    # return jsonify(messengers_list)

    # return json.dumps(email_services)