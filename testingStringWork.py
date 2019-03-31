# проверка работы со строками
import requests

a = '/id [45608811]\n'

token = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'
g_id = '45608811'  #

def validationMessage(a):
    # функция проверки правильности ввода сообщения о новом id проверяемой группы
    # на вход функция принимает строку соощения
    # возвращает строку "N" в случае если в сообщении содержатся ошибки
    # возвращает строку с "чистым" id группы
    start = -1 # индекс начала циферного id (следующий после "[")
    end = -1   # индекс конца циферного id (предидущий после "]")

    for i in range(len(a)):
        if a[i]==']':
            end = i
            break
        elif a[i]=='[':
            start = i+1

    markOfErr = 0# маркер ошибки ввода (если в числе id будт найден нециферный символ)
    a = a[start:end]
    for c in a:
        if not((ord(c)>=48)&(ord(c)<=57)):
            markOfErr = 1;
            break

    if (start>0) & (end>start) & (markOfErr!=1): # проверка на верную расстановку кавычек и то, что в ковычках только цифры
        return a
    else:
        return 'N'


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


#answer = validationMessage(a)
#print(answer)
#print(getGroupName(token,5555555555))
