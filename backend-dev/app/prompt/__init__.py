from flask import Blueprint

bp  = Blueprint('prompt', __name__)

from app.prompt import routes