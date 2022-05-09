import jwt
from flask import Flask, render_template, jsonify, request, Blueprint, url_for, redirect

application = Flask(__name__)

from pymongo import MongoClient
from DB_ADMIN import account

client = MongoClient(account.API_KEY)
db = client.Haromony
news = client.news_data
SECRET_KEY = 'test'
detail = Blueprint('detail', __name__)


@detail.route("/detail/<post_id>")
def detail_load(post_id):
    post = news.news_data.find_one({'post_id': int(post_id)}, {'_id': False})
    return render_template('detail.html', post=post)


# 댓글 작성
# @detail.route('/comments', methods=['POST'])
# def save_comment():
#     """
#     댓글 작성 정보(사용자 ID, 기사 ID, 내용, 작성 시간)를 comments 컬렉션에 저장
#     :return:확인 메시지
#     """
#     comment_name_receive = request.form['comment_name_give']
#     comment_content_receive = request.form['comment_give']
#     time_receive = request.form['time_give']
#
#     doc = {
#         'comment_name': comment_name_receive,
#         'comment_content': comment_content_receive,
#         'time': time_receive
#     }
#     db.comments.insert_one(doc)
#     return jsonify({'msg': '작성 완료!'})


# @detail.route('/like_update', methods=['POST'])
# def like_update():
#     """ -yj
#     좋아요
#     :return:확인 메시지
#     """
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"user_id": payload["id"]})
#         comment_id_receive = request.form["comment_id_give"]
#         action_receive = request.form["action_give"]
#         doc = {
#             "like_comment_id": comment_id_receive,
#             "user_id": user_info["user_id"]
#         }
#         if action_receive == "like":
#             db.users.insert_one(doc)
#         else:
#             db.users.delete_one(doc)
#         count = db.users.count_documents({"like_comment_id": comment_id_receive})
#         return jsonify({"result": "success", 'msg': 'updated', "count": count})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))
#
#
# @detail.route('/bookmark', methods=['POST'])
# def bookmark():
#     """ -yj
#     북마크
#     :return:확인 메시지
#     """
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"user_id": payload["id"]})
#         post_id_receive = request.form["post_id_give"]
#         action_receive = request.form["action_give"]
#         doc = {
#             "bookmark_post_id": post_id_receive,
#             "user_id": user_info["user_id"]
#         }
#         if action_receive == "bookmark":
#             db.users.insert_one(doc)
#         else:
#             db.users.delete_one(doc)
#         return jsonify({"result": "success", 'msg': 'updated'})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))
#
#
# @detail.route('/comments_get', methods=['GET'])
# def comments_get():
#     """ -yj
#     DB의 comments 컬렉션에서 댓글 정보 리스트를 최근 시간 순으로 가져오기
#     :return: 댓글 리스트
#     """
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"username": payload["id"]})
#         # 매개변수로 받은 user_id 유무에 따라 find 조건 걸어주기
#         user_id_receive = request.args.get("user_id_give")
#         if user_id_receive=="":
#             comments = list(db.comments.find({}).sort("date", -1).limit(20))
#         else:
#             comments = list(db.comments.find({"user_id": user_id_receive}).sort("date", -1).limit(20))
#         # 좋아요 갯수
#         for comment in comments:
#             comment["_id"] = str(comments["_id"])
#             comment["count_like"] = db.users.count_documents({"like_comment_id": comment["_id"]})
#             comment["like_by_me"] = bool(db.users.find_one({"like_comment_id": comment["_id"], "user_id": user_info}))
#         return jsonify({"result": "success", "msg": "comments_get", "comments": comments})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


# get_news() 랑 합칠건지? -yj
# @detail.route('/posts_get', methods=['GET'])
# def posts_get():
#     """ -yj
#     DB의 news_data 컬렉션에서 북마크한 기사 리스트를 최근 시간 순으로 가져오기
#     :return: 댓글 리스트
#     """
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"username": payload["id"]})
#         # 매개변수로 받은 user_id가 북마크한 기사 ID를 찾아서 해당 기사들만 가져오기
#         user_id_receive = request.args.get("user_id_give")
#         bookmark_post_id = list(db.users.find({"user_id": user_id_receive}, {"_id": 0, "bookmark_post_id": 1}).sort("date", -1).limit(20))
#         # 이거 리스트로 북마크한 기사 ID 반복문 돌려서 각 id마다 뉴스데이터에서 일치하는거 가져와야함...밑에처럼 바로 가면 안될듯
#
#         bookmarked_posts = list(news.find({"post_id": bookmark_post_id}, {"_id": 0}).sort("date", -1).limit(20))
#         # 좋아요 갯수
#         for comment in comments:
#             comment["_id"] = str(comments["_id"])
#             comment["count_like"] = db.users.count_documents({"like_comment_id": comment["_id"]})
#             comment["like_by_me"] = bool(db.users.find_one({"like_comment_id": comment["_id"], "user_id": user_info}))
#         return jsonify({"result": "success", "msg": "comments_get", "bookmarked_posts": bookmarked_posts})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)