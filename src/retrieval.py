import os

import argparse
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

class InformationRetriever:

    """
    A class designed to retrieve information from documents stored in specific directories,
    process them using text splitting and save the processed chunks into a Chroma database
    with embeddings generated via OpenAI's Embeddings API.
    """

    def __init__(self):

        """
        Initializes the InformationRetriever by setting up the paths to documents and resources,
        loading OpenAI API keys, and initializing Chroma vector store with OpenAI embeddings.
        """

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

        """
        Retrieves OpenAI API keys from a specified file and stores them as attributes.

        Args:
            file_path (str): Path to the file containing the OpenAI API keys.
        """

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

        """
        Loads documents from a specified path using a PDF directory loader.

        Args:
            docs_path (str): The path where documents are stored.

        Returns:
            list[Document]: A list of loaded documents.
        """

        document_loader = PyPDFDirectoryLoader(docs_path)
        return document_loader.load()
    
    def split_documents(documents: list[Document]):

        """
        Splits loaded documents into smaller chunks using a character-based text splitter.

        Args:
            documents (list[Document]): A list of documents to split.

        Returns:
            list[Document]: A list of document chunks after splitting.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    
    def calculate_chunk_ids(chunks):

        """
        Assigns unique IDs to each chunk based on source and page information.

        Args:
            chunks (list[Document]): A list of document chunks.

        Returns:
            list[Document]: The list of chunks with updated metadata including unique IDs.
        """

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

        """
        Saves document chunks to a Chroma database for later retrieval and querying.

        Args:
            chunks (list[Document]): Document chunks to be saved.
        """

        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(openai_api_key=self.key_secret), persist_directory=self.CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}")
    
    def retrieve(self):

        """
        Full retrieval process: loads documents, splits them into chunks, assigns unique IDs,
        and saves them into the Chroma database.
        """

        self.get_openai_keys(self.openai_keys_file)

        documents = self.load_documents(self.ALL_DOCS)

        chunks = self.split_documents(documents)
        self.save_to_chroma(chunks)