from pymongo import MongoClient
from DB_ADMIN import account

client = MongoClient(account.API_KEY)
db = client.news_data

def get_news():
    '''
    네이버 뉴스에서 제목과 내용 가져와서, app.py의 news_get라우터 함수에 리턴
    :param: None
    :return: 문자열 리스트
    '''
    try:
        news_box = list(db.news_data.find({}, {'_id': False}).limit(20).sort([("post_id", -1)]))
        # print(news_box)
        return news_box

    except:
        return []
