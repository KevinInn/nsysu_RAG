from sentence_transformers import SentenceTransformer
import pickle
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

import os
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_PORT = os.getenv("OLLAMA_PORT")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
BASEURL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"
print(f"Using Ollama model: {OLLAMA_MODEL} at {BASEURL}")
if not OLLAMA_HOST or not OLLAMA_PORT or not OLLAMA_MODEL:
    raise ValueError("OLLAMA_HOST, OLLAMA_PORT, and OLLAMA_MODEL must be set in environment variables.")

model = SentenceTransformer("BAAI/bge-m3", device="cuda")
with open("faiss_index.pkl", "rb") as f:
    index, chunks = pickle.load(f)

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
        你是一位助教。請根據以下資料回答學生的問題：

        文件內容:
        {context}

        用戶問題:
        {question}

        請用簡潔中文回答：
        """,
        input_variables=["question", "context"],
    )

    rag_chain = prompt_template | llm | StrOutputParser()
    return rag_chain.invoke({"question": question, "context": context})