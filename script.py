import requests
import os
from dotenv import load_dotenv
import pprint
import random
VERSION_API = 5.92


def get_longpoll_server(access_token, group_id):
    url = "https://api.vk.com/method/groups.getLongPollServer"
    params = {'group_id': group_id,
              'access_token': access_token,
              'v': VERSION_API,
              }
    response = requests.get(url, params=params)
    print(response.url)
    pprint.pprint(response.json())
    return response.json()['response']['key'], response.json()['response']['server'], response.json()['response']['ts']


def send_message(message: str,  group_id: str, access_token, domain: str, attachment=None, user_id: int=0, ):
    url = "https://api.vk.com/method/messages.send"
    print(domain)
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
    if user_id != 0 and domain is None:
        params['user_id'] = user_id
    else:
        params['domain'] = domain
    pprint.pprint(params)
    response = requests.get(url, params=params)
    return response.json(), response.url


def main():
    load_dotenv(".env")
    vk_token = os.getenv('vk_token')
    vk_group_token = os.getenv('vk_group_token')
    vk_group_id = os.getenv('vk_group_id')
    answer = send_message("Тест", vk_group_id, vk_group_token, domain='')
    key, server, ts = get_longpoll_server(vk_group_token, vk_group_id)
    pprint.pprint(answer)

if __name__ == '__main__':
    main()
