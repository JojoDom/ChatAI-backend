import datetime
from uuid import UUID

from fastapi import FastAPI, Body, status, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from database import get_db


from schema import User, Conversations, Chats

from models import (
    ConversationChatMessageResponse,
    CreateChatRequest,
    UserRespone,
    UserConversationResponse,
    ConversationResponse,
    ChatMessageResponse,
    CreateUserRequest,
    CreateConversationRequest,
    UpdateConversationRequest,
)

app = FastAPI(
    title="Chat App",
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.post(
    "/users/",
    tags=["users"],
    response_model=UserRespone,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: CreateUserRequest = Body(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()

    if user is None:
        user = User(
            **request.model_dump(),
            createdAt=datetime.datetime.now(),
            updatedAt=datetime.datetime.now(),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    return {"user": user}


@app.get(
    "/users/{user_id}",
    tags=["users"],
    response_model=UserRespone,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return {"user": user}


@app.get(
    "/users/{user_id}/converstions",
    tags=["users"],
    response_model=UserConversationResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_conversations(
    user_id: int, db: Session = Depends(get_db)
) -> UserConversationResponse:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user_conversations = (
        db.query(Conversations)
        .filter(Conversations.userId == user_id)
        .order_by(Conversations.createdAt.desc())
        .all()
    )

    return {"conversations": user_conversations}


@app.post(
    "/conversations",
    tags=["conversations"],
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    request: CreateConversationRequest = Body(...), db: Session = Depends(get_db)
) -> ConversationResponse:
    user = db.query(User).filter(User.id == request.userId).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    conversation = Conversations(**request.model_dump())
    chat = Chats(
        conversationId=conversation.id,
        text=conversation.title,
        userId=conversation.userId,
    )

    db.add(conversation)
    db.add(chat)
    db.commit()
    db.refresh(conversation)

    return {"conversation": conversation}


# @app.get(
#     "/conversations/{conversation_id}",
#     tags=["conversations"],
#     response_model=ConversationResponse,
#     status_code=status.HTTP_200_OK,
# )
# async def get_conversation(
#     conversation_id: str, db: Session = Depends(get_db)
# ) -> ConversationResponse:
#     db.query(User).filter(User.id == 1).update({"userName": "Chat AI"})
#     db.commit()


@app.put(
    "/conversations/{conversation_id}",
    tags=["conversations"],
    status_code=status.HTTP_200_OK,
)
async def update_conversation(
    conversation_id: str,
    request: UpdateConversationRequest = Body(...),
    db: Session = Depends(get_db),
):
    db.query(Conversations).filter(Conversations.id == conversation_id).update(
        {"isFavorite": request.isFavorite, "updatedAt": datetime.datetime.now()}
    )
    db.commit()

    return {"message": "Conversation updated."}


@app.delete(
    "/conversations/{conversation_id}",
    tags=["conversations"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    deleted = (
        db.query(Conversations)
        .filter(Conversations.id == str(conversation_id))
        .delete()
    )
    db.commit()


@app.get(
    "/conversations/{conversation_id}/chat-messages",
    tags=["conversations"],
    response_model=ConversationChatMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_chat_messages(conversation_id: UUID, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversations).filter(Conversations.id == str(conversation_id)).first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user = db.query(User).filter(User.id == conversation.userId).first()
    bot = db.query(User).filter(User.id == 1).first()
    chats = db.query(Chats).filter(Chats.conversationId == conversation.id).all()

    response = [
        {
            "user": {
                "id": user.id,
                "userName": user.userName,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "imageUrl": user.imageUrl,
            },
            "text": chat.text,
            "conversationId": chat.conversationId,
        }
        if chat.userId != 1
        else {
            "user": {
                "id": bot.id,
                "userName": bot.userName,
                "email": bot.email,
                "phoneNumber": bot.phoneNumber,
                "imageUrl": bot.imageUrl,
            },
            "text": chat.text,
            "conversationId": chat.conversationId,
        }
        for chat in chats
    ]

    return {"chatMessages": response}


@app.post(
    "/conversations/{conversation_id}/chat-messages",
    tags=["conversations"],
    response_model=ConversationChatMessageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_chat_messages(conversation_id: UUID, db: Session = Depends(get_db)):
    conversation = (
        db.query(Conversations).filter(Conversations.id == str(conversation_id)).first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user = db.query(User).filter(User.id == conversation.userId).first()
    bot = db.query(User).filter(User.id == 1).first()
    chats = db.query(Chats).filter(Chats.conversationId == conversation.id).all()

    response = [
        {
            "user": {
                "id": user.id,
                "userName": user.userName,
                "email": user.email,
                "phoneNumber": user.phoneNumber,
                "imageUrl": user.imageUrl,
            },
            "text": chat.text,
            "conversationId": chat.conversationId,
        }
        if chat.id != 1
        else {
            "user": {
                "id": bot.id,
                "userName": bot.userName,
                "email": bot.email,
                "phoneNumber": bot.phoneNumber,
                "imageUrl": bot.imageUrl,
            },
            "text": chat.text,
            "conversationId": chat.conversationId,
        }
        for chat in chats
    ]

    return {"chatMessages": response}


@app.post(
    "/chat-messages/",
    tags=["chats"],
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_message(
    request: CreateChatRequest, db: Session = Depends(get_db)
) -> ChatMessageResponse:
    user = db.query(User).filter(User.id == request.userId).first()

    conversation = (
        db.query(Conversations)
        .filter(Conversations.id == request.conversationId)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found. Please start a new conversation.",
        )

    chat = Chats(**request.model_dump())

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {
        "chatMessage": {
            "id": chat.id,
            "conversationId": request.conversationId,
            "user": user,
            "text": request.text,
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9001)
