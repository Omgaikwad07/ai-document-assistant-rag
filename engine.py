from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from openai import OpenAI
import os

loader = PyPDFLoader("data/dbms.pdf")

documents = loader.load()

print(f"total_pages: {len(documents)}")

# print("\n------- First Page ------\n")

# print(documents[0].page_content)

# print(documents[0].metadata)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 350,
    chunk_overlap = 50
)

chunks = splitter.split_documents(documents)

print(f"Chunks Length: {len(chunks)}")

print("\n------- First Chunk ------\n")

print(chunks[0].page_content)

print("\n -------Second chunk -----\n")

print(chunks[1].page_content)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embedding_model.embed_query(chunks[0].page_content)

print(f"Length of 1st vector: {len(vector)}")

print(f"First vector: {vector[:5]}")

db = FAISS.from_documents(
    chunks,
    embedding_model
)

question = "What is Normalization"

results = db.similarity_search(question, k=5)

print("\n========== RESULT 1 ==========\n")
print(results[0].page_content)

print("\n========== RESULT 2 ==========\n")
print(results[1].page_content)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
context = ""

for doc in results:
    context += doc.page_content
    context += "\n\n"

prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer is not present,
say:

"I couldn't find the answer in the uploaded document."

Context:

{context}

Question:

{question}
"""

respnose = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
        "role" : "user",
        "content": prompt
        }
    ]
)

print("\n Answer")
print(respnose.choices[0].message.content)