from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dev_module import news_getter
from dev_module import weather
from DB_ADMIN import account
from dev_module.comments import comments
from datetime import datetime, timedelta
import jwt

application = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
application.register_blueprint(weather.weather_api)
application.register_blueprint(comments)

client = MongoClient(account.API_KEY)
db = client.Haromony
SECRET_KEY = 'test'

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


@application.route('/fake_signin', methods=['POST'])
def fake_sign_in():
    # 로그인
    username_receive = 'test_id'
    result = db.users.find_one({'username': username_receive})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').encode().decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '똥'})


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
