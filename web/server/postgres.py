import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, Column, Integer, String, \
    BigInteger, Numeric

Base = declarative_base()


class LocationData(Base):
    """Wrapper for location_data table

    location_data holds all of the necessary data collected by the cameras
    deployed on the field. The data points are updated periodically to reflect
    the current state of the various areas and is used to render the heatmap
    in the website.

    Attributes:
        lat = (column) Decimal value corresponding to latitiude
        lng = (column) Decimal value corresponding to longitude
        weight = (column) Population density at the corresponding area
    """

    __tablename__ = "location_data"

    lat = Column(Numeric, primary_key=True)
    lng = Column(Numeric, primary_key=True)
    weight = Column(Numeric)


def all_tables():
    return ["location_data"]


def get_user_config():
    """Returns a dictionary containing config options loaded from
    ./conf.json"""

    config = {}
    with open('./web/server/conf.default.json', 'r') as f:
        config = json.loads(f.read())
    return config


def has_tables(tables, engine):
    """Returns a True/False based on if tables have been created in engine"""

    exists = True
    for table in tables:
        exists = exists and engine.dialect.has_table(engine, table)
    return exists


def get_engine():
    """Returns sqlalchemy engine to connect to db"""

    login = get_user_config()["db"]
    engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' %
                           (login["user"], login["password"],
                            login["host"], login["port"],
                            login["database"]))
    return engine


def create_tables():
    engine = get_engine()
    if not has_tables(all_tables(), engine):
        print("Creating tables...")
        Base.metadata.create_all(engine)
    else:
        print("Tables are already created")


def get_session():
    """Returns a new session to database specified in ./conf.json

    get_session() will create the necessary tables if they do not exists in the
    specified database. A new engine is created for each session
    """
    engine = get_engine()
    Session = sessionmaker(engine)
    session = Session()
    return session


if __name__ == "__main__":
    create_tables()
