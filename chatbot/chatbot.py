import os
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from . import api_queries_jikanpy as api_queries
# se quiser executar no terminal, descomente a linha abaixo e comente a linha superior
# import api_queries_jikanpy as api_queries

SEP = os.path.sep
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + SEP
INTENTS_PATH = DIR_PATH + "intents.json"
WORDS_PATH = DIR_PATH + "words.pkl"
CLASSES_PATH = DIR_PATH + "classes.pkl"
CHAT_MODEL_PATH = DIR_PATH + "chatbot_model.h5"

lemmatizer = WordNetLemmatizer()
intents = json.loads(open(INTENTS_PATH).read())    # abre o documentos onde estão as perguntas e respostas pre def
words = pickle.load(open(WORDS_PATH, 'rb'))        # abre o documento gerado pela rede neural que tem as palavras
classes = pickle.load(open(CLASSES_PATH, 'rb'))    # abre o documento gerado pela rede neural que tem as classes
model = load_model(CHAT_MODEL_PATH)                # carrega o modelo


def is_noun(pos: str) -> bool: # função que verifica se uma lista tem substantivos
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('tagsets', quiet=True)
    # function to test if something is a noun
    return pos[:2] == 'NN' or pos[:2] == 'NNP'


def get_nouns(sentence: str) -> str:
    # pega os substantivos de acordo com a gramática implementada no nltk
    string_nouns = '' # string contendo todos os substantivos, para facilitar a busca na query
    tokenized = nltk.word_tokenize(sentence)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    for each in nouns:
        string_nouns = string_nouns + " " + each
    return string_nouns


def clean_sentences(sentence: str) -> list[str]:
    # faz o token, ou seja, pega a string e transforma em um valor numérico,
    # bem como classifica a string na gramática e elimina os sinais de pontuação
    cleaned_sentence = nltk.word_tokenize(sentence)
    cleaned_sentence = [lemmatizer.lemmatize(word) for word in cleaned_sentence]
    return cleaned_sentence


def bag_of_words(sentence: str) -> type(np):
    cleaned_sentence = clean_sentences(sentence)
    bag = [0] * len(words)  # faz um vetor de zeros do tamanho das palavras
    for each_word in cleaned_sentence:
        for i, word in enumerate(words):
            if word == each_word:
                bag[i] = i
    return np.array(bag)


def predict_class(sentence: str) -> list:   # classe que faz a predição da classe passando pelo modelo treinado
    bofwords = bag_of_words(sentence)
    result = model.predict(np.array([bofwords]), verbose=0)[0]  # verbose 0 é usado para que a barra de progresso de
    # inferência não apareça para o usuário
    error_threshhold = 0.20 # threshhold de 0.2, foi definido aleatoriamente
    results = [[i, r] for i, r in enumerate(result) if r > error_threshhold]
    results.sort(key=lambda x: x[1], reverse=True)
    lista = []
    for each in results:
        lista.append({'intent': classes[each[0]], 'probability': str(each[1])})
    return lista


def resposta(intents_list, intents_json) -> str:    # essa função escolhe aleatoriamente as respostas do chatbot predef.
    tag = intents_list[0]['intent']
    list_intents = intents_json['intents']
    result = ''
    for each in list_intents:
        if each['tag'] == tag:
            result = random.choice(each['responses'])
            break
    return result


def get_answer(question: str) -> str:
    answer = ""
    if "*" in question:
        answer = "Please don't use '*' on your question."
        return answer
    intent = predict_class(question)
    res = resposta(intent, intents)
    if 'tag' in res:
        # filtra a query, baseada no tipo de query é necessário ou não o segundo argumento
        # segundo a documentação da api: https://jikanpy.readthedocs.io/en/latest/
        if res[4:] == "characters":
            str_nouns = get_nouns(question)
            # pega os substantivos da entrada do usuário
            # só é utilizado o primeiro substantivo como argumento
            if len(str_nouns) > 1:
                answer = api_queries.query_filter(api_queries.query(res[4:], str_nouns))
            else:
                # se não houver substantivos, a query não pode ser feita
                # porque o segundo argumento é obrigatório
                answer = "Sorry, can you say it again? Please use capital letters on proper nouns."
        elif res[4:] == "anime":
            str_nouns = get_nouns(question)
            print(str_nouns)
            # pega os substantivos da entrada do usuário
            # só é utilizado o primeiro substantivo como argumento
            if len(str_nouns) > 1:
                answer = api_queries.query_filter(api_queries.query(res[4:], str_nouns))
            else:
                # se não houver substantivos, a query não pode ser feita
                # porque o segundo argumento é obrigatório
                answer = "Sorry, can you say it again? Please use capital letters on proper nouns."
        elif res[4:] == "genres":
            str_nouns = get_nouns(question)
            print(str_nouns)
            # pega os substantivos da entrada do usuário
            # só é utilizado o primeiro substantivo como argumento
            if len(str_nouns) > 1:
                answer = api_queries.query_filter(api_queries.query(res[4:], str_nouns))
        elif res[4:] == "recommendations":
            # essa query específica não precisa de argumento, portanto a função
            # get_nouns() não é chamada
            answer = api_queries.query_filter(api_queries.query(res[4:]))
        elif res[4:] == "season":
            # essa query específica não precisa de argumento, portanto a função
            # get_nouns() não é chamada
            answer = api_queries.query_filter(api_queries.query(res[4:]))
        elif res[4:] == "top":
            # essa query precisa de um numeral como segundo argumento
            # se esse numeral não for fornecido será usado o 1 como numeral
            # isso significa que será printado o melhor anime (top 1)
            answer = api_queries.query_filter(api_queries.query(res[4:], 1))
        elif res[4:] == "similar":
            str_nouns = get_nouns(question)
            # pega os substantivos da entrada do usuário
            # só é utilizado o primeiro substantivo como argumento
            if len(str_nouns) > 1:
                answer = api_queries.query(res[4:], str_nouns)
            else:
                # se não houver substantivos, a query não pode ser feita
                # porque o segundo argumento é obrigatório
                answer = "Sorry, can you say it again? Please use capital letters on proper nouns."
    else:
        answer = res

    if type(answer) == list:
        if len(answer) == 0:
            answer = ""
        else:
            answer = answer[0]
    return answer


def run_chatbot():  # função de execução do chatbot
    print("Chatbot running...")
    while True:
        question = input()
        intent = predict_class(question)
        res = resposta(intent, intents)
        if 'tag' in res:
            # filtra a query, baseada no tipo de query é necessário ou não o segundo argumento
            # segundo a documentação da api: https://jikanpy.readthedocs.io/en/latest/
            if res[4:] == "characters":
                nouns = get_nouns(question)
                # pega os substantivos da entrada do usuário
                # só é utilizado o primeiro substantivo como argumento
                if nouns:
                    print(api_queries.query_filter(api_queries.query(res[4:], nouns[0])))
                else:
                    # se não houver substantivos, a query não pode ser feita
                    # porque o segundo argumento é obrigatório
                    print("Sorry, can you say it again? Please use capital letters on proper nouns.")
            elif res[4:] == "anime":
                nouns = get_nouns(question)
                # pega os substantivos da entrada do usuário
                # só é utilizado o primeiro substantivo como argumento
                if nouns:
                    print(api_queries.query_filter(api_queries.query(res[4:], nouns[0])))
                else:
                    # se não houver substantivos, a query não pode ser feita
                    # porque o segundo argumento é obrigatório
                    print("Sorry, can you say it again? Please use capital letters on proper nouns.")
            elif res[4:] == "genres":
                nouns = get_nouns(question)
                # pega os substantivos da entrada do usuário
                # só é utilizado o primeiro substantivo como argumento
                print(api_queries.query_filter(api_queries.query(res[4:], nouns[0])))
            elif res[4:] == "recommendations":
                # essa query específica não precisa de argumento, portanto a função
                # get_nouns() não é chamada
                print(api_queries.query_filter(api_queries.query(res[4:])))
            elif res[4:] == "season":
                # essa query específica não precisa de argumento, portanto a função
                # get_nouns() não é chamada
                print(api_queries.query_filter(api_queries.query(res[4:])))
            elif res[4:] == "top":
                # essa query precisa de um numeral como segundo argumento
                # se esse numeral não for fornecido será usado o 1 como numeral
                # isso significa que será printado o melhor anime (top 1)
                print(api_queries.query_filter(api_queries.query(res[4:])), 1)
        else:
            print(res)


if __name__ == "__main__":
    run_chatbot()

