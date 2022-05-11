from flask import Blueprint, jsonify
from dev_module import news_getter
from site_control import main_control


main_page = Blueprint('main', __name__)


@main_page.route('/')
def home():
    return main_control.home_render()

@main_page.route("/news", methods=["GET"])
def news_get():
    news_list = news_getter.get_news()
    return jsonify({'news_list': news_list})
