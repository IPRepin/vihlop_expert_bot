from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Text, Boolean

from data.db_connect import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(length=255), nullable=False)
    user_email = Column(String(length=50), nullable=True)
    user_url = Column(String(length=255), nullable=True)


class Application(BaseModel):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(length=255), nullable=False)
    phone = Column(String(length=50), nullable=False)
    viewed = Column(Boolean, nullable=False, default=False)


class Admin(BaseModel):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(length=255), nullable=False)


class Stock(BaseModel):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=50), nullable=False)
    image = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Text, nullable=True)


class Service(BaseModel):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=50), nullable=False)
    image = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))


class Category(BaseModel):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=50), nullable=False)
