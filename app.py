import os
from flask import Flask, render_template, jsonify
from python_aternos import Client

app = Flask(__name__)

# Получаем данные из переменных окружения Render
USER = os.getenv('ATERNOS_USER')
PASSWORD = os.getenv('ATERNOS_PASS')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-server', methods=['POST'])
def start_server():
    try:
        # Авторизация
        aternos = Client.from_credentials(USER, PASSWORD)
        servs = aternos.list_servers()
        
        # Выбираем первый сервер в списке и запускаем
        myserv = servs[0]
        myserv.start()
        
        return jsonify({"status": "success", "message": "Сервер запускается!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
  
