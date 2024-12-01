from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey

from data.db_connect import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(BigInteger, nullable=False)
    username = Column(String(length=255), nullable=False)
