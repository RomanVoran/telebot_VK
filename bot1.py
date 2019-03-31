import config
import telebot
import requests
import threading
import time


#tokenTB = '258667681:AAGpgdlD_jepb2wlZpF9Zm3MWIq4KYO6_YY'
url = "https://api.telegram.org/bot" + config.tokenTB + "/"
tokenVK = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'
allUsersId = [] # массив id всех чатов с которыми переговаривается бот
#bot = telebot.TeleBot(config.API_TOKEN)
bot = telebot.TeleBot(config.tokenTB, threaded=False)



def vkGetMembers(token, g_id):
    offset = 0  # отступ при считывании списка
    method = 'groups.getMembers'  # выполняемый метод
    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода

    # вектор параметров запроса
    params = {'group_id': g_id, 'offset': offset}

    # выполнение запроса к VK для получения нужной информации
    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + token, params)
    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
    ######################################################################
    # применительно к выполняемой задаче:

    count = response['response']['count']  # количество подписчиков в группе
    count_offset = round(count // 1000)  # количество тысяч в числе count с округлением в меньшую сторону
    print('количество тыс. подписчиков',count_offset)

    i = 0
    followers = []
    while offset/1000 <= count_offset:
        # потысячное получение подписчиков группы
        params = {'group_id': g_id, 'offset': offset}
        r = requests.get(vk_URL + method + '?v=5.8&access_token=' + token, params)
        response = r.json()
        followers.extend(response['response']['users'])  # добавление полученной тысячи подписчиков в общий массив
        offset = offset + 1000  # сдвиг на 1000
        time.sleep(0.1)
        print(offset/1000,'тыс. обработано...')
    return followers

def isActiveGroup(tokenVK,group_id):
    # функция принимает на вход токен приложения вконтакте и id группы в целочисленном типе или строковом
    # возвращает True : если группа активна
    # возвращает False : если группа забанена или удалена
    # для работы требуется подключить библиотеку "import requests"
    method = 'groups.getById'  # выполняемый метод
    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода
    params = {'group_id': group_id, 'fields': 'name'}
    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + tokenVK, params)
    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
    return not('deactivated' in response['response'][0])

def isGroupExist(token,message):
    # Функция принимает на вход строку, затем если в строке присутствуют круглые скобки, извлекает запись из этих скобок.
    # Если скобок нет или они расположены иным образом относительно друг друга, то выводится сообщение, что принятая
    # команда составлена не корректно. Затем полученную запись вставляет в метод VK.API "groups.getById".
    # В полученном в результате ответа словаре ищется ключ "id". если такого поля нет, то говорится что такой
    # группы не существует. Если поле присутствует, то функция возвращает поле ключа "id" (циферный идентификатор группы ВК)
    start = -1  # индекс начала циферного id (следующий после "[")
    end = -1  # индекс конца циферного id (предидущий после "]")

    for i in range(len(message)): # вычисление индексов
        if message[i] == ')':
            end = i
        elif (message[i] == '(') & (start == -1):
            start = i + 1

    if not((start > 0) & (end > start)):
        return 'ans1'  # код ответа в случае если команда набрана некорректно

    identifier = message[start:end]

    method = 'groups.getById'  # выполняемый метод
    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода
    params = {'group_id': identifier, 'fields': 'name'}
    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + token, params)
    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
    try:
        return response['response'][0]['id']
    except:
        return 'ans2' # код ответа в случае если такой группы не существует




    pass

def getGroupName(tokenVK,group_id):
    # функция принимает на вход токен приложения вконтакте и id группы в целочисленном типе или строковом
    # возвращает имя группы по его id
    # для работы требуется подключить библиотеку "import requests"
    method = 'groups.getById'  # выполняемый метод
    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода
    params = {'group_id': group_id, 'fields': 'name'}
    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + tokenVK, params)
    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
    return response['response'][0]['name']

def getUserInf(token,userVKid_id):
    # функция принимает на вход токен приложения вконтакте и id группы в целочисленном типе или строковом
    # возвращает имя группы по его id
    # для работы требуется подключить библиотеку "import requests"
    method = 'users.get'  # выполняемый метод
    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода
    params = {'group_id': userVKid_id}
    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + tokenVK, params)
    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
    return (str(response['response'][0]['first_name']) +' '+ str(response['response'][0]['last_name']))

def validationMessage(message):
    # функция проверки правильности ввода сообщения о новом id проверяемой группы
    # на вход функция принимает строку соощения
    # возвращает строку "N" в случае если в сообщении содержатся ошибки
    # возвращает строку с "чистым" id группы
    start = -1 # индекс начала циферного id (следующий после "[")
    end = -1   # индекс конца циферного id (предидущий после "]")

    for i in range(len(message)):
        if message[i]==')':
            end = i
        elif (message[i]=='(')&(start==-1):
            start = i+1

    markOfErr = 0# маркер ошибки ввода (если в числе id будт найден нециферный символ)
    message = message[start:end]
    for c in message:
        if not((ord(c)>=48)&(ord(c)<=57)):
            markOfErr = 1
            break
    if message=='':
        markOfErr = 1
    elif (message=='0'): #если числовое значение id меньше нуля
        markOfErr = 1

    if (start>0) & (end>start) & (markOfErr!=1): # проверка на верную расстановку кавычек и то, что в ковычках только цифры
        return message
    else:
        return 'N'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
            'Привет, этот бот будет отсылать тебе оповещения о новых подписчиках интересующих тебя групп социальной сети Вконтакте.\n'
            'Ниже представлены команды для работы с ботом.\n\n'
            '*setid(####)* - добавляет id группы в ваш список.\n'
            'Например: "*setid(smmbro)*".\n\n'
            '*showlist* - выводит ваш список добавленных групп.\n\n'
            '*delid(#)* - удаляет id группы из вашего списка по его порядковому номеру.\n'
            'Например: "*delid(3)*".\n\n'
            '*/help* - вызывает памятку команд.\n\n'
            'По всем вопросам обращайся по адресу:\n'
            'geraskin.ra@gmail.com',parse_mode='Markdown')
    if not (str(message.chat.id) in allUsersId):  # если данного "chat_id" еще не встречалось то заносим его в базу
        f = open('users.txt', 'a')  # заонсим в базу
        f.write(str(message.chat.id) + '\n')
        f.close()
        f = open('users_database/' + str(message.chat.id) + '.txt', 'w')  # создаём личный файл в каталоге "users_database/"
        f.close()
        allUsersId.append(str(message.chat.id))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print('Я ЗАШЁЛ В ФУНКЦИЮ messageHandler')
    print(message.text)
    first_name = 'goga'
    last_name = 'gogansberg'
    messageText = message.text
    chat_id = message.chat.id

    if not (str(message.chat.id) in allUsersId):  # если данного "chat_id" еще не встречалось то заносим его в базу
        f = open('users.txt', 'a')  # заонсим в базу
        f.write(str(message.chat.id) + '\n')
        f.close()
        f = open('users_database/' + str(message.chat.id) + '.txt', 'w')  # создаём личный файл в каталоге "users_database/"
        f.close()
        allUsersId.append(str(message.chat.id))


    try:
        if messageText=='showlist': # команда отображения всех групп пользователя
            userGroupsMessage = '' # здесь будет содержаться всё сообщение
            f = open('users_database/'+str(chat_id)+'.txt','r')
            num = 1
            for line in f: # цикл формирующий сообщение построчно " <№>) <id группы> - <название группы> \n... "
                gr_name = getGroupName(tokenVK, line[0:len(line)-1])
                userGroupsMessage = userGroupsMessage + str(num) + ') ' + line[0:len(line)-1] + ' - *' + gr_name + '*\n'
                num = num + 1
                time.sleep(0.1)
            f.close()
            if len(userGroupsMessage)==0:
                bot.send_message(chat_id,'Ваш список групп пуст.')
            else:
                bot.send_message(chat_id,userGroupsMessage,parse_mode='Markdown')
        elif (messageText[0:5] == 'delid'): #######################################################################
            if validationMessage(messageText)=='N': # условие: если номер из списка групп введён верно
                bot.send_message(chat_id,'Некорректно введён номер группы из списка.')
            else:
                grDelNum = int(validationMessage(messageText))# id удаляемой группы
                allUsersGroups = []# массив id всех групп конкретного пользователя
                f = open('users_database/'+str(chat_id)+'.txt','r')
                for line in f:
                    allUsersGroups.append(line)# Сохранение в массив вместе с символом "\n" на конце
                f.close()
                if len(allUsersGroups)<int(grDelNum):# если пользователь ввёл число превышающее количесвто групп в списке
                    bot.send_message(chat_id,'Невозможно удалить группу с таким номером ( всего групп в списке: '
                              + str(len(allUsersGroups))+' ).')
                else:
                    delGroupId = allUsersGroups.pop(int(grDelNum)-1)# id удаляемой группы
                    delGroupId = delGroupId[0:len(delGroupId)-1] #удаляем из переменной пробел в кнце
                    f = open('users_database/'+str(chat_id)+'.txt','w')
                    for line in allUsersGroups:
                        f.write(line)
                    f.close()


                    ind = -1;
                    tmp = [] # удаление id пользователя из файла групп
                    f = open('groups_database/' + str(delGroupId)+'.txt','r')
                    for line in f: tmp.append(line[0:len(line)-1])
                    f.close()
                    try: ind = tmp.index(str(chat_id))
                    except: pass
                    if ind>=0:
                        tmp.pop(ind)
                        countOfUsersOfGroup = len(tmp);
                        f = open('groups_database/' + str(delGroupId)+'.txt','w')
                        for item in tmp:
                            f.write("%s\n" % item)
                        f.close()

                    # проверка, на наличие отслеживающих пользователей у удаляемой группы. Если пользователей больше
                    # нет, то она удаляется из списка "groups.txt", иначе её осталяем в этом списке
                    if countOfUsersOfGroup==0:
                        tmp = []
                        f = open('groups.txt', 'r')
                        for line in f: tmp.append(line[0:len(line) - 1])
                        f.close()
                        tmp.pop(grDelNum - 1)
                        f = open('groups.txt', 'w')
                        for item in tmp:
                            f.write("%s\n" % item)
                        f.close()
                    gr_name = getGroupName(tokenVK, delGroupId)# название предполагаемой группы
                    bot.send_message(chat_id,'Группа "*' + gr_name + '*" удалена из вашего списка',parse_mode='Markdown')
        elif (messageText[0:5]=='setid'):# если пришло сообщение с командой /id для добавления в список новой группы
            gr_id = str(isGroupExist(tokenVK,message.text))
            if gr_id == 'ans1':
                bot.send_message(chat_id, 'Некорректно введён id группы.')
            elif (gr_id =='ans2')or(int(gr_id)<=0):
                bot.send_message(chat_id, 'Группы с таким идентификатором не существует.')
            else:
                if not(isActiveGroup(tokenVK, gr_id)):# если группа  удалена или заблокирована
                    bot.send_message(chat_id, 'Группы с таким идентификатором удалена или заблокированна.')
                else:
                    allUsersGroups = []# массив id всех групп конкретного пользователя
                    f = open('users_database/' + str(chat_id) + '.txt', 'r')
                    for line in f:
                        allUsersGroups.append(line)# Сохранение в массив вместе с символом "\n" на конце
                    f.close()
                    if not ((gr_id + '\n') in allUsersGroups):# если эта группа ещё не была добавлена в список
                        gr_name = getGroupName(tokenVK, gr_id)# название предполагаемой группы
                        bot.send_message(chat_id, 'Группа "*' + gr_name + '*" добавлена в ваш список групп.',
                                         parse_mode='Markdown')
                        f = open('users_database/' + str(chat_id) + '.txt', 'a')
                        f.write(str(gr_id) + '\n')
                        f.close()

                        usersInGroup =[]#добавление нового файла группы в каталог "groups_database/"
                        f = open('groups_database/' + str(gr_id) + '.txt', 'a')
                        f.close()
                        f = open('groups_database/' + str(gr_id) + '.txt', 'r')
                        for line in f:
                            usersInGroup.append(line[0:len(line)-1])
                        f.close()
                        if not (chat_id in usersInGroup):
                            f = open('groups_database/' + str(gr_id) + '.txt', 'a')
                            f.write(str(chat_id) + '\n')
                            f.close()
                        usersInGroup =[]

                        groups = [] #добавление новой группы в файл "groups.txt"
                        f = open('groups.txt', 'r')
                        for line in f:
                            groups.append(line[0:len(line) - 1])
                        f.close()
                        if not (gr_id in groups):
                            f = open('groups.txt', 'a')
                            f.write(str(gr_id) + '\n')
                            f.close()

                    else:
                        bot.send_message(chat_id,'Группа с таким id уже была добавлена в вашь список.')
        else:# если пользователь прислал любое сообщение к которому у бота не привязанна никакая функция
            bot.send_message(chat_id,'Некорректная команда.')
    except Exception as err:
        err = str(err)
        bot.send_message('281667447', 'произошла ошибка\n\n' + err )
        pass




def vk_part():           # второй поток бота, выполняющий олпросы всех записанных групп ВК
    oldUpdate = dict()
    newUpdate = dict()
    allGroups = []
    f = open('groups.txt','r')
    for line in f:
        allGroups.append(line[0:len(line)-1])
    f.close()
    for group_id in allGroups:# заполнение старыми
        oldUpdate[str(group_id)] = vkGetMembers(tokenVK, str(group_id))
    while True:

        #проверка на наличие хотябы одного пользователя
        tmp = []
        f = open('users.txt','r')
        for line in f: tmp.append(line[0:len(line)-1])
        if tmp!=[]:
            for group_id in allGroups:# заполнение старыми
                newUpdate[str(group_id)] = vkGetMembers(tokenVK, str(group_id))
                newMembers = []
                for item in set(newUpdate[str(group_id)]).difference(oldUpdate[str(group_id)]):
                    newMembers.append(item)
                if newMembers != []:
                    f = open('groups_database/' + str(group_id) + '.txt','r')
                    for line in f:
                        print(newMembers)
                        sending_message =  '*' + getUserInf(tokenVK,str(newMembers)) + '*' + ' вступил в группу ' + '*' + str(getGroupName(tokenVK,group_id)) + '*' + '\n' + 'https://vk.com/id' + str(newMembers)
                        bot.send_message(line[0:len(line)-1],sending_message,parse_mode='Markdown')
                oldUpdate[str(group_id)] = newUpdate[str(group_id)]

            allGroups = []# проверка добавление новых груп в спсок проверок
            f = open('groups.txt', 'r')
            for line in f:
                allGroups.append(line[0:len(line) - 1])
            f.close()
            for group_id in allGroups:
                if not(group_id in oldUpdate.keys()):
                    oldUpdate[str(group_id)] = vkGetMembers(tokenVK, str(group_id))


def polling_function_threading():
    print('BOT поток')
    bot.polling(none_stop=True)
    pass


def vk_function_threading():
    print('VK поток')
    vk_part()
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


# вытаскиване из файла "users.txt" id всех юзеров и запись в переменную "allUsersId"
f = open('users.txt', 'r')
for line in f:
    lenLine = len(line)
    allUsersId.append(line[0:(lenLine - 1)])
f.close()
print(allUsersId)



# Создание новой нити
thread1 = myThread("VK", 1)
thread2 = myThread("BOT", 2)

# Запуск новой нити
thread1.start()
thread2.start()

thread1.join()
thread2.join()

