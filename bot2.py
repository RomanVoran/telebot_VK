# бот просто отвечает на все ссобщени пользователя

import requests
from time import sleep


token = '258667681:AAGpgdlD_jepb2wlZpF9Zm3MWIq4KYO6_YY'
url = "https://api.telegram.org/bot" + token + "/"


def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

print(last_update(get_updates_json(url)))

def main():
    i = 0
    lu = last_update(get_updates_json(url));
    update_id = lu['update_id']
    while True:
        lu = last_update(get_updates_json(url));
        if update_id == lu['update_id']:
            print(i)
            i = i + 1
            first_name = lu['message']['from']['first_name']
            last_name = lu['message']['from']['last_name']
            send_mess(get_chat_id(lu), 'Ответ на сообщение: "' + lu['message']['text'] + '" от: ' + first_name + ' ' +last_name )
            update_id += 1
        #sleep(0.25)

if __name__ == '__main__':
    main()