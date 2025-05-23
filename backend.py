from sentence_transformers import SentenceTransformer
import faiss, pickle
import requests
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

model = SentenceTransformer("all-MiniLM-L6-v2")
with open("faiss_index.pkl", "rb") as f:
    index, chunks = pickle.load(f)

import os
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
BASEURL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

def get_answer(question):
    q_embedding = model.encode([question])
    D, I = index.search(q_embedding, k=3)
    context = "\n\n".join([chunks[i].page_content for i in I[0]])
    
    
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
        max_retries=2,
        streaming=True,
        base_url=BASEURL,
    )
    
    prompt_template = PromptTemplate(
        template="""
        文件內容: {context} 
        ...
        用戶問題: {question} 
        回答:""",
        input_variables=["question", "context"],
    )
    
    rag_chain = prompt_template | llm | StrOutputParser()
    
    prompt = f"你是一位助教。請根據以下資料回答學生的問題。\n\n資料：\n{context}\n\n問題：{question}\n\n請用簡潔中文回答："
    
    # response = rag_chain.invoke(input={"question": query, "context": documents})
    
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return res.json().get("response", "回答失敗")