import sqlite3
import json

DB_FILE = 'films.db'
def check():
    conn = sqlite3.connect('Films.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM films;")
    rows = cursor.fetchall()

    print("Содержимое таблицы 'films':\n")
    for row in rows:
        film_id = row[0]
        title = row[1]
        age_rating = row[2]
        gener = row[3]
        time = row[4]
        image_url = row[5]
        print(f"ID: {film_id}")
        print(f"Название: {title}")
        print(f"Возраст: {age_rating}")
        print(f"Время: {gener}\n")
        print(f"Жанр: {time}\n")
        print(f"image_url: {image_url}\n")

    cursor.close()
    conn.close()

def exists():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films';")
    result = cursor.fetchone()
    if result:
        print("Таблица 'films' существует.")
    else:
        print("Таблица 'films' не существует.")
    cursor.close()
    conn.close()

import os
def rem():
    try:
        # Убедитесь, что база данных закрыта
        conn = sqlite3.connect('Films.db')
        conn.close()

        # Удалите файл базы данных
        os.remove('Films.db')
        print("База данных удалена.")
    except Exception as e:
        print(f"Ошибка: {e}")

rem()
#exists()
#check()