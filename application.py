from site_view import main_site, join_site, detail_site
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from dev_module import weather
from CONFIG import account
from werkzeug.utils import secure_filename
import jwt

application = Flask(__name__)
# weather.py 파일로 날씨 관련 api 분리 후 가져오기
application.register_blueprint(main_site.main_page)
application.register_blueprint(join_site.join_page)
application.register_blueprint(detail_site.detail_page)
application.register_blueprint(weather.weather_api)

client = MongoClient(account.API_KEY)
db = client.Haromony


SECRET_KEY = 'test'



@application.route('/profile/<userid>')
def profile(userid):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (userid == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
        user_info = db.users.find_one({"user_id": userid}, {"_id": False})
        return render_template('profile.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))

@application.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        name_receive = request.form["name_give"]
        about_receive = request.form["about_give"]
        new_doc = {
            "profile_name": name_receive,
            "profile_info": about_receive
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        print(payload['id'])
        db.users.update_one({'user_id': payload['id']}, {'$set': new_doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        print('image save fail')
        return redirect(url_for("home"))


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
