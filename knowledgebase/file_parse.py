import pypdf
import numpy as np
import ollama
import faiss
import json

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF while preserving page numbers."""
    pdf_reader = pypdf.PdfReader(pdf_path)
    document_chunks = [{"text": page.extract_text(), "page": num + 1} 
                       for num, page in enumerate(pdf_reader.pages) if page.extract_text()]
    # for i in document_chunks:
    #     print(i)
    #     print('\n')
    # exit()
    return document_chunks

def generate_embeddings_by_page(chunks):
    """Generate embeddings for document chunks using Ollama."""
    embeddings = [ollama.embeddings(model="nomic-embed-text", prompt=chunk["text"])["embedding"]
                  for chunk in chunks]
    return np.array(embeddings, dtype=np.float32)

def store_embeddings(embeddings, documents):
    """Store embeddings in FAISS and save metadata for retrieval."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, "faiss_knowledge_base.index")

    # Save metadata mapping (page numbers)
    metadata = {i: doc["page"] for i, doc in enumerate(documents)}
    with open("metadata.json", "w") as f:
        json.dump(metadata, f)

    print("Embeddings stored successfully!")
    return index

def query_faiss(index, query_text, documents, top_k=3):
    """Query FAISS to find the most relevant document chunks."""
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query_text)["embedding"]
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

    distances, indices = index.search(query_embedding, top_k)
    
    results = [{"text": documents[doc_idx]["text"], 
                "page": documents[doc_idx]["page"], 
                "distance": distances[0][i]}
               for i, doc_idx in enumerate(indices[0])]
    
    return results

def format_for_rag(results):
    """Format retrieved results for AI-based answering."""
    formatted_text = "\n\n".join(
        [f"(Page {res['page']}) {res['text']}..." for res in results]
    )
    return f"Context from retrieved documents:\n{formatted_text}"


def generate_rag_answer(query, index, documents):
    """
    Retrieve the most relevant context using FAISS and generate an answer with citations using Ollama.
    """
    # Retrieve context from FAISS
    retrieved_context = query_faiss(index, query, documents, top_k=3)
    
    # Format the retrieved context with page references
    context_text = "\n\n".join([f"Page {doc['page']}: {doc['text']}" for doc in retrieved_context])
    
    # Build the prompt for the LLM
    prompt = f"""
        You are a knowledgeable assistant. Based on the following document excerpts, please answer the question with specific page references.

        Document Excerpts:
        {context_text}

        Question: {query}

        Provide a clear and concise answer with citations (page numbers) for your response.
    """
    
    # Generate the answer using Ollama's chat API (using your LLM model, e.g., deepseek-r1)
    response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]






# Process Workflow
pdf_path = "/Users/jeff.chen/git/AI-deepseek/pdfs/LRRP-Landlord-Handbook.pdf"  
documents = extract_text_from_pdf(pdf_path)



# Generate embeddings and store in FAISS
embeddings = generate_embeddings_by_page(documents)
faiss_index = store_embeddings(embeddings, documents)

query = "What is 2019 80% Area Median Income of 1 person in Hudson?"
answer = generate_rag_answer(query, faiss_index, documents)
    
print("Final Answer:")
print(answer)