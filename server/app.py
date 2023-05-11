from flask import Flask
from WebAutomation.general_utils import *
from flask_sqlalchemy import SQLAlchemy
import json

with open('conf.json', 'r', encoding='utf-8') as fd:
    conf = json.load(fd)
    database = conf['database']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database['user']}:{database['password']}@{database['host']}/{database['dbname']}"

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Hello, World!"

if '-t' in sys.argv and __name__ == '__main__':
    # Тестовый режим запуска
    db.create_all()
    app.run()
elif __name__ == '__main__':
    # Релизный режим запуска
    app.run()