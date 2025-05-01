import os
from dotenv import load_dotenv
import chromadb
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from mistralai import Mistral

# Folder where your PDFs are stored
folder_path = "data"

# Load environment variables
load_dotenv()
mistral_key = os.getenv("MISTRAL_API_KEY")

# Initialize embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="core/vector_db")
collection_name = "legal_assitant"
collection = chroma_client.get_or_create_collection(name=collection_name)

# Initialize Mistral chat client
chat_client = Mistral(api_key=mistral_key)

# ==== Step 1: Extract text from all PDFs ====
def extract_text_from_all_pdfs(folder_path):
    print("==== Extracting text from all PDFs in folder ====")
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            doc = fitz.open(path)
            text = "\n".join([page.get_text() for page in doc])
            documents.append({"id": filename, "text": text})
    return documents

# ==== Step 2: Split text into chunks ====
def split_text(text, chunk_size=1000, chunk_overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# ==== Step 3: Load, chunk, and prepare embeddings ====
documents = extract_text_from_all_pdfs(folder_path)

chunks = []
ids = []
for doc in documents:
    doc_chunks = split_text(doc["text"])
    for i, chunk in enumerate(doc_chunks):
        chunks.append(chunk)
        ids.append(f"{doc['id']}_chunk_{i}")

# ==== Step 4: Generate embeddings and insert into Chroma ====
print("==== Generating embeddings and inserting into ChromaDB ====")
embeddings = embedding_model.encode(chunks).tolist()  # batch encode
collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)

# ==== Step 5: Query top relevant chunks ====
def query_documents(question, n_results=3):
    results = collection.query(query_texts=[question], n_results=n_results)
    return results["documents"][0]

# ==== Step 6: Generate response from Mistral ====
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are a helpful legal assistant answering questions using the following context "
        "from the Constitution of Nepal. If the answer is not found in the context, say 'I don't know.'\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer in a concise and clear way:"
    )
    response = chat_client.chat.complete(
        model="mistral-large-latest",
        messages=[{
            "role": "user",
            "content": prompt,
        }]
    )
    return response.choices[0].message.content