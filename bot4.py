# бот отправляет во все чаты инфу о том что кто-либо подписался на тот или иной паблик вконтате
# при слишком быстрой отправке боту сообщений, бот будет отвечать на последнее, при этом игнорируя первые

import requests
import time


token = '258667681:AAGpgdlD_jepb2wlZpF9Zm3MWIq4KYO6_YY'
url = "https://api.telegram.org/bot" + token + "/"
tokenVK = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'
g_id = 69930438  #
allUsersId = [] # массив id всех чатов с которыми переговаривается бот


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

def validationMessage(message):
    # функция проверки правильности ввода сообщения о новом id проверяемой группы
    # на вход функция принимает строку соощения
    # возвращает строку "N" в случае если в сообщении содержатся ошибки
    # возвращает строку с "чистым" id группы
    start = -1 # индекс начала циферного id (следующий после "[")
    end = -1   # индекс конца циферного id (предидущий после "]")

    for i in range(len(message)):
        if message[i]==']':
            end = i
        elif (message[i]=='[')&(start==-1):
            start = i+1

    markOfErr = 0# маркер ошибки ввода (если в числе id будт найден нециферный символ)
    message = message[start:end]
    for c in message:
        if not((ord(c)>=48)&(ord(c)<=57)):
            markOfErr = 1
            break
    if message=='':
        markOfErr = 1
    elif (int(message)<=0): #если числовое значение id меньше нуля
        markOfErr = 1

    if (start>0) & (end>start) & (markOfErr!=1): # проверка на верную расстановку кавычек и то, что в ковычках только цифры
        return message
    else:
        return 'N'

def messageHandler(lastUpdate):
    # функция обработчика входящий сообщений от пользователей telegram
    # на вход принимает словарь с последним обновлением
    # выполняет соответствующие входящим сообщениям функции
    update_id = lastUpdate['update_id']
    print('Я ЗАШЁЛ В ФУНКЦИЮ messageHandler')
    try: # предотвращение ошибки кода если юзер исправляет написанное им сообщение ключ "message" меняется на "edited_message"
        first_name = lastUpdate['message']['from']['first_name']
        last_name = lastUpdate['message']['from']['last_name']
        message = lastUpdate['message']['text']
        chat_id = lastUpdate['message']['chat']['id']
    except Exception:
        first_name = lastUpdate['edited_message']['from']['first_name']
        last_name = lastUpdate['edited_message']['from']['last_name']
        message = lastUpdate['edited_message']['text']
        chat_id = lastUpdate['edited_message']['chat']['id']


    if message == ('/start') or (message == '/help'): # тут всё предельно понятно
        send_mess(chat_id,
                  'Дороу, это бот отсылает тебе оповещения  о подписке на группу в ВК. '
                  'Группу ты можешь указать сам, написав сообщение "/idSet ************". '
                  'Звёздочками указан id группы в цифровом формате например:\n'
                  '/idSet [96542134]')
        if not((str(chat_id)+'\n') in allUsersId): # если данного "chat_id" еще не встречалось то заносим его в базу
            f = open('users.txt','a') # заонсим в базу
            f.write(str(chat_id) + '\n')
            f.close()
            f = open('users_database/'+str(chat_id)+'.txt','w') #создаём личный файл в каталоге "users_database/"
            f.close()

    elif message=='/showList': # команда отображения всех групп пользователя
        userGroupsMessage = '' # здесь будет содержаться всё сообщение
        f = open('users_database/'+str(chat_id)+'.txt','r')
        num = 1
        for line in f: # цикл формирующий сообщение построчно " <№>) <id группы> - <название группы> \n... "
            gr_name = getGroupName(tokenVK, line[0:len(line)-1])
            userGroupsMessage = userGroupsMessage + str(num) + ') ' + line[0:len(line)-1] + ' - ' + gr_name + '\n'
            num = num + 1
            time.sleep(0.1)
        f.close()
        if len(userGroupsMessage)==0:
            send_mess(chat_id,'Ваш список групп пуст.')
        else:
            send_mess(chat_id,userGroupsMessage)

    elif (message[0:6] == 'delId ') or (message[0:6] == 'delId['):
        if validationMessage(message)=='N': # условие: если номер из списка групп введён верно
            send_mess(chat_id,'Некорректно введён номер группы из списка.')
        else:
            grDelNum = int(validationMessage(message))# id удаляемой группы
            allUsersGroups = [] # массив id всех групп конкретного пользователя
            f = open('users_database/'+str(chat_id)+'.txt','r')
            for line in f:
                allUsersGroups.append(line) # Сохранение в массив вместе с символом "\n" на конце
            f.close()
            if len(allUsersGroups)<int(grDelNum): # если пользователь ввёл число превышающее количесвто групп в списке
                send_mess(chat_id,'Невозможно удалить группу с таким номером ( всего групп в списке: '
                          + str(len(allUsersGroups))+' ).')
            else:
                delGroupId = allUsersGroups.pop(int(grDelNum)-1) # id удаляемой группы
                f = open('users_database/'+str(chat_id)+'.txt','w')
                for line in allUsersGroups:
                    f.write(line)
                f.close()
                delGroupId = delGroupId[0:len(delGroupId)-1]
                gr_name = getGroupName(tokenVK, delGroupId)  # название предполагаемой группы
                send_mess(chat_id,'Группа "' + gr_name + '" удалена из вашего списка')



    elif (message[0:6]=='setId ')or(message[0:6]=='setId['): # если пришло сообщение с командой /id для добавления в список новой группы
        if validationMessage(message)=='N': # условие: если id группы введён неверно
            send_mess(chat_id,'Некорректно введён id группы.')
        else:
            gr_id = validationMessage(message)# id предполагаемой группы
            allUsersGroups = []  # массив id всех групп конкретного пользователя
            f = open('users_database/' + str(chat_id) + '.txt', 'r')
            for line in f:
                allUsersGroups.append(line)  # Сохранение в массив вместе с символом "\n" на конце
            f.close()
            if not((gr_id+'\n') in allUsersGroups):#если эта группа ещё не была добавлена в список
                gr_name = getGroupName(tokenVK,gr_id)# название предполагаемой группы
                if (gr_name == 'DELETED')or(gr_name == ''):# условие: группы с введённым id не существует
                    send_mess(chat_id, 'Группы с таким id не существует.')
                else: # если сообщение сформированно верно, при этом группа с данным id сущесствует (ВСЁ ОК!!!!)
                    send_mess(chat_id, 'Группа "'+gr_name+'" добавленна в ваш список групп.')
                    f = open('users_database/'+str(chat_id)+'.txt','a')
                    f.write(str(gr_id)+'\n')
                    f.close()
            else:
                send_mess(chat_id,'Группа с таким id уже была добавлена в вашь список.')


    else: # если пользователь прислал любое сообщение к которому у бота не привязанна никакая функция
        send_mess(chat_id,'Ответ на сообщение: "' + message + '" от: ' + first_name + ' ' + last_name + '.')




def main():

    # вытаскиване из файла "users.txt" id всех юзеров и запись в переменную "allUsersId"
    f = open('users.txt','r')
    for line in f:
        lenLine = len(line)
        allUsersId.append(line[0:(lenLine-1)])
    f.close()


    lu = last_update(get_updates_json(url))
    update_id = lu['update_id']

    old = vkGetMembers(tokenVK, g_id)

    while True:
        lu = last_update(get_updates_json(url))
        print(lu)

        # проверка входящих сообщений
        if update_id != lu['update_id']:# если новый id сообщения не похож на старый
            messageHandler(lu)
            update_id = lu['update_id']


        # вконтактовская часть (проверка на наличие новых подписчиков)
        new = vkGetMembers(tokenVK, g_id)
        newMembers = []
        for item in set(new).difference(old):
            newMembers.append(item)
        if newMembers != []:
            send_mess(get_chat_id(lu),newMembers)
        old = new
        time.sleep(0.2)


if __name__ == '__main__':
    main()
