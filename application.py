from site_view import main_site, join_site, detail_site, profile_site
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from dev_module import weather
from CONFIG import account


application = Flask(__name__)
application.register_blueprint(main_site.main_page)
application.register_blueprint(join_site.join_page)
application.register_blueprint(detail_site.detail_page)
application.register_blueprint(weather.weather_api)
application.register_blueprint(profile_site.profile_page)

client = MongoClient(account.API_KEY)
db = client.Haromony

SECRET_KEY = 'test'

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
