from transformers import MarianMTModel, MarianTokenizer
import os

class Translator:

    """
    A class for translating text using the Marian neural machine translation models from Hugging Face.

    Attributes:
        RES_PATH (str): Base path for resources.
        MODELS_PATH (str): Path where model resources are stored.
        model (MarianMTModel): The loaded Marian machine translation model.
        tokenizer (MarianTokenizer): The tokenizer corresponding to the Marian model.
    """

    def __init__(self):

        """
        Initializes the Translator by setting up the path to model resources and loading the model and tokenizer.
        """

        self.RES_PATH = "../res"
        self.MODELS_PATH = os.path.join(self.resources_path, "models")
        model_path = os.path.join(self.MODELS_PATH, os.path.join("Helsinki-NLP", "opus-mt-en-es"))
        self.model = MarianMTModel.from_pretrained(model_path)
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)

    def translate(self, text):

        """
        Translates text from English to Spanish using a pretrained MarianMTModel.

        Args:
            text (str): The text to translate in English.

        Returns:
            str: The translated text in Spanish.
        """

        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        translated_tokens = self.model.generate(input_ids)

        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        return translated_text
    
if __name__ == '__main__':

    translator = Translator()

    print(translator.translate("Hi my name is Sara and I come from Idaho, USA!"))