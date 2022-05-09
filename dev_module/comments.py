from flask import Flask, render_template, jsonify, request, Blueprint
import jwt
from pymongo import MongoClient
from DB_ADMIN import account

app = Flask(__name__)


client = MongoClient(account.API_KEY)
db = client.Haromony
comments = Blueprint('comments', __name__)

SECRET_KEY = 'test'


@comments.route("/comments")
def comments_load():
    return render_template('new_comment.html')


@comments.route('/comment', methods=['POST'])
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


@comments.route('/api/comment', methods=['GET'])
def view_comments():
    """
    DB의 comments 컬렉션에서 댓글 작성 정보 리스트를 최근 시간 순으로 가져오기
    :return: 댓글 작성 리스트
    """
    comments = list(db.comments.find({}, {'_id': False}).sort('time', -1))
    return jsonify({'comments': comments})


@comments.route('/api/like', methods=['POST'])
def plus_like():
    """
    화면에 출력되는 like 값을 가져옴
    like 컬렉션이 존재하면 기존의 like 값에 1 추가해서 기존 값과 교체
    like 컬렉션이 존재하지 않으면 새 값 입력
    :return:확인 메시지
    """
    like_receive = request.form['like_give']
    like_check = db.like.find_one({})
    if like_check is not None:
        current_like = like_check['like']
        plus_like = int(current_like) + 1
        db.like.update_one({}, {'$set': {'like': plus_like}})
    else:
        plus_like = int(like_receive) + 1
        doc = {
            'like': plus_like
        }
        db.like.insert_one(doc)

    return jsonify({'msg': '좋아요 완료!'})


@comments.route('/api/like', methods=['GET'])
def show_likes():
    """
    DB의 like 컬렉션에서 좋아요 수 가져오기
    :return: 좋아요 수
    """
    new_like = db.like.find_one({}, {'_id': False})['like']
    return jsonify({'new_like': new_like})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)