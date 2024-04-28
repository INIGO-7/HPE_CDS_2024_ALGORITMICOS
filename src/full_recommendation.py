import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm.notebook import tqdm
import re
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import Tokenizer

plt.style.use('ggplot')
np.__version__

class ConditionClassificationModel:

    def __init__(self):

        self.resources_path = "../res"
        self.datasets_path = os.path.join(self.resources_path, "datasets")
        self.models_path = os.path.join(self.resources_path, "models")

    def train_model(self, df: pd.DataFrame, num_classes: int):

        df = pd.read_csv('datasets/Symptom2Disease.csv').iloc[:, 1:]
        df.head()

        model = TFAutoModelForSequenceClassification.from_pretrained(os.path.join(models_path, "bert_finetuned"))

        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

        pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k = num_classes)