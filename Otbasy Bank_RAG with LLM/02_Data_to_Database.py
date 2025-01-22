from langchain.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
import os
import shutil

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please check your .env file.")
print(f"OPENAI_API_KEY loaded: {api_key}")

CHROMA_PATH = "chroma"
PDF_FILE_PATH = 'C:\Личные данные\python_exp\Otbasy Bank_bot_RAG with LLM\Knowledge_base_Otbasy_bank_SSagynov.pdf'  

def main():
    generate_data_store()

def load_pdf():
    loader = PyPDFLoader(PDF_FILE_PATH)
    documents = loader.load()
    return documents

def generate_data_store():
    documents = load_pdf()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10] if len(chunks) > 10 else chunks[0]
    print(f"Chunk content: {document.page_content}")
    print(f"Metadata: {document.metadata}")

    return chunks

def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create the DB and automatically persist it
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
