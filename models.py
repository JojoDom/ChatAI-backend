from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


def new_uuid() -> str:
    return str(uuid4())


class DateTimeModelMixin(BaseModel):
    createdAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)


class CreateUserRequest(BaseModel):
    userName: str
    email: EmailStr
    phoneNumber: Optional[str] = None
    imageUrl: Optional[str] = None


class User(BaseModel):
    id: int
    userName: str
    email: EmailStr
    phoneNumber: Optional[str]
    imageUrl: Optional[str]


class Converstion(DateTimeModelMixin):
    id: UUID
    title: str
    userId: int
    isFavorite: bool = False


class UserRespone(BaseModel):
    user: User


class UserConversationResponse(BaseModel):
    conversations: List[Converstion]


class ConversationResponse(BaseModel):
    conversation: Converstion


class ChatMessage(BaseModel):
    id: int
    user: User
    text: str
    conversationId: str
    


class ChatMessageResponse(BaseModel):
    chatMessage: ChatMessage


class ConversationChatMessageResponse(BaseModel):
    chatMessages: List[ChatMessage]


class CreateConversationRequest(DateTimeModelMixin):
    id: UUID = Field(default_factory=new_uuid)
    userId: int
    title: str
    isFavorite: bool = False


class UpdateConversationRequest(BaseModel):
    isFavorite: Optional[bool]


class CreateChatRequest(DateTimeModelMixin):
    userId: int
    text: str
    conversationId: str
