from imaplib import IMAP4_SSL
from flask import Flask, Response, jsonify, url_for, request, g
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from get_conf import conf
from db import Session
from WebAutomation.diplom_work.services.mail import connection

# приложение по REST API
app = Flask(__name__)

origins = "*"
# чтобы работали запросы от клиента
CORS(app, resources={r"/*": {"origins": origins}})
# CORS(app, resources={r"/*": {"origins": origins}, r"/email_messages/*": {"origins": "*"}, r"/email_services/*": {"origins": "*"}})

# приложение по socket
socket_app = Flask(__name__) 
socket_app = Flask(__name__)
socket_app.config["SECRET_KEY"] = conf["socket"]["secret"]
# CORS(socket_app, resources={r"/*": {"origins": origins}})
socketio = SocketIO(socket_app)
# socketio.init_app(socket_app)

# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database['user']}:{database['password']}@{database['host']}/{database['dbname']}"
# db = SQLAlchemy(app)

# # настройка, чтобы запросы работали
# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
#     return response

# настройка, чтобы запросы работали
@app.before_request
def handle_preflight():
	if request.method == "OPTIONS":
		res = Response()
		res.headers['X-Content-Type-Options'] = '*'
		return res

# сессия базы данных
session = Session()

def get_email_connections():
	return {} if not hasattr(g, 'email_connections') else g.email_connections

def create_email_connection(
    id: int, imap_server: str, username: str, password: str
) -> IMAP4_SSL:
    # создание соединения
    g.email_connections = get_email_connections()

    conn = connection(imap_server, username, password)

    g.email_connections[id] = {"connection": conn}

    return conn