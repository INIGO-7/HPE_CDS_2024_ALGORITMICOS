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

from keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split

plt.style.use('ggplot')
np.__version__

class ConditionClassificationModel:

    def __init__(self):

        self.RESOURCES_PATH = "../res"
        self.DATASETS_PATH = os.path.join(self.resources_path, "datasets")
        self.MODELS_PATH = os.path.join(self.resources_path, "models")

    def train_model(self, df: pd.DataFrame, num_classes: int):

        int2label = {}

        for i, disease in enumerate(df['label'].unique()):
            int2label[i] = disease

        label2int = {v : k for k, v in int2label.items()}
        num_classes = len(int2label)

        df['label'] = df['label'].map(lambda x: label2int[x]).astype("category")
        df['text'] = df['text'].astype("str")

        X, y = df['text'].values, df['label'].values

        x_tokenizer = Tokenizer(filters = '')
        x_tokenizer.fit_on_texts(X)
        x_vocab = len(x_tokenizer.word_index) + 1
        print("X vocab:", x_vocab)

        train_x, val_x, train_y, val_y = train_test_split(X, y, test_size = 0.1, stratify = y)
        train_x.shape, val_x.shape, train_y.shape, val_y.shape

        BATCH_SIZE = 8

        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        train_encodings = tokenizer(list(train_x), padding="max_length", truncation=True)
        val_encodings = tokenizer(list(val_x), padding="max_length", truncation=True)

        train_dataset = tf.data.Dataset.from_tensor_slices((
            dict(train_encodings),
            train_y
        )).batch(BATCH_SIZE)

        val_dataset = tf.data.Dataset.from_tensor_slices((
            dict(val_encodings),
            val_y
        )).batch(BATCH_SIZE)

        model = TFAutoModelForSequenceClassification.from_pretrained(
            "bert-base-cased", 
            num_labels = num_classes, 
            id2label = int2label, 
            label2id = label2int,
            output_attentions = True
        )

        model.compile(
            loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer = keras.optimizers.Adam(learning_rate = 3e-5),
            metrics = ['accuracy']
        )

        EPOCHS = 5

        model.fit(train_dataset,
            epochs = EPOCHS,
            validation_data = val_dataset
        )

        model.save_pretrained(self.MODELS_PATH)