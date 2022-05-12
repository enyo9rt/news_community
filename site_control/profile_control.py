from flask import render_template, request, jsonify, redirect, url_for
from model.mongo import UserAdmin
from werkzeug.utils import secure_filename
from model.mongo import DetailContents
from dev_module.xss_protect import xss_protect
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
                "nick_name": xss_protect.stop_code_filter(name_receive),
                "profile_info": xss_protect.stop_code_filter(about_receive)
            }
            if 'file_give' in request.files:
                file = request.files["file_give"]
                filename = secure_filename(file.filename)
                extension = filename.split(".")[-1]
                file_path = f"profile_pics/{username}.{extension}"
                file.save("./static/" + file_path)
                new_doc["profile_pic"] = filename
                new_doc["profile_pic_real"] = file_path
            else:
                filename = 'profile_placeholder.png'
                file_path = 'profile_pics/profile_placeholder.png'
                new_doc["profile_pic"] = filename
                new_doc["profile_pic_real"] = file_path

            UserAdmin.users_update_one(payload['id'], new_doc)
            return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))

    @staticmethod
    def posts_get(user_id_receive):
        """ -yj
        DB의 news_data 컬렉션에서 북마크한 기사 리스트를 최근 시간 순으로 가져오기
        :return: 댓글 리스트
        """
        try:
            # 매개변수로 받은 user_id가 북마크한 기사 ID를 찾아서 해당 기사들만 가져오기
            bookmark_post_ids = list(DetailContents.find_bookmark_post(user_id_receive).sort("date", -1).limit(20))
            bookmarked_posts = []
            for r in bookmark_post_ids:
                if r:
                    bookmarked_posts.append(DetailContents.find_post(r["bookmark_post_id"]))
            return jsonify({"result": "success", "msg": "posts_get", "posts": bookmarked_posts})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))

