#!/usr/bin/env python3
import os
import sys
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv("sample.env")
API_KEY = os.getenv("API_KEY")


logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_exchange_rate(base_currency, target_currency, date):
    url = f"http://localhost:8080/?from={base_currency}&to={target_currency}&date={date}"
    try:
        response = requests.post(url, data={"key": API_KEY}, timeout=10)
        response.raise_for_status()  # проверка HTTP ошибок
        data = response.json()
        # сервис возвращает {"error":"", "data":...}
        if isinstance(data, dict) and data.get("error"):
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
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Неожиданная ошибка: {e}")
        return None


def save_to_file(data, base_currency, target_currency, date):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{base_currency}_{target_currency}_{date}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")
        print(f"Ошибка при сохранении файла: {e}")


def main():
    if len(sys.argv) != 4:
        print("Использование: python lab02/currency_exchange_rate.py <base_currency> <target_currency> <date(YYYY-MM-DD)>")
        sys.exit(1)

    base_currency = sys.argv[1].upper()
    target_currency = sys.argv[2].upper()
    date = sys.argv[3]

    
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Используйте YYYY-MM-DD.")
        sys.exit(1)

    if not API_KEY:
        print("API_KEY не найден в .env. Откройте .env и добавьте API_KEY=...")
        logging.error("API_KEY not found in .env")
        sys.exit(1)

    data = get_exchange_rate(base_currency, target_currency, date)
    if data:
        save_to_file(data, base_currency, target_currency, date)

if __name__ == "__main__":
    main()
