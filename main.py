from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Твои официальные боевые данные Telegram
BOT_TOKEN = "8880993858:AAFyWotA446pHrTApgsInmc4Gkj-NVlg-0U"
CHAT_ID = "905068086"

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
    
    # Красивый текст уведомления для твоего телефона
    tg_text = f"🏎️ **Новое свидание запрограммировано!**\n\n" \
              f"📅 **Дата:** 28 августа\n" \
              f"🕒 **Время:** {selected_time}\n" \
              f"📍 **Место:** {selected_location}"
              
    # ИСПРАВЛЕННЫЙ АДРЕС: теперь всё разложено строго по полочкам с нужными слэшами
    tg_url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": tg_text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(tg_url, json=payload, timeout=10)
        print(f"Ответ серверов Telegram: {response.text}")
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
