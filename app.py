from flask import Flask, render_template, request, jsonify
from database import get_filtered_films, create_database_and_table
from Scrap import scrape_films
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)


def update_database():
    print("Обновление базы данных...")
    scrape_films()

scheduler = BackgroundScheduler()
scheduler.add_job(update_database, 'interval', minutes=30)
scheduler.start()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['GET'])
def filter_films():
    keyword = request.args.get('keyword', '')
    time_of_day = request.args.get('time_of_day', '')
    age_rating = request.args.get('age_rating', '')

    results = get_filtered_films(keyword, time_of_day, age_rating)

    if not results:
        return jsonify({'message': 'На сегодня нет доступных сеансов. Заходите завтра'})

    return results


has_scraped = False

if __name__ == '__main__':
    create_database_and_table()
    if not has_scraped:
        scrape_films()
        has_scraped = True
    app.run(debug=False, host="0.0.0.0")