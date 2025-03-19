import pypdf
import numpy as np
import ollama
import faiss
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF while preserving page numbers."""
    pdf_reader = pypdf.PdfReader(pdf_path)
    document_chunks = []

    for page_num, page in enumerate(pdf_reader.pages, start=1):
        text = page.extract_text()
        if text:
            document_chunks.append({"text": text, "page": page_num})

    # print(document_chunks)
    return document_chunks


def generate_embeddings_by_page(chunks):
    embeddings = []
    for chunk in chunks:
        response = ollama.embeddings(model="nomic-embed-text", prompt=chunk["text"])
        embeddings.append(response['embedding'])
    return np.array(embeddings)

def store_embeddings(embeddings, documents):
    """Stores document embeddings in FAISS for fast retrieval."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance-based index
    index.add(embeddings)
    
    # Save metadata mapping (page numbers)
    metadata = {i: doc["page"] for i, doc in enumerate(documents)}

    # Save FAISS index and metadata
    faiss.write_index(index, "faiss_knowledge_base.index")
    with open("metadata.json", "w") as f:
        json.dump(metadata, f)

    print("Embeddings stored successfully!")
    return index

# 4. Query FAISS for the most relevant document chunks
def query_faiss(index, query_text, documents, top_k=3):
    """Query FAISS to find the most relevant document chunks."""

    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query_text)["embedding"]
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)  # Convert to FAISS format
    
    distances, indices = index.search(query_embedding, top_k)  # Search FAISS for nearest neighbors

    results = []
    for i in range(len(indices[0])):
        doc_idx = indices[0][i]
        results.append({
            "text": documents[doc_idx]["text"],
            "page": documents[doc_idx]["page"],
            "distance": distances[0][i]  # Lower distance = more relevant
        })

    return results


# Step 1: Extract text from PDF
pdf_path = "/Users/jeff.chen/git/AI-deepseek/pdfs/LRRP-Landlord-Handbook.pdf" # Replace with your actual PDF path
documents = extract_text_from_pdf(pdf_path)



# Step 2: Generate embeddings
embeddings = generate_embeddings_by_page(documents)
print(embeddings.shape)

# Step 3: Store embeddings in FAISS
faiss_index = store_embeddings(embeddings, documents)


query = "What is General Restrictions?"  # Example query
results = query_faiss(faiss_index, query, documents)

for res in results:
    print(f"Page: {res['page']}, Score: {res['distance']:.4f}\nText: {res['text']}\n")
