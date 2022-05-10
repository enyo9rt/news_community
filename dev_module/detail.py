import jwt
from flask import Flask, render_template, jsonify, request, Blueprint, url_for, redirect

application = Flask(__name__)

from pymongo import MongoClient
from DB_ADMIN import account

client = MongoClient(account.API_KEY)
db = client.Haromony
news = client.news_data.news_data
SECRET_KEY = 'test'
detail = Blueprint('detail', __name__)


@detail.route("/detail/<post_id>")
def detail_load(post_id):
    post = news.find_one({'post_id': int(post_id)}, {'_id': False})
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        status = True
        return render_template('detail.html', post=post, status=status, user_info=user_info)
    except :
        status = False
        return render_template('index.html', status=status)


# -hj
@detail.route('/comment', methods=['POST'])
def save_comment():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})

    comment_receive = request.form['comment_give']
    date_receive = request.form["date_give"]

    doc = {
        "comment": comment_receive,
        "user_id": user_info['id'],
        "date": date_receive
    }

    db.comments.insert_one(doc)
    return jsonify({'msg': '의견이 정상적으로 등록되었습니다.'})


@detail.route('/like_update', methods=['POST'])
def like_update():
    """ -yj
    좋아요
    :return:확인 메시지
    """
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = payload["id"]
        comment_id_receive = request.form["comment_id_give"]
        action_receive = request.form["action_give"]
        doc = {
            "like_comment_id": comment_id_receive,
            "user_id": user_info
        }
        if action_receive == "like":
            db.action.insert_one(doc)
        else:
            db.action.delete_one(doc)
        count = db.action.count_documents({"like_comment_id": comment_id_receive})
        print(count)
        return jsonify({"result": "success", "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@detail.route('/bookmark', methods=['POST'])
def bookmark():
    """ -yj
    북마크
    :return:확인 메시지
    """
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = payload["id"]
        post_id_receive = request.form["post_id_give"]
        action_receive = request.form["action_give"]
        doc = {
            "bookmark_post_id": post_id_receive,
            "user_id": user_info
        }
        if action_receive == "bookmark":
            db.action.insert_one(doc)
        else:
            db.action.delete_one(doc)
        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@detail.route('/comments_get', methods=['GET'])
def comments_get():
    """ -yj
    DB의 comments 컬렉션에서 댓글 정보 리스트를 최근 시간 순으로 가져오기
    :return: 댓글 리스트
    """
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = payload["id"]
        # 매개변수로 받은 user_id 유무에 따라 find 조건 걸어주기
        user_id_receive = request.args.get("user_id_give")
        post_id_receive = request.args.get("post_id_give")
        # user_id가 없으면 post_id와 매칭되는 댓글 가져오기
        if user_id_receive=="":
            comments = list(db.comments.find({"post_id": post_id_receive}).sort("date", -1).limit(20))
        else:
            comments = list(db.comments.find({"user_id": user_id_receive}).sort("date", -1).limit(20))
        for comment in comments:
            comment["_id"] = str(comment["_id"])
            # 좋아요 갯수, 여부 확인
            comment["count_like"] = db.action.count_documents({"like_comment_id": comment["_id"]})
            comment["like_by_me"] = bool(db.action.find_one({"like_comment_id": comment["_id"], "user_id": user_info}))
        return jsonify({"result": "success", "msg": "comments_get", "comments": comments})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@detail.route('/bookmarked', methods=['GET'])
def bookmarked():
    """ -yj
    북마크 여부 확인
    :return:
    """
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = payload["id"]
        # 매개변수로 받은 user_id 유무에 따라 find 조건 걸어주기
        post_id_receive = request.args.get("post_id_give")
        bookmark_by_me = bool(db.action.find_one({"bookmark_post_id": post_id_receive, "user_id": user_info}))
        return jsonify({"result": "success", "bookmark_by_me": bookmark_by_me})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)