from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MEDIASTACK_API_KEY = "fdedba661a59949ad0878b368261f3a0"
OPENWEATHERMAP_API_KEY = "77b3c06ce43a957cfbec5ac73df0c9bd"

@app.route('/get_data', methods=['POST'])
def get_data():
    data = request.get_json()
    date = data.get('date')
    
    if not date:
        return jsonify({"error": "Date not provided"}), 400

    # Fetch weather data
    weather_data = fetch_weather_data(date)
    
    # Fetch news data
    news_data = fetch_news_data(date)

    result = {
        "weather": weather_data,
        "news": news_data
    }

    return jsonify(result)

def fetch_weather_data(date):
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "rajkot",
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",
    }
    response = requests.get(weather_url, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        return {
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "humidity": weather_data["main"]["humidity"],
            "windSpeed": weather_data["wind"]["speed"]
        }
    else:
        return {
            "temperature": 0,
            "description": "Weather data not available",
            "humidity": 0,
            "windSpeed": 0
        }

def fetch_news_data(date):
    news_url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": MEDIASTACK_API_KEY,
        "languages": "en", 
        "date": date,
    }
    response = requests.get(news_url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get("data", [])
        news_list = []
        for article in articles:
            news_list.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("published_at")
            })
        return news_list
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True)
