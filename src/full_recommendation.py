import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm.notebook import tqdm
import re

import tensorflow as tf
from tensorflow import keras

from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification
from transformers import TextClassificationPipeline

from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

plt.style.use('ggplot')
np.__version__

class ConditionClassifierBERT:

    def __init__(self, num_classes: int):

        self.RESOURCES_PATH = "../res"
        self.DATASETS_PATH = os.path.join(self.resources_path, "datasets")
        self.MODELS_PATH = os.path.join(self.resources_path, "models")
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.num_classes = num_classes

    def xy_generation(self, df: pd.DataFrame):
        self.int2label = {}

        for i, disease in enumerate(df['label'].unique()):
            self.int2label[i] = disease

        self.label2int = {v : k for k, v in self.int2label.items()}

        df['label'] = df['label'].map(lambda x: self.label2int[x]).astype("category")
        df['text'] = df['text'].astype("str")

        return (df['text'].values, df['label'].values)

    def train_model(self, df: pd.DataFrame, num_classes: int, batch_size: int = 8, epochs: int = 5):

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

    def predict_disease(text : str, pipe) -> str:
        return pipe(text)[0][:2]
    
    def classify(self, model_path: str, text: str):

        model = TFAutoModelForSequenceClassification.from_pretrained(model_path)
        pipe = TextClassificationPipeline(model=model, tokenizer=self.tokenizer, top_k = self.num_classes)

        return self.predict_disease(text, pipe)