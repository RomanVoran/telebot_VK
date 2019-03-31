import requests
import time


tokenVK = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'
g_id = 45608811  #


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



old = vkGetMembers(tokenVK,g_id)
while 1:
    tStart = round(time.time())
    new = vkGetMembers(tokenVK,g_id)

    newMembers = []
    for item in set(new).difference(old):
        newMembers.append(item)

    if newMembers != []:
        print(newMembers)

    old = new
    print('check')
    print('за',round(time.time())-tStart,'сек. был выполнен один обход')
    time.sleep(5)


