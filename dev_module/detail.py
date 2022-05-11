import jwt
from flask import Flask, render_template, jsonify, request, Blueprint, url_for, redirect


application = Flask(__name__)

from pymongo import MongoClient
from DB_ADMIN import account

from operator import itemgetter

client = MongoClient(account.API_KEY)
db = client.Haromony
news = client.news_data.news_data
SECRET_KEY = 'test'
detail = Blueprint('detail', __name__)


@detail.route("/detail/<post_id>")
def detail_load(post_id):
    post = news.find_one({'post_id': int(post_id)}, {'_id': False})
    comment_count = db.comments.count_documents({'post_id': post_id})
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["id"]})
        status = True
        return render_template('detail.html', post=post, status=status, user_info=user_info, comment_count=comment_count)
    except:
        status = False
        return redirect(url_for("home", msg="로그인을 해주세요!"))


@detail.route('/comment', methods=['POST'])
def save_comment():
    # 토큰으로 유저 정보 가져오기
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"user_id": payload["id"]})
    print(user_info)

    # 클라이언트로부터 데이터 받아오기
    comment_receive = request.form['comment_give']
    date_receive = request.form["date_give"]
    id_receive = request.form["id_give"]

    comment_count = db.comments.estimated_document_count()

    if comment_count == 0:
        max_value = 1
    else:
        max_value = db.comments.find_one(sort=[("idx", -1)])['idx'] + 1

    doc = {
        "comment": comment_receive,
        "user_id": user_info['user_id'],
        "nick_name": user_info['nick_name'],
        "date": date_receive,
        "profile_pic_real": user_info['profile_pic_real'],
        "post_id": id_receive,
        "idx": max_value
    }

    db.comments.insert_one(doc)
    return jsonify({'msg': '의견이 정상적으로 등록되었습니다.'})


@detail.route('/comment/delete', methods=['POST'])
def delete_comment():
    comment_idx_receive = request.form['comment_idx_give']
    db.comments.delete_one({'idx': int(comment_idx_receive)})
    return jsonify({'msg': '의견이 삭제 되었습니다.'})


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
        sorting_status_receive = request.args.get("sorting_status_give")
        # user_id가 없으면 post_id와 매칭되는 댓글 가져오기
        print("sorting_status_receive 받았고, 변환함", sorting_status_receive)
        if user_id_receive == "":
            comments = list(db.comments.find({"post_id": post_id_receive}).sort("date", -1).limit(20))
        else:
            comments = list(db.comments.find({"user_id": user_id_receive}).sort("date", -1).limit(20))

        for comment in comments:
            comment["_id"] = str(comment["_id"])
            # 좋아요 갯수, 여부 확인
            comment["count_like"] = db.action.count_documents({"like_comment_id": comment["_id"]})
            comment["like_by_me"] = bool(db.action.find_one({"like_comment_id": comment["_id"], "user_id": user_info}))

        # 정렬
        if sorting_status_receive == "new":
            comments = sorted(comments, key=itemgetter('date'), reverse=True)
        elif sorting_status_receive == "old":
            comments = sorted(comments, key=itemgetter('date'))
        elif sorting_status_receive == "like":
            comments = sorted(comments, key=itemgetter('count_like', 'date'), reverse=True)

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


@detail.route('/posts_get', methods=['GET'])
def posts_get():
    """ -yj
    DB의 news_data 컬렉션에서 북마크한 기사 리스트를 최근 시간 순으로 가져오기
    :return: 댓글 리스트
    """
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 매개변수로 받은 user_id가 북마크한 기사 ID를 찾아서 해당 기사들만 가져오기
        user_id_receive = request.args.get("user_id_give")
        bookmark_post_ids = list(db.action.find({"user_id": user_id_receive}, {"_id": 0, "bookmark_post_id": 1}).sort("date", -1).limit(20))
        bookmarked_posts = []
        for r in bookmark_post_ids:
            if r:
                r["bookmark_post_id"] = int(r["bookmark_post_id"])
                bookmarked_posts.append(news.find_one({"post_id": r["bookmark_post_id"]}, {"_id": 0}))
        return jsonify({"result": "success", "msg": "posts_get", "posts": bookmarked_posts})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)