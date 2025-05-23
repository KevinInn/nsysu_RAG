from sentence_transformers import SentenceTransformer
import faiss, pickle
import requests

model = SentenceTransformer("all-MiniLM-L6-v2")
with open("faiss_index.pkl", "rb") as f:
    index, chunks = pickle.load(f)

def get_answer(question):
    q_embedding = model.encode([question])
    D, I = index.search(q_embedding, k=3)
    context = "\n\n".join([chunks[i].page_content for i in I[0]])

    prompt = f"你是一位助教。請根據以下資料回答學生的問題。\n\n資料：\n{context}\n\n問題：{question}\n\n請用簡潔中文回答："

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return res.json().get("response", "回答失敗")