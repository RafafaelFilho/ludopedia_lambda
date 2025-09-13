from api.settings   import settings
from sqlmodel       import create_engine, Session

database_url=f'mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}'
engine=create_engine(database_url)
#engine=create_engine(settings.DATABASE_URL)

def getSession():
    with Session(engine) as session:
        yield session
