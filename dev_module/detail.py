import jwt
from flask import Flask, render_template, jsonify, request, Blueprint

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
    return render_template('detail.html', post=post)


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

    db.comment.insert_one(doc)
    return jsonify({'msg': '의견이 정상적으로 등록되었습니다.'})


if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)