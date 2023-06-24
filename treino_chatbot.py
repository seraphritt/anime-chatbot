import random
import json
import pickle
import numpy as np
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download("punkt")  # precisa baixar esses pacotes da própria biblioteca nltk
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()    # instancia o lemmatizer, responsavel por aplicar a gramática

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', ',', '.']    # pontuações a serem ignoradas

for intent in intents['intents']:   # loop por cada intent no arquivo intents.json
    for pattern in intent['patterns']:
        wordList = nltk.word_tokenize(pattern)  # faz o token de cada frase presente no arquivo intents.json, na área
        # de patterns
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:    # adiciona a tag, se ainda não está presente
            classes.append(intent['tag'])

# list comprehension para pegar cada palavra e aplicar o método lemmatize, aplicando assim a gramática.
words = [lemmatizer.lemmatize(word) for word in words if word not in ignoreLetters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb')) # arquivos a serem escritos, esse formato é da biblioteca pickle
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [lemmatizer.lemmatize(word.lower()) for word in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]

# rede neural com arquitetura pré definida
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))
sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# aqui treina-se o modelo com 200 épocas e após isso ele é salvo no formato .h5
model.fit(trainX, trainY, epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5')
print('Done')
