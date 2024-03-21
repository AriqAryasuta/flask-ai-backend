
from langchain.schema import HumanMessage, SystemMessage
from langchain.llms.vertexai import VertexAI
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chat_models.vertexai import ChatVertexAI
from langchain.chains import RetrievalQA
from google.cloud import aiplatform
from typing import List
from pydantic import BaseModel
import chromadb

import time
import langchain
import os
import vertexai

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../../vertex.json"

def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)

class CustomVertexAIEmbeddings(VertexAIEmbeddings, BaseModel):
    requests_per_minute: int
    num_instances_per_batch: int

    # Overriding embed_documents method
    def embed_documents(self, texts: List[str]):
        limiter = rate_limit(self.requests_per_minute)
        results = []
        docs = list(texts)

        while docs:
            # Working in batches because the API accepts maximum 5
            # documents per request to get embeddings
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch :],
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)

        return [r.values for r in results]
    

class vertexModelAndEmbeddings:
    def __init__(self, meetings):
        self.projectid = "perceptive-ivy-388603"
        self.region = "us-central1"
        self.chatHistory = []
        vertexai.init(project=self.projectid, location=self.region)
        self.chat = ChatVertexAI()
        self.llm = VertexAI(
            model_name="text-bison@002",
            max_output_tokens=256,
            temperature=0.1,
            top_p=0.8,
            top_k=40,
            verbose=True,
        )
        self.embeddings = CustomVertexAIEmbeddings(
            requests_per_minute=100,
            num_instances_per_batch=5,
        )
        self.collection = chromadb.Client().create_collection(name="chat")
        self.meetings = meetings
        self.collection.add(
            documents=[f"{meeting['date']}.{meeting['summary']}" for meeting in self.meetings],
            metadatas=[{"title": meeting["title"]} for meeting in self.meetings],
            ids=[str(note["note_id"])for note in self.meetings]
        )
        self.notulensi_file = self.collection.get(
            ids=[str(note["note_id"]) for note in self.meetings]
        )
        self.notulensi_file = list(self.notulensi_file)

        self.db = Chroma.from_texts(self.notulensi_file, self.embeddings)
        self.retriver = self.db.as_retriever(search_type="similarity", search_k={"k": 10})
        self.qa = RetrievalQA(llm=self.llm, retriever=self.retriver, return_source_documents=True)

    def get_query(self, user_input):
        self.user_input = user_input
        if self.chatHistory == []:
            return user_input
        else:
            return f"{self.user_input}(context: {self.chatHistory[-1]})"
    
    def process_input(self, user_input):
        query = self.get_query(user_input)
        result = self.qa({"query": query})
        return result["result"]

if __name__ == "__main__":
    meetings = [
        {
            "date": "2022-01-01",
            "summary": "The meeting was about the budget for the next year",
            "title": "Budget Meeting",
            "note_id": 1
        },
        {
            "date": "2022-01-02",
            "summary": "The meeting was about the new product launch",
            "title": "Product Launch Meeting",
            "note_id": 2
        }
    ]
    model = vertexModelAndEmbeddings(meetings)
    model.chat("What was the budget meeting about?")





        
