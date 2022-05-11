from flask import render_template, request, jsonify, redirect, url_for
from model.mongo import UserAdmin
from werkzeug.utils import secure_filename
import jwt

SECRET_KEY = 'test'


class ProfileHandler:
    @staticmethod
    def profile_render(token, userid):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            status = (userid == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False
            user_info = UserAdmin.users_find_one('user_id', userid)
            return render_template('profile.html', user_info=user_info, status=status)
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("/"))

    @staticmethod
    def change_img(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
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
                file.save("./static/" + file_path)
                new_doc["profile_pic"] = filename
                new_doc["profile_pic_real"] = file_path
            print(payload['id'])
            UserAdmin.users_update_one(payload['id'], new_doc)
            return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            print('image save fail')
            return redirect(url_for("home"))


