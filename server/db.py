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
from sqlalchemy.orm import sessionmaker, registry
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
    ms_update = Column(Float, nullable=False, default=0.250)
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


class EmailMessage(BaseModel):
    __tablename__ = "email_message"

    email = Column(String(50), nullable=False)
    sender = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False, default="Без темы")
    text = Column(String, nullable=False)
    attachments_count = Column(Integer, nullable=False, default=0)
    is_read = Column(Boolean, nullable=False, default=False)
    date = Column(DateTime, nullable=False)

    to_id = Column(Integer, ForeignKey("email_profile.id"))


class Messenger(Service):
    __tablename__ = "messenger"


metadata.reflect(bind=engine)


def get_subclasses(cls):
    subclasses = set(cls.__subclasses__())
    for subclass in subclasses.copy():
        subclasses |= set(get_subclasses(subclass))
    return subclasses


services = get_subclasses(Service)
other_models = set(
    filter(
        lambda model: not issubclass(model, Service), list(get_subclasses(BaseModel))
    )
)
all_models = get_subclasses(Base)

for service in services:
    service.__abstract__ = None

for model in other_models:
    model.__abstract__ = None

for model in all_models:
    if hasattr(model, "__tablename__") and getattr(model, "__abstract__", False):
        model.metadata.drop_all(engine)
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
