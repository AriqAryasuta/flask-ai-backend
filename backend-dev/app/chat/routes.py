from flask import render_template, request, jsonify
from app.chat import bp

import json

from app.controller.rag import(
    vertexModelAndEmbeddings
)

from app.models.chat import(
    Chat,
    ChatModel,
    ChatResponse,
    ChatForm,
    Chats
)



@bp.route('/')
def index():
    model = vertexModelAndEmbeddings()

@bp.route('/newchat', methods=['POST'])
async def new_chat(user_input):

