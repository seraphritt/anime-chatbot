# Dependencias
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
