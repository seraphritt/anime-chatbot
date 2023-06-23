import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_sentences(sentence: str) -> list[str]:
    cleaned_sentence = nltk.word_tokenize(sentence)
    cleaned_sentence = [lemmatizer.lemmatize(word) for word in cleaned_sentence]
    return cleaned_sentence


def bag_of_words(sentence: str) -> type(np):
    cleaned_sentence = clean_sentences(sentence)
    bag = [0] * len(words)
    for each_word in cleaned_sentence:
        for i, word in enumerate(words):
            if word == each_word:
                bag[i] = i
    return np.array(bag)


def predict_class(sentence: str) -> list:
    bofwords = bag_of_words(sentence)
    result = model.predict(np.array([bofwords]), verbose=0)[0]
    error_threshhold = 0.20
    results = [[i, r] for i, r in enumerate(result) if r > error_threshhold]
    results.sort(key=lambda x: x[1], reverse=True)
    lista = []
    for each in results:
        lista.append({'intent': classes[each[0]], 'probability': str(each[1])})
    return lista


def resposta(intents_list, intents_json) -> str:
    tag = intents_list[0]['intent']
    list_intents = intents_json['intents']
    result = ''
    for each in list_intents:
        if each['tag'] == tag:
            result = random.choice(each['responses'])
            break
    return result


print("Test")
while True:
    message = input()
    intent = predict_class(message)
    res = resposta(intent, intents)
    print(res)
