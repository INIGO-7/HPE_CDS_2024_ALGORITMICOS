import os

import argparse
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

class InformationRetriever:

    def __init__(self):
        self.RES_PATH = "../res"
        self.DOCS_PATH = os.path.join(self.RES_PATH, "docs")
        self.WELLNESS_PATH = os.path.join(self.DOCS_PATH, "Bienestar")
        self.PHYSICAL_HEALTH_PATH = os.path.join(self.DOCS_PATH, "Salud Fisica")
        self.MENTAL_HEALTH_PATH = os.path.join(self.DOCS_PATH, "Salud Mental")
        self.ALL_DOCS = os.path.join(self.DOCS_PATH, "All_docs")

        self.CHROMA_PATH = os.path.join(self.RES_PATH, "CHROMA_DB")
        self.DATA_PATH = "data"

        self.openai_keys_file = os.path.join(self.RES_PATH, os.path.join("keys", "openai_key.txt"))

        self.get_openai_keys(self.openai_keys_file)

        self.PROMPT_TEMPLATE = """Basándote exclusivamente en el siguiente contexto:
        {context}
        ---
        Resuelve la siguiente cuestión: {question}
        """

        embedding_function = OpenAIEmbeddings(openai_api_key=self.openai_key_secret)
        self.db = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=embedding_function)

    def get_openai_keys(self, file_path: str) -> None:
        keys = {}

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')
                    keys[key] = value
        except FileNotFoundError:
            print("El archivo especificado no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")

        # Devolvemos las llaves
        self.openai_key_name, self.openai_key_secret = keys.get('name'), keys.get('secret')

    def load_documents(docs_path: str):
        document_loader = PyPDFDirectoryLoader(docs_path)
        return document_loader.load()
    
    def split_documents(documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    
    def calculate_chunk_ids(chunks):

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks
    
    def save_to_chroma(chunks: list[Document]):

        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(openai_api_key=self.key_secret), persist_directory=self.CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}")
    
    def retrieve(self):

        self.get_openai_keys(self.openai_keys_file)

        documents = self.load_documents(self.ALL_DOCS)

        chunks = self.split_documents(documents)
        self.save_to_chroma(chunks)