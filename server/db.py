from enum import IntEnum
from get_conf import conf
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    MetaData,
    DateTime,
)
from datetime import datetime
from uuid import UUID
import json
from sqlalchemy.ext.declarative import (
    declarative_base,
    as_declarative,
    declared_attr,
    DeclarativeMeta,
)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship, sessionmaker, registry
from pprint import pprint
from WebAutomation.general_utils import *

database = conf["database"]

DATABASE_URI = f"postgresql+psycopg2://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['dbname']}"

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def as_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {
            column.key: getattr(self, attr)
            for attr, column in self.__mapper__.c.items()
        }
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [
                        i.to_dict(backref=self.__table__) for i in value
                    ]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)


class BaseModel(OutputMixin, Base):
    __tablename__ = "base_model"
    __abstract__ = True

    id = Column(
        Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Service(BaseModel):
    __tablename__ = "service"
    __abstract__ = True

    name = Column(String(50), nullable=False, unique=True)
    enabled = Column(Boolean, nullable=False, default=True)
    limit = Column(Integer, nullable=False, default=100)
    ms_update = Column(Float, nullable=False, default=5000)
    logo = Column(String, nullable=False)


class Email(Service):
    __tablename__ = "email"

    imap_server = Column(String(50))
    pop_server = Column(String(50))
    smtp_server = Column(String(50))


class EmailProfile(BaseModel):
    __tablename__ = "email_profile"

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    email_id = Column(Integer, ForeignKey("email.id"))
    email_message = relationship("EmailMessage", back_populates="profile")


class EmailMessage(BaseModel):
    __tablename__ = "email_message"

    email = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=False, default="Без темы")
    text = Column(String, nullable=False)
    attachments_count = Column(Integer, nullable=False, default=0)
    is_read = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)

    to_id = Column(Integer, ForeignKey("email_profile.id"))
    profile = relationship("EmailProfile", back_populates="email_message")

class TestEmail(Service):
    __tablename__ = "test_email"

    imap_server = Column(String(50))
    pop_server = Column(String(50))
    smtp_server = Column(String(50))

class TestEmailProfile(BaseModel):
    __tablename__ = "test_email_profile"

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    email_id = Column(Integer, ForeignKey("test_email.id"))
    email_message = relationship("TestEmailMessage", back_populates="profile")

class TestEmailMessage(BaseModel):
    __tablename__ = "test_email_message"

    email = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String, nullable=False, default="Без темы")
    text = Column(String, nullable=False)
    attachments_count = Column(Integer, nullable=False, default=0)
    is_read = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)

    to_id = Column(Integer, ForeignKey("test_email_profile.id"))
    profile = relationship("TestEmailProfile", back_populates="email_message")

class Messenger(Service):
    __tablename__ = "messenger"

class Telegram(Service):
    __tablename__ = "telegram"

class TelegramProfile(BaseModel):
    __tablename__ = "telegram_profile"

    first_name = Column(String, default="")
    last_name = Column(String, default="")

    message = relationship("TelegramMessage", back_populates="profile")
    auth_data = relationship("TelegramProfileAuthData", back_populates="profile")


class TelegramProfileAuthData(BaseModel):
    __tablename__ = "telegram_profile_auth_data"

    phone = Column(String(50), nullable=False, unique=True)
    session_name = Column(String, nullable=False)
    api_id = Column(Integer, nullable=False)
    api_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    profile_id = Column(Integer, ForeignKey('telegram_profile.id'))
    profile = relationship("TelegramProfile", back_populates="auth_data")

class TelegramMessage(BaseModel):
    __tablename__ = "telegram_message"

    mentioned = Column(Boolean, nullable=False, default=False)
    silent = Column(Boolean, nullable=False, default=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)

    # sender_id = Column(Integer, ForeignKey('telegram_profile.id'))
    sender = Column(String, nullable=False)

    to_id = Column(Integer, ForeignKey('telegram_profile.id'))
    profile = relationship("TelegramProfile", back_populates="message")


metadata.reflect(bind=engine)


def get_subclasses(cls):
    subclasses = set(cls.__subclasses__())
    for subclass in subclasses.copy():
        subclasses |= set(get_subclasses(subclass))
    return subclasses

def drop_tables(table_names):
    session = Session()
    for table_name in table_names:
        try:
            Base.metadata.tables[table_name].drop(engine)
        except Exception as ex:
            print(f"Error dropping table {table_name}: {str(ex)}")
    session.commit()

def table_is_empty(table):
    session = Session()
    result = session.query(exists().where(table.id != None)).scalar() is None
    session.close()
    return result

# services = get_subclasses(Service)
# other_models = set(
#     filter(
#         lambda model: not issubclass(model, Service), list(get_subclasses(BaseModel))
#     )
# )
# all_models = get_subclasses(Base)

# for service in services:
#     service.__abstract__ = None

# for model in other_models:
#     model.__abstract__ = None

# for model in all_models:
#     if hasattr(model, "__tablename__") and getattr(model, "__abstract__", False):
#         model.metadata.drop_all(engine)
        # metadata.drop_all(engine, tables=[model.__table__])

# print('Удаление таблиц')
# abstract_table_names = []
# for table_name in metadata.tables.keys():
#     print(table_name)
#     table = metadata.tables[table_name]
#     # pprint(dir(table))
#     # pprint(dir(table._all_columns))
#     try:
#         print(getattr(table, 'info', {}).get('abstract', False))
#     except:
#         print('не абстрактный')
#     if getattr(table, '__abstract__', False):
#         abstract_table_names.append(table_name)

# metadata.drop_all(engine, checkfirst=False, tables=abstract_table_names)


# mapped_classes = mapper_registry.mapped_classes
# print(mapped_classes)
# for mapper in mapper_registry.mappers:
#     model = mapper.class_
#     print('Таблица', model.__tablename__)
#     if getattr(model, "__abstract__", False) is True:
#         # удалите таблицу по имени
#         print(f"Таблица {model.__tablename__} должна быть удалена")
#         metadata.tables[model.__tablename__].drop(engine)
