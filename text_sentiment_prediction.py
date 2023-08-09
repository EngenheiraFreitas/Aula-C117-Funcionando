import pandas as pd
import numpy as np

import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
# dados de treinamento
train_data = pd.read_csv("./static/data_files/tweet_emotions.csv")    
training_sentences = []

for i in range(len(train_data)):
    sentence = train_data.loc[i, "content"]
    training_sentences.append(sentence)

#carregue o modelo
model = load_model("./static/model_files/Tweet_Emotion.h5")

vocab_size = 40000
max_length = 100
trunc_type = "post"
padding_type = "post"
oov_tok = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

#atribuir emoticons para emoções diferentes
emo_code_url = {
    "vazio": [0, "./static/emoticons/Empty.png"],
    "tristeza": [1,"./static/emoticons/Sadness.png" ],
    "entusiasmo": [2, "static/emoticons/Enthusiastic.png"],
    "neutro": [3, "./static/emoticons/Neutral.png"],
    "preocupação": [4, "./static/emoticons/Worry.png"],
    "surpresa": [5, "./static/emoticons/Surprise.png"],
    "amor": [6, "./static/emoticons/Love.png"],
    "diversão": [7, "./static/emoticons/Fun.png"],
    "ódio": [8, "./static/emoticons/Hate.png"],
    "felicidade": [9, "./static/emoticons/Happiness.png"],
    "tédio": [10, "./static/emoticons/Boredom.png"],
    "alívio": [11, "./static/emoticons/Relief.png"],
    "raiva": [12, "./static/emoticons/Anger.png"]
    
    }
# escreva a função para prever a emoção
def predict(text):
    predict_emotion = ""
    predict_emotion_img_url = ""
    
    if text != "":
        sentence = []
        sentence.append(text)
        
        sequences = tokenizer.texts_to_sequences(sentence)
        
        padded = pad_sequences(
            sequences, maxlen = max_length, padding = padding_type, truncating = trunc_type
        )
        testing_padded = np.array(padded)
        
        predicted_class_label = np.argmax(model.predict(testing_padded),axis=1)
        print(predicted_class_label)
        for key, value in emo_code_url.items():
            if value[0] == predicted_class_label:
                predict_emotion_img_url = value[1]
                predict_emotion = key
        return predict_emotion, predict_emotion_img_url
        
