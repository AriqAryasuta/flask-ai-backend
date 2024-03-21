from flask import Blueprint

bp  = Blueprint('RAG', __name__)

from app.chat import routes