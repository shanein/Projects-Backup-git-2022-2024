from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from sqlalchemy.orm import registry

username = os.getenv("POSTGRES_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")
hostname = os.getenv("POSTGRES_DB")
port = os.getenv("POSTGRES_PORT")
isDev = os.getenv("IS_DEV")
if isDev == "true":
    db = "@db-dev:"
else:
    db = "@db:"
engine = create_engine(
    "postgresql://postgres:" + str(password) + db + str(port) + "/" + str(hostname)
)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
mapper_registry = registry()
Base = mapper_registry.generate_base()
db = Session()


def get_db():
    try:
        yield db
    finally:
        db.close()
