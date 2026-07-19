from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Твои официальные боевые данные Telegram
BOT_TOKEN = "8880993858:AAFyWotA446pHrTApgsInmc4Gkj-NVlg-0U"
CHAT_ID = "905068086"

# ДОБАВЬ ЭТУ ФУНКЦИЮ (решает все проблемы с картинками и шрифтами)
@app.after_request
def add_csp_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; "
        "style-src 'unsafe-inline' https://fonts.googleapis.com; "
        "script-src 'unsafe-inline';"
    )
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/instruction')
def instruction():
    return render_template('instruction.html')

@app.route('/get-gift')
def get_gift():
    return render_template('get_gift.html')

@app.route('/submit-gift', methods=['POST'])
def submit_gift():
    data = request.json
    selected_time = data.get('time')
    selected_location = data.get('location')
    
    tg_text = f"🏎 Новое свидание запрограммировано!**\n\n" \
              f"📅 **Дата: 28 августа\n" \
              f"🕒 Время: {selected_time}\n" \
              f"📍 Место: {selected_location}"
              
    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": tg_text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(tg_url, json=payload, timeout=10)
        print(f"Ответ серверов Telegram: {response.text}")
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "message" in update and "text" in update["message"]:
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"]["text"]
        
        if text.startswith("/start"):
            welcome_text = "Привет, Лиза! ❤️\n\n" \
                           "🏎 Твой секретный веб-сервер успешно подключен к Telegram!\n" \
                           "🔐 Канал связи полностью защищен.\n\n" \
                           "Как только именинник Александр выберет время и локацию встречи на сайте, я мгновенно перенаправлю его ответ в этот чат! До связи!"
            
            tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": welcome_text}
            requests.post(tg_url, json=payload, timeout=10)
            
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
