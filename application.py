from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    token_receive = request.cookies.get('mytoken')  # 클라이언트로부터 mytoekn에 담겨 온 토큰 정보 받아주기
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"id": payload["id"]})
        status = True
        return render_template('index.html', status=status, user_info=user_info)
    except :
        status = False
        return render_template('index.html', status=status)


@application.route("/news", methods=["GET"])
def news_get():
    """
    DB의 news_log 컬렉션에서 뉴스 정보를 가져오기
    :param: None
    :return: 문자열 리스트, 뉴스 정보
    """
    news_list = news_getter.get_news()
    print(news_list)
    return jsonify({'news_list': news_list})


@application.route('/fake_signin', methods=['POST'])
def fake_sign_in():
    # 로그인
    # username_receive = 'test_id'
    result = db.users.find_one({'id': 'test_id'})
    print(result)
    if result is not None:
        payload = {
         'id': 'test_id',
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').encode().decode('utf-8')
        print(f'token_content: {token}')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '똥'})


@application.route('/profile/<userid>')
def profile(userid):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (userid == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        user_info = db.users.find_one({"id": userid}, {"_id": False})
        return render_template('profile.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
