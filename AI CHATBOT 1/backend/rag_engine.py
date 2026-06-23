import os
import ollama
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from typing import List

class RAGEngine:
    def __init__(self, model_name="llama3.2:latest", collection_name="chatbot_docs"):
        self.model_name = model_name
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_function
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
        chunks = []
        for i in range(0, len(text), chunk_size - chunk_overlap):
            chunks.append(text[i : i + chunk_size])
        return chunks

    def add_document(self, pdf_path: str):
        text = self.extract_text_from_pdf(pdf_path)
        chunks = self.chunk_text(text)
        
        # Add to collection (Chroma will handle embeddings automatically)
        self.collection.add(
            ids=[f"{os.path.basename(pdf_path)}_{i}" for i in range(len(chunks))],
            documents=chunks,
            metadatas=[{"source": pdf_path} for _ in chunks]
        )

    def query(self, prompt: str, n_results: int = 3) -> str:
        # Retrieve relevant chunks (Chroma handles query embedding automatically)
        results = self.collection.query(
            query_texts=[prompt],
            n_results=n_results
        )
        
        # Check if we have any results
        context = ""
        if results and results.get("documents") and results["documents"][0]:
            context = "\n".join(results["documents"][0])
        
        # Construct final prompt
        if context:
            final_prompt = f"""
            You are a helpful Enterprise AI Assistant. 
            Use the following context to answer the user's question. 
            If the context doesn't contain the full answer, use your internal knowledge to provide a complete and helpful response, but prioritize information from the context.
            
            Context:
            {context}
            
            Question: {prompt}
            
            Answer:
            """
        else:
            # General question fallback
            final_prompt = f"""
            You are a helpful Enterprise AI Assistant. 
            No specific documents were found for this query, so please answer based on your general knowledge.
            
            Question: {prompt}
            
            Answer:
            """
        
        response = ollama.generate(model=self.model_name, prompt=final_prompt)
        return response["response"]

    def reset_collection(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)
