from flask import Flask, render_template, jsonify, request, Blueprint

app = Flask(__name__)

from pymongo import MongoClient
from DB_ADMIN import account

client = MongoClient(account.API_KEY)
db = client.Haromony
comments = Blueprint('comments', __name__)


@comments.route("/comments")
def comments_load():
    return render_template('comments.html')

@comments.route('/api/comment', methods=['POST'])
def save_comment():
    """
    댓글 작성 정보(닉네임, 내용, 작성 시간)를 comments 컬렉션에 저장
    :return:확인 메시지
    """
    comment_name_receive = request.form['comment_name_give']
    comment_content_receive = request.form['comment_give']
    time_receive = request.form['time_give']

    doc = {
        'comment_name': comment_name_receive,
        'comment_content': comment_content_receive,
        'time': time_receive
    }
    db.comments.insert_one(doc)
    return jsonify({'msg': '작성 완료!'})

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