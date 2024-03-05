from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer

metadata = MetaData()


test_model = Table(
    'test_model',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True)
)

