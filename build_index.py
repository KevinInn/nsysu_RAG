from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss, pickle, os

DATA_DIR = "data"
texts = []

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".txt"):
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            texts.append(f.read())

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.create_documents(texts)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([chunk.page_content for chunk in chunks])

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

with open("faiss_index.pkl", "wb") as f:
    pickle.dump((index, chunks), f)

print("FAISS index 已儲存！")