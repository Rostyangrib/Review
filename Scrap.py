import sqlite3
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



def clear_table():
    conn = sqlite3.connect('films.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='films'")
    conn.commit()
    print("Таблица очищена.")
    cursor.close()
    conn.close()

def scrape_films():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    clear_table()
    try:
        driver.get('https://newcinema38.ru/')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "releases-item"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        films = soup.find_all('a', class_='releases-item NH6Te')

        conn = sqlite3.connect('films.db')
        cursor = conn.cursor()

        for film in films:
            try:
                img_tag = film.find('img')
                image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''

                title = film.find('div', class_='releases-item__info').find('div', class_='releases-item-description').find(
                    'div', class_='releases-item-description__title text text--size-24')
                title = title.text.strip() if title else 'Неизвестно'

                disc = film.find('div', class_='releases-item__info').find('div', class_='releases-item-description').find(
                    'div', class_='releases-item-description__badge text text--size-12')
                spans = disc.find_all('span') if disc else []
                age_rating = spans[0].text.strip() if len(spans) > 0 else ''
                genre = spans[1].text.strip() if len(spans) > 1 else ''

                time_sel = film.find('div', class_='releases-item__info').find('div', class_='releases-item-schedule').find_all('div', class_='seance-item')
                for t in time_sel:
                    time_film = t.find('div', class_='seance-item__container').find(
                        'div', class_='seance-item__item').find(
                        'div', class_='seance-item__time text text--size-18')
                    time_film = time_film.text.strip() if time_film else '00:00'
                    cursor.execute("""
                        INSERT INTO films (title, age_rating, genre, time, image_url) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (title, age_rating, genre, time_film, image_url))
                    conn.commit()

                print("Фильм добавлен:", title)

            except Exception as e:
                print(f"Ошибка обработки фильма: {e}")
                continue

        cursor.close()
        conn.close()

    finally:
        driver.quit()


