from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from dev_module import news_getter
from dev_module import weather
from DB_ADMIN import account
from dev_module import detail
from datetime import datetime, timedelta
import jwt
import hashlib

application = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
application.register_blueprint(weather.weather_api)
application.register_blueprint(detail.detail)

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

@application.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@application.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@application.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_id": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nick_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@application.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"user_id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
