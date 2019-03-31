import requests
from time import sleep


token = '258667681:AAGpgdlD_jepb2wlZpF9Zm3MWIq4KYO6_YY'
url = "https://api.telegram.org/bot" + token + "/"


def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()


def last_update(data):
    results = data['result']
    print(results)
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

chat_id = get_chat_id(last_update(get_updates_json(url)))
send_mess(chat_id, 'отвечаю на сообщение')


gg = last_update(get_updates_json(url))
print()
print(gg)
print()
print()
print(chat_id)
print()
print()
print(gg['message']['text'])
