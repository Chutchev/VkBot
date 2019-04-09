import requests
import os
from dotenv import load_dotenv
import pprint
import random
VERSION_API = 5.92


#TODO Изменить метод UNAUTHORIZED for url
#def get_users_dm(access_token):
#    url = 'https://discordapp.com/api/users/@me/channels'
#    header = {'Authorization': 'Bearer {}'.format(access_token)}
#    response = requests.get(url, headers=header)
#    response.raise_for_status()
#    pprint.pprint(response.json())
#    return response.json()


def get_user_object(access_token):
    url = 'https://discordapp.com/api/users/@me'
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(url, headers=header)
    response.raise_for_status()
    pprint.pprint(response.json())
    return response.json()


def get_discord_access_token(client_id, client_secret, redirect_uri, code):
    data = {
        'client_id': int(client_id),
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'gdm.join messages.read identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('https://discordapp.com/api/oauth2/token', data, headers)
    pprint.pprint(r.json())
    return r.json()


def get_longpoll_server(access_token, group_id):
    url = "https://api.vk.com/method/groups.getLongPollServer"
    params = {'group_id': group_id,
              'access_token': access_token,
              'v': VERSION_API,
              }
    response = requests.get(url, params=params)
    pprint.pprint(response.json())
    return response.json()['response']['key'], response.json()['response']['server'], response.json()['response']['ts']


def send_message(message: str,  group_id: str, access_token, domain: str, attachment=None, user_id: int=0, ):
    url = "https://api.vk.com/method/messages.send"
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
    response = requests.get(url, params=params)
    return response.json(), response.url


def main():
    load_dotenv(".env")
    vk_token = os.getenv('vk_token')
    vk_group_token = os.getenv('vk_group_token')
    vk_group_id = os.getenv('vk_group_id')
    discord_client_id = os.getenv('discord_client_id')
    discord_client_secret = os.getenv('discord_client_secret_token')
    discord_code = os.getenv('discord_code')
    redirect_uri = 'https://discordapp.com/api/oauth2/token'
    #answer = send_message("Тест", vk_group_id, vk_group_token, domain='chutchevv')
    access_token_answer = get_discord_access_token(discord_client_id, discord_client_secret, redirect_uri, discord_code)
    user_object = get_user_object(access_token_answer['access_token'])
    #users_dm = get_users_dm(access_token_answer['access_token'])
    #key, server, ts = get_longpoll_server(vk_group_token, vk_group_id)
    #pprint.pprint(answer)


if __name__ == '__main__':
    main()
