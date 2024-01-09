from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    email = Column(String)
    phoneNumber = Column(String, nullable=True)
    imageUrl = Column(String)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)


class Conversations(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    title = Column(Text)
    isFavorite = Column(Boolean)
    userId = Column(Integer, ForeignKey("users.id"))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)


class Chats(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    conversationId = Column(String, ForeignKey("conversations.id"))
    userId = Column(Integer, ForeignKey("users.id"))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)


Base.metadata.create_all(engine)
