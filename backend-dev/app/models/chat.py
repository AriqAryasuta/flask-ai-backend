from peewee import *
from pydantic import BaseModel
from typing import List,Optional

import uuid
import time
import json

from config import DB
# DB.connect()

# Chat DB Schema

class Chat(Model):
    id = CharField(unique=True)
    chat = TextField()
    timestamp = DateField()

    class Meta:
        database = DB

class ChatModel(BaseModel):
    id : str
    chat : str
    timestamp : int

# Form for Chat

class ChatForm(BaseModel):
    chat: dict

class ChatResponse(BaseModel):
    id: str
    chat: dict
    timestamp: int

class ChatTable:
    def __init__(self, db):
        self.db = db
        db.create_tables([Chat])
    
    def new_chat(self, form_data: ChatForm) -> Optional[ChatModel]:
        id = str(uuid.uuid4())
        chat = ChatModel(**{
            "id": id,
            "chat": json.dumps(form_data.chat),
            "timestamp": int(time.time())
        })
        result = Chat.create(**chat.model_dump())
        return chat if result else None
    
    
        
Chats = ChatTable(DB)
