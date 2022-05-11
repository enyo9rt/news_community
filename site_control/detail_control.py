from flask import render_template, request, jsonify, redirect, url_for
from CONFIG.account import SECRET_KEY
from model.mongo import UserAdmin, DetailContents
from operator import itemgetter
import jwt


class DetailControl():
    @staticmethod
    def detail_render(post_id):
        post = DetailContents.find_post(post_id)
        count_comments = DetailContents.count_comments(post_id)
        token_receive = request.cookies.get('mytoken')  # 클라이언트로부터 mytoekn에 담겨 온 토큰 정보 받아주기
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = UserAdmin.users_find_one("user_id", payload["id"])
            status = True
            return render_template('detail.html', post=post, status=status, user_info=user_info, count_comments=count_comments)
        except :
            status = False
            return render_template('index.html', msg="로그인을 해주세요!")

    @staticmethod
    def save_comment(comment_receive, date_receive, id_receive):
        # 토큰으로 유저 정보 가져오기
        token_receive = request.cookies.get('mytoken')
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = UserAdmin.users_find_one({"user_id": payload["id"]})

        if DetailContents.count_all_comments == 0:
            max_value = 1
        else:
            max_value = DetailContents.plus_comment_id()

        doc = {
            "comment": comment_receive,
            "user_id": user_info['user_id'],
            "nick_name": user_info['nick_name'],
            "date": date_receive,
            "profile_pic_real": user_info['profile_pic_real'],
            "post_id": id_receive,
            "idx": max_value
        }

        DetailContents.insert_comment(doc)
        return jsonify({'msg': '의견이 정상적으로 등록되었습니다.'})

    @staticmethod
    def delete_comment(comment_idx_receive):
        DetailContents.delete_comment(comment_idx_receive)
        return jsonify({'msg': '의견이 삭제 되었습니다.'})

    @staticmethod
    def like_update(comment_id_receive, action_receive):
        """ -yj
        좋아요
        :return:확인 메시지
        """
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = payload["id"]
            doc = {
                "like_comment_id": comment_id_receive,
                "user_id": user_info
            }
            if action_receive == "like":
                DetailContents.insert_action(doc)
            else:
                DetailContents.delete_action(doc)
            count = DetailContents.count_like(comment_id_receive)
            return jsonify({"result": "success", "count": count})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))

    @staticmethod
    def bookmark(post_id_receive, action_receive):
        """ -yj
        북마크
        :return:확인 메시지
        """
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = payload["id"]
            doc = {
                "bookmark_post_id": post_id_receive,
                "user_id": user_info
            }
            if action_receive == "bookmark":
                DetailContents.insert_action(doc)
            else:
                DetailContents.delete_action(doc)
            return jsonify({"result": "success"})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))

    @staticmethod
    def comments_get(user_id_receive, post_id_receive, sorting_status_receive):
        """ -yj
        DB의 comments 컬렉션에서 댓글 정보 리스트를 최근 시간 순으로 가져오기
        :return: 댓글 리스트
        """
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = payload["id"]

            # user_id가 없으면 post_id와 매칭되는 댓글 가져오기
            if user_id_receive == "":
                comments = list(DetailContents.find_comments("post_id", post_id_receive).sort("date", -1).limit(20))
            else:
                comments = list(DetailContents.find_comments("user_id", user_id_receive).sort("date", -1).limit(20))

            for comment in comments:
                comment["_id"] = str(comment["_id"])
                # 좋아요 갯수, 여부 확인
                comment["count_like"] = DetailContents.count_like(comment["_id"])
                comment["like_by_me"] = bool(DetailContents.like_by_me("like_comment_id", comment["_id"], user_info))

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

    @staticmethod
    def bookmarked(post_id_receive):
        """ -yj
        북마크 여부 확인
        :return:
        """
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = payload["id"]
            # 매개변수로 받은 user_id 유무에 따라 find 조건 걸어주기
            bookmark_by_me = bool(DetailContents.like_by_me("bookmark_post_id", post_id_receive, user_info))
            return jsonify({"result": "success", "bookmark_by_me": bookmark_by_me})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))

    @staticmethod
    def posts_get(user_id_receive):
        """ -yj
        DB의 news_data 컬렉션에서 북마크한 기사 리스트를 최근 시간 순으로 가져오기
        :return: 댓글 리스트
        """
        token_receive = request.cookies.get('mytoken')
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            # 매개변수로 받은 user_id가 북마크한 기사 ID를 찾아서 해당 기사들만 가져오기
            bookmark_post_ids = list(DetailContents.find_bookmark_post(user_id_receive).sort("date", -1).limit(20))
            bookmarked_posts = []
            for r in bookmark_post_ids:
                if r:
                    r["bookmark_post_id"] = int(r["bookmark_post_id"])
                    bookmarked_posts.append(DetailContents.find_post(r["bookmark_post_id"]))
            return jsonify({"result": "success", "msg": "posts_get", "posts": bookmarked_posts.reverse()})
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("home"))