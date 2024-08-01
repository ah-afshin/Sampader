from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()
db_uri = "sqlite:///database/data.db"
engine = create_engine(db_uri)


Session = sessionmaker(bind=engine)
session = Session()

def generate_uuid():
    return str(uuid.uuid4())

print("db constants configs were set")
uploads_path = "F://Sampader/uploads"


# lists of valid values
school_and_class = ["101", "102", "103", "104", "201", "202", "203", "204", "301", "302", "303", "304",]
verified = [
    0, # not verified
    1, # general verifiction
    2, # verified as admin
    3, # verified as teacher
]
