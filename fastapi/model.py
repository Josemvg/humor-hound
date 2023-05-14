import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import pickle

class CNN:
    def __init__(self) -> None:
        # path_to_models = "fastapi/models/"
        self.model = self._load_model()
        self.tokenizer = self._load_tokenizer()
        self.contractions = pd.read_csv("./data/Contractions.csv", sep=";")
        self.stop_words = stopwords.words("english")
        self.lemmatizer = WordNetLemmatizer()

    def _load_tokenizer(self):
        with open('./models/tokenizer.pickle', 'rb') as f:
            tokenizer = pickle.load(f)

        return tokenizer

    def _load_model(self):
            
        model = tf.keras.models.load_model('./models/cnn_model.h5')
        return model
    
    def _preprocess_text(self, text: str) -> str:
        # Convert to lowercase
        text = text.lower()
        # Expand contractions
        text = " ".join(
            [self.contractions[self.contractions["contraction"] == word]["expanded"].values[0]
                if word in self.contractions["contraction"].values
                else word for word in text.split()])
        # Remove non-alphanumeric characters
        text = re.sub(r'[^\w\s]', '', text)
        # Remove digits
        text = re.sub(r'\d', '', text)
        # Remove stop words
        text = " ".join([word for word in text.split() if word not in self.stop_words])
        # Lemmatize words
        text = " ".join([self.lemmatizer.lemmatize(word) for word in text.split()])
        return text
    
    def _tokenize(self, text: str) -> str:
        tokenized_text = self.tokenizer.texts_to_sequences(text)
        padded_text = pad_sequences(tokenized_text, maxlen=14, padding="post")
        return padded_text


    def _predict(self, text: str):

        # preprocess data
        preprocessed_text = self._preprocess_text(text=text)
        sequence_text = self._tokenize(text=preprocessed_text)

        predictions = self.model.predict(sequence_text)

        return str(np.mean(predictions))
    
if __name__=="__main__":
    model = CNN()

    sample = "Donald Trump runs for president again!"

    prediction = model._predict(sample)

    print(prediction)
