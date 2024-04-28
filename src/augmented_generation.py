import os
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class AugmentedGeneration:

    """
    Class to generate augmented responses based on documents using embedding similarity search and an AI model.
    """

    def __init__(self):
        """
        Initializes the AugmentedGeneration class by setting up paths and loading necessary resources.
        """

        self.RES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res')
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

    def get_openai_keys(self, file_path: str):
        """
        Retrieves OpenAI API keys from a given file path.
        
        :param file_path: Path to the file containing OpenAI keys.
        :return: Tuple containing the API key name and secret.
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

    def generate_answer(self, query: str):
        """
        Generates an answer to a given query using similarity search and AI model generation.
        
        :param query: String containing the query to be answered.
        :return: Tuple containing the generated answer, sources of the documents used, and the inferred topic.
        """

        # Search the DB.
        results = self.db.similarity_search_with_score(query, k=5)

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query)

        model = ChatOpenAI(openai_api_key=self.openai_key_secret, model="gpt-3.5-turbo")
        answer = model.predict(prompt)

        sources = [doc.metadata.get("source", None) for doc, _score in results]

        topic = model.predict(f"Considerando estas cuatro temáticas: Bienestar, Salud mental, Salud física o No aplica, necesito que se \
                                    devuelva únicamente de resultado la temática a la que crees que pertenece el siguiente texto: {answer}")

        return (answer, sources, topic)


if __name__ == "__main__":
    aug_gen = AugmentedGeneration()

    answer, sources, topic = aug_gen.generate_answer("Mi amiga sara tiene fiebre y se ha puesto enferma después de comer en un restaurante exótico. Necesitamos ayuda")

    print(answer, "\n", sources, "\n", topic)