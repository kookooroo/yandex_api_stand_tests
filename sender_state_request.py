import requests
import config, data

def post_new_user(body):
    return requests.post(config.URL_SERVICE + config.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def get_users_table():
    return requests.get(config.URL_SERVICE + config.USERS_TABLE_PATH)