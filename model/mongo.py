from pymongo import MongoClient
from CONFIG.account import API_KEY

client = MongoClient(API_KEY)
db = client.Haromony


class DBAdmin():
    @staticmethod
    def get_mongo_connector():
        return db


class UserAdmin():
    @staticmethod
    def users_find_one(column, target):   # main_control, join_control에서 사용
        return db.users.find_one({column: target})

    @staticmethod
    def is_customer_check(user_id, pw_hash):  # join_control: checkdup()에 사용
        return db.users.find_one({'user_id': user_id, 'password': pw_hash})

    @staticmethod
    def user_signup_db(doc): # join_control에 사용
        db.users.insert_one(doc)

    @staticmethod
    def users_update_one(payload_id, new_doc):
        return db.users.update_one({'user_id': payload_id}, {'$set': new_doc})
