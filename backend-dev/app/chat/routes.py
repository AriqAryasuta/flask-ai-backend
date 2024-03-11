from flask import render_template
from app.chat import bp

import json

from app.models.chat import(
    Chat,
    ChatModel,
    ChatResponse,
    ChatForm,
    Chats
)

@bp.route('/')
def index():
    return 'this is chat blueprint'

@bp.route('/newchat', methods=['POST'])
async def post_new_chat(form_data: ChatForm):
    try:
        chat = Chats.new_chat(form_data)
        return ChatResponse(**{**chat.model_dump(), "chat": json.loads(chat.chat)})
    except Exception as e:
        return print(e)
