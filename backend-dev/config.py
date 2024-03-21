import chromadb
import json
from peewee import *
from chromadb import Settings

CHROMA_DATA_PATH = "C:/Users/your_user_name/Chroma/ChromaData/"

CHROMA_CLIENT = chromadb.PersistentClient(
    path=CHROMA_DATA_PATH,
    settings=Settings(allow_reset=True, anonymized_telemetry=False)
)

FILE_PATH = "data_clean.json"

CREDENTIAL_PATH = "vertex.json"


DB = SqliteDatabase('chat.db')
DB.connect()



