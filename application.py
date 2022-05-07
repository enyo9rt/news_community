from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dev_module import news_getter
from dev_module import weather
from DB_ADMIN import account
from dev_module.comments import comments

application = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
application.register_blueprint(weather.weather_api)
application.register_blueprint(comments)

client = MongoClient(account.API_KEY)
db = client.Haromony


@application.route('/')
def home():
    return render_template('index.html')


@application.route("/news", methods=["GET"])
def news_get():
    """
    DB의 news_log 컬렉션에서 뉴스 정보를 가져오기
    :param: None
    :return: 문자열 리스트, 뉴스 정보
    """
    news_list = news_getter.get_news()
    return jsonify({'news_list': news_list})


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
