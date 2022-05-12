from site_view import main_site, join_site, detail_site, profile_site
from flask import Flask
from dev_module import weather



application = Flask(__name__)
application.register_blueprint(main_site.main_page)
application.register_blueprint(join_site.join_page)
application.register_blueprint(detail_site.detail_page)
application.register_blueprint(weather.weather_api)
application.register_blueprint(profile_site.profile_page)

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000, debug=True)
