import sqlite3
import os

def create_database_and_table():
    if os.path.exists('films.db'):
        print("База данных 'films.db' уже существует.")
        conn = sqlite3.connect('Films.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='films';
        """)
        result = cursor.fetchone()

        if result:
            print("Таблица 'films' уже существует.")
        else:
            print("Таблица 'films' не найдена. Создание таблицы...")
            cursor.execute("""
                CREATE TABLE films (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    age_rating TEXT NOT NULL,
                    genre TEXT NOT NULL,
                    time TEXT NOT NULL,
                    image_url TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Таблица 'films' успешно создана.")
    else:
        print("Создание базы данных...")
        conn = sqlite3.connect('films.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                age_rating TEXT NOT NULL,
                genre TEXT NOT NULL,
                time TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Таблица 'films' успешно создана.")
    conn.close()


def get_filtered_films(keyword, time_of_day, age_rating):
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()

    query = "SELECT * FROM films WHERE 1=1"
    params = []

    if keyword:
        query += " AND title LIKE ?"
        params.append(f"%{keyword}%")
    if time_of_day:
        if time_of_day == "morning":
            query += " AND time BETWEEN '06:00' AND '12:00'"
        elif time_of_day == "afternoon":
            query += " AND time BETWEEN '12:00' AND '18:00'"
        elif time_of_day == "evening":
            query += " AND time BETWEEN '18:00' AND '23:59'"
    if age_rating:
        query += " AND age_rating LIKE ?"
        params.append(f"%{age_rating}%")

    cursor.execute(query, params)
    results = cursor.fetchall()

    films = []
    for film in results:
        films.append({
            'id': film[0],
            'title': film[1],
            'age_rating': film[2],
            'genre': film[3],
            'time': film[4],
            'image_url': film[5]
        })

    cursor.close()
    conn.close()
    return films

