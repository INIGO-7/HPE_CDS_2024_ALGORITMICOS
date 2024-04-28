from transformers import MarianMTModel, MarianTokenizer
import os

class Translator:

    def __init__(self):
        self.RES_PATH = "../res"
        self.MODELS_PATH = os.path.join(self.resources_path, "models")
        model_path = os.path.join(self.MODELS_PATH, os.path.join("Helsinki-NLP", "opus-mt-en-es"))
        self.model = MarianMTModel.from_pretrained(model_path)
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)

    def translate(self, text):

        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        translated_tokens = self.model.generate(input_ids)

        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        return translated_text
    
if __name__ == '__main__':

    translator = Translator()

    print(translator.translate("Hi my name is Sara and I come from Idaho, USA!"))