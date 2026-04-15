import os
from flask import Flask, render_template_string, jsonify
from python_aternos import Client

app = Flask(__name__)

# Данные для Aternos (настрой их в панели Render в разделе Environment)
USER = os.getenv('ATERNOS_USER')
PASSWORD = os.getenv('ATERNOS_PASS')

# HTML-код прямо в переменной
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aternos Starter</title>
    <style>
        body {
            margin: 0; padding: 0;
            font-family: 'Segoe UI', sans-serif;
            background: #121212;
            display: flex; flex-direction: column; height: 100vh;
        }
        /* Трава в стиле Майнкрафт */
        .mc-grass {
            width: 100%; height: 50px;
            background: #5aa35a;
            border-bottom: 6px solid #3d6e3d;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        .content {
            flex: 1; display: flex; justify-content: center; align-items: center;
        }
        /* Стеклянная кнопка а-ля iPhone */
        .glass-btn {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 25px 50px;
            border-radius: 24px;
            color: white;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .glass-btn:hover { background: rgba(255, 255, 255, 0.15); transform: translateY(-2px); }
        .glass-btn:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="mc-grass"></div>
    <div class="content">
        <button class="glass-btn" onclick="startServer()" id="btn">Запустить Aternos</button>
    </div>

    <script>
        async function startServer() {
            const btn = document.getElementById('btn');
            btn.innerText = "Подключение...";
            btn.style.opacity = "0.7";
            
            try {
                const res = await fetch('/start-server', { method: 'POST' });
                const data = await res.json();
                alert(data.message);
            } catch (e) {
                alert("Ошибка запроса");
            } finally {
                btn.innerText = "Запустить Aternos";
                btn.style.opacity = "1";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    # Используем render_template_string для рендера из переменной
    return render_template_string(HTML_TEMPLATE)

@app.route('/start-server', methods=['POST'])
def start_server():
    try:
        if not USER or not PASSWORD:
            return jsonify({"status": "error", "message": "Переменные окружения не настроены!"}), 500
            
        at = Client.from_credentials(USER, PASSWORD)
        at.list_servers()[0].start()
        return jsonify({"status": "success", "message": "Команда на запуск отправлена!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
  
