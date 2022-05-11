from flask import request, Blueprint
from site_control.profile_control import ProfileHandler

SECRET_KEY = 'test'

profile_page = Blueprint('profile', __name__)


# 각 사용자의 프로필과 글을 모아볼 수 있는 공간
@profile_page.route('/profile/<userid>')
def profile(userid):
    token_receive = request.cookies.get('mytoken')
    return ProfileHandler.profile_render(token_receive, userid)


# 사용자의 프로필 이미지 바꿀 수 있는 기능
@profile_page.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    return ProfileHandler.change_img(token_receive)


# 프로필 페이지에서 사용자가 북마크한 기사만 모아보기
@profile_page.route('/profile/<userid>')
def show_bookmark(userid):
    return ProfileHandler.posts_get(userid)
