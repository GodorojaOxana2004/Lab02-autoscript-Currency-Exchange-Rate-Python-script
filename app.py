from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Заглушка курсов валют
FAKE_RATES = {
    "USD": {"EUR": 0.95, "JPY": 150.0},
    "EUR": {"USD": 1.05, "JPY": 160.0},
    "JPY": {"USD": 0.0067, "EUR": 0.0063}
}

@app.route("/api/exchange_rate")
def exchange_rate():
    base = request.args.get("base", "").upper()
    target = request.args.get("target", "").upper()
    date = request.args.get("date", "")

    # Проверка даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Неверный формат даты. Используйте YYYY-MM-DD."}), 400

    # Проверка валют
    if base not in FAKE_RATES or target not in FAKE_RATES.get(base, {}):
        return jsonify({"error": f"Курс {base} -> {target} недоступен"}), 400

    rate = FAKE_RATES[base][target]

    return jsonify({
        "base": base,
        "target": target,
        "date": date,
        "rate": rate
    })

if __name__ == "__main__":
    app.run(port=5000)
