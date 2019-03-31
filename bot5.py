import config
import telebot
import requests
import threading
import time


token = '258667681:AAGpgdlD_jepb2wlZpF9Zm3MWIq4KYO6_YY'
url = "https://api.telegram.org/bot" + token + "/"
tokenVK = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'
g_id = 69930438  #
allUsersId = [] # массив id всех чатов с которыми переговаривается бот
bot = telebot.TeleBot(config.API_TOKEN)
#bot = telebot.TeleBot(config.API_TOKEN, threaded=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	send_message = 'Этот бот делает бла бла блааа....'
	bot.send_message(chat_id=message.chat.id, text=send_message)



@bot.message_handler(func=lambda message: True)
def echo_all(message):
	send_message = 'Ответ на сообщение "' + str(message.text) + '".'
	bot.send_message(chat_id=message.chat.id, text=send_message)


def polling_function_threading():
	print('BOT поток')
	bot.polling(none_stop=True)
	pass


def vk_function_threading():
	print('VK поток')
	while True:
		time.sleep(4)
		print('Вк всё ещё работает')
	pass



class myThread (threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter
    def run(self):
        print_date(self.name, self.counter)

def print_date(threadName, counter):
	if counter==1:
		vk_function_threading()
	else:
		polling_function_threading()




bot = telebot.TeleBot(config.API_TOKEN)

# Создание новой нити
thread1 = myThread("VK", 1)
thread2 = myThread("BOT", 2)

# Запуск новой нити
thread1.start()
thread2.start()

thread1.join()
thread2.join()
