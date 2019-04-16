import requests
import os
from dotenv import load_dotenv
import pprint
import random
import DB
from time import sleep
BASE_URL_VK = 'https://api.vk.com/method/'
VERSION_API = 5.95


def get_user_object(user_id, access_token):
    url = f'{BASE_URL_VK}users.get'
    params = {'user_ids': user_id,
              'access_token': access_token,
              'v': VERSION_API}
    response = requests.get(url, params=params)
    return response.json()


def join_longpoll_server(server, key, ts):
    url = f'{server}?act=a_check&key={key}&ts={ts}&wait=25'
    response = requests.get(url)
    pprint.pprint(response.json())
    return response.json()['ts'], response.json()


def get_longpoll_server(access_token, group_id):
    url = f"{BASE_URL_VK}groups.getLongPollServer"
    params = {'group_id': group_id,
              'access_token': access_token,
              'v': VERSION_API,
              }
    response = requests.get(url, params=params)
    print('Подключено')
    return response.json()['response']['key'], response.json()['response']['server'], response.json()['response']['ts']


def send_message(message: str,  group_id: str, access_token, domain: str = '', attachment=None, user_id: int=0, ):
    url = f"{BASE_URL_VK}messages.send"
    if attachment is None:
        params = {'message': message,
                  'random_id': random.randint(1, 100000000),
                  'group_id': group_id,
                  'access_token': access_token,
                  'v': VERSION_API}
    else:
        params = {'message': message,
                  'random_id': random.randint(1, 100000000),
                  'group_id': group_id,
                  'attachment': attachment,
                  'access_token': access_token,
                  'v': VERSION_API}
    if user_id != 0:
        params['user_id'] = user_id
    else:
        params['domain'] = domain
    response = requests.get(url, params=params)
    return response.json(), response.url


def main():
    load_dotenv(".env")
    vk_group_token = os.getenv('vk_group_token')
    vk_group_id = os.getenv('vk_group_id')
    key, server, ts = get_longpoll_server(vk_group_token, vk_group_id)
    ts, answer = join_longpoll_server(server, key, ts)
    try:
        answer_message = send_message("Приветствую Вас! Продолжайте в том же духе. Напиши как к вам обращаться",
                                      vk_group_id, vk_group_token,
                                      user_id=int(answer['updates'][0]['object']['user_id']))
    except KeyError:
        pass
    while True:
        ts, answer = join_longpoll_server(server, key, ts)
        try:
            data = answer['updates'][0]['object']
            user = get_user_object(data['peer_id'], vk_group_token)
            user = user['response'][0]
            if answer['updates'][0]['type'] == 'message_new':
                message = data['text']
                DB.insert_DB(user, message)
            nickname = DB.select_DB(user)
            answer_message = send_message(
                f"{nickname[3]}, вы молодец! Продолжайте в том же духе. Напиши как к вам обращаться",
                vk_group_id, vk_group_token,
                user_id=int(data['from_id']))
        except IndexError:
            pass


if __name__ == '__main__':
    main()
