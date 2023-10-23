# Dependências (PT-BR)
O projeto foi feito utilizando:
- python 3.10

Instale as depencias:
```
pip install -r requirements.txt
```
Caso de erro no download do ntlk instale os pacotes com:
```
python -m nltk.downloader averaged_perceptron_tagger
```

# Rodando
Primeiro treine o modelo
```
python ./chatbot/treino_chatbot.py
```
Caso você queira utilizar o modelo na linha de comando:
```
python ./chatbot/chatbot.py
```
Caso você queira subir o servidor web:
```
flask --app app_main run --debug
```
# Requirements (ENG)
The project was made using:
- python 3.10

Install the requirements using this command:
```
pip install -r requirements.txt
```
In case of error during the ntlk donwload, use this command:
```
python -m nltk.downloader averaged_perceptron_tagger
```

# Running
First, train the model.
```
python ./chatbot/treino_chatbot.py
```
In case you want to use the model from the command line:
```
python ./chatbot/chatbot.py
```
In case you want to use it as an online server page (recommended):
```
flask --app app_main run --debug
```

