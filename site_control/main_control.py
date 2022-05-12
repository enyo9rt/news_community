from flask import render_template, request
from CONFIG.account import SECRET_KEY
from model.mongo import UserAdmin
import jwt


def home_render():
    msg = request.args.get("msg")
    token_receive = request.cookies.get('mytoken')  # 클라이언트로부터 mytoekn에 담겨 온 토큰 정보 받아주기
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # db.users.find_one({"user_id": test})을 의미화
        user_info = UserAdmin.users_find_one("user_id", payload["id"])
        status = True
        return render_template('index.html', status=status, user_info=user_info)
    except :
        status = False
        return render_template('index.html', status=status, msg=msg)