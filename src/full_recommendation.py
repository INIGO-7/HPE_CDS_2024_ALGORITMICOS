import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from tqdm.notebook import tqdm
import re

import tensorflow as tf
from tensorflow import keras

from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification
from transformers import TextClassificationPipeline

from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

plt.style.use('ggplot')
np.__version__

class ConditionClassifierBERT:

    """
    A classifier for medical conditions using BERT model from the Hugging Face Transformers library.

    Attributes:
        num_classes (int): Number of unique labels/classes in the dataset.
        RESOURCES_PATH (str): Base path for resources.
        DATASETS_PATH (str): Path to datasets within the resources.
        MODELS_PATH (str): Path to save trained models.
        tokenizer: Pretrained tokenizer from the BERT model.
    """

    def __init__(self, num_classes: int, first_aid_data_path):

        """
        Initializes the classifier with paths and a pretrained BERT tokenizer.

        Args:
            num_classes (int): Number of unique classes or labels in the classification problem.
        """

        self.RES_PATH = os.path.join("../res")
        self.DATASETS_PATH = os.path.join(self.RES_PATH, "datasets")
        self.MODELS_PATH = os.path.join(self.RES_PATH, "models")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.num_classes = num_classes

        self.first_aid_data = self.load_data(first_aid_data_path)

    def xy_generation(self, df: pd.DataFrame):

        """
        Generates input features and target labels from the dataset.

        Args:
            df (pd.DataFrame): Dataframe containing the text and corresponding labels.

        Returns:
            tuple: Tuple containing arrays of texts and their corresponding labels.
        """

        self.int2label = {}

        for i, disease in enumerate(df['label'].unique()):
            self.int2label[i] = disease

        self.label2int = {v : k for k, v in self.int2label.items()}

        df['label'] = df['label'].map(lambda x: self.label2int[x]).astype("category")
        df['text'] = df['text'].astype("str")

        return (df['text'].values, df['label'].values)

    def train_model(self, df: pd.DataFrame, num_classes: int, batch_size: int = 8, epochs: int = 5):

        """
        Trains the BERT model using the provided DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing the data.
            num_classes (int): Number of classes in the dataset.
            batch_size (int): Size of each batch for training.
            epochs (int): Number of epochs to train the model.

        Saves the trained model to MODELS_PATH.
        """

        X, y = self.xy_generation(df)

        x_tokenizer = Tokenizer(filters = '')
        x_tokenizer.fit_on_texts(X)

        train_x, val_x, train_y, val_y = train_test_split(X, y, test_size = 0.1, stratify = y)
        train_x.shape, val_x.shape, train_y.shape, val_y.shape

        train_encodings = self.tokenizer(list(train_x), padding="max_length", truncation=True)
        val_encodings = self.tokenizer(list(val_x), padding="max_length", truncation=True)

        train_dataset = tf.data.Dataset.from_tensor_slices((
            dict(train_encodings),
            train_y
        )).batch(batch_size)

        val_dataset = tf.data.Dataset.from_tensor_slices((
            dict(val_encodings),
            val_y
        )).batch(batch_size)

        model = TFAutoModelForSequenceClassification.from_pretrained(
            "bert-base-cased", 
            num_labels = num_classes, 
            id2label = self.int2label, 
            label2id = self.label2int,
            output_attentions = True
        )

        model.compile(
            loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer = keras.optimizers.Adam(learning_rate = 3e-5),
            metrics = ['accuracy']
        )

        model.fit(train_dataset,
            epochs = epochs,
            validation_data = val_dataset
        )

        model.save_pretrained(self.MODELS_PATH)

    def predict_disease(self, text : str, pipe) -> str:

        """
        Predicts the medical condition for a given text using a specified pipeline.

        Args:
            text (str): Text input for which to predict the medical condition.
            pipe: Pipeline object used for prediction.

        Returns:
            str: Predicted medical condition.
        """

        return pipe(text)[0][:2]
    
    def classify(self, model_path: str, text: str):

        """
        Classifies the input text using a trained model.

        Args:
            model_path (str): Path to the trained BERT model.
            text (str): Text input to classify.

        Returns:
            Prediction result from the TextClassificationPipeline.
        """

        model = TFAutoModelForSequenceClassification.from_pretrained(model_path)
        pipe = TextClassificationPipeline(model=model, tokenizer=self.tokenizer, top_k = self.num_classes)

        return self.predict_disease(text, pipe)
    
    def load_data(self, filename):
        # Load JSON data from a file
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def get_advice_by_tag(self, data, tag):
        # Search for the tag in the data and return the corresponding advice
        for entry in data['intents']:
            if entry['tag'].lower() == tag.lower():
                return entry['responses']
        return "No advice found for this tag."

    def get_first_aid(self, model_path: str, text: str):
        
        condition = self.classify(model_path, text)[0]['label']
        return condition, self.get_advice_by_tag(self.first_aid_data, condition)

if __name__ == "__main__":

    prompt = "I was with my son in a boat and then he fell overboard. We rescued him from the water, but he is now unconscious. What should I do?"

    RES_PATH = os.path.join("../res")
    DATASETS_PATH = os.path.join(RES_PATH, "datasets")
    MODELS_PATH = os.path.join(RES_PATH, "models")
    first_aid_path = os.path.join(DATASETS_PATH, "Medical_Aid_v2.json")
    # model_path = os.path.join(MODELS_PATH, os.path.join("bert_finetuned", "tf_model.h5"))
    model_path = os.path.join(MODELS_PATH, "bert_finetuned")

    classifier = ConditionClassifierBERT(24, first_aid_path)
    condition, advice = classifier.get_first_aid(model_path, prompt)

    print("------------------------------")
    print(f"Prompt: {prompt}")
    print(f"Condition: {condition}")
    print(f"Advice: {advice}")