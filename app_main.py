from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Inicializa uma lista para armazenar as mensagens do chat
message_history = []

@app.route('/')
def index():
    return render_template('index.html', mensagens=enumerate(message_history))

# Rota para o envio de mensagens
@app.route('/send', methods=["POST"])
def send():
    # Recupera o texto digitado no formulário de entrada de chat
    chat_input = request.form.get("chat-input")
    if chat_input != "":
        # Adiciona a mensagem na lista message_history, convertendo a primeira letra para maiúscula
        message_history.append(chat_input.capitalize())

        #Pega respota da IA
        resposta = "Resposta temporária para: " + chat_input
        # Adiciona a resposta lista message_history
        message_history.append(resposta.capitalize())

    return redirect(url_for("index")) 

if __name__ == '__main__':
    app.run()