# app_ollama.py
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import requests, json

app = FastAPI()

mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["finance"]

class Query(BaseModel):
    question: str

@app.post("/qa")
def qa(q: Query):
    docs = list(db.stock_prices.find().sort("ts", -1).limit(5))
    if docs:
        context = "\n".join(
            [f"{d.get('company', 'Unknown')} price: {d.get('price', 'N/A')}" for d in docs]
        )
    else:
        context = "No financial data found in the database."

    prompt = f"""
        You are an AI financial assistant.
        You will answer questions based on the following financial data context.
        Context:
        {context}
        Question: {q.question}
        Answer in clear English or Thai (depending on the language of the question), 
        and explain your reasoning briefly.
        """
    payload = {"model": "llama3", "prompt": prompt, "stream": True}

    try:
        with requests.post("http://localhost:11434/api/generate", json=payload, stream=True) as r:
            full = ""
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    continue
                if "response" in chunk:
                    full += chunk["response"]
                if chunk.get("done"):
                    break
        return {"answer": full.strip()}
    except Exception as e:
        return {"error": str(e)}
