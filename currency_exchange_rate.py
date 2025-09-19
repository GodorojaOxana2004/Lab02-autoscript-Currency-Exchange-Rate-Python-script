#!/usr/bin/env python3
import os
import sys
import json
import logging
from datetime import datetime
import requests

# Настройка логирования ошибок
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Функция для запроса курса валют
def get_exchange_rate(base_currency, target_currency, date):
    url = f"http://localhost:5000/api/exchange_rate?base={base_currency}&target={target_currency}&date={date}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка HTTP ошибок
        data = response.json()
        if "error" in data:
            raise ValueError(data["error"])
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        print(f"Ошибка запроса к API: {e}")
        return None
    except ValueError as e:
        logging.error(f"API returned error: {e}")
        print(f"Ошибка API: {e}")
        return None

# Функция для сохранения данных в JSON
def save_to_file(data, base_currency, target_currency, date):
    os.makedirs("data", exist_ok=True)
    filename = f"data/exchange_{base_currency}_{target_currency}_{date}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")
        print(f"Ошибка при сохранении файла: {e}")

# Основная логика
def main():
    if len(sys.argv) != 4:
        print("Использование: python currency_exchange_rate.py <base_currency> <target_currency> <date(YYYY-MM-DD)>")
        return

    base_currency = sys.argv[1].upper()
    target_currency = sys.argv[2].upper()
    date = sys.argv[3]

    # Проверка формата даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Используйте YYYY-MM-DD.")
        return

    data = get_exchange_rate(base_currency, target_currency, date)
    if data:
        save_to_file(data, base_currency, target_currency, date)

if __name__ == "__main__":
    main()
