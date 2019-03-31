# проверка работы с файлами
'''
f = open('text.txt','w')
f.write("[13255]\n")
f.write("[85435468424]\n")
f.write("[7782545]\n")
f.close()

a = []
f = open('text.txt')
for line in f:
    l = len(line)
    print(l)
    print(int(line[1:l-2]))
    print()
    a.append(line[1:l-2])
f.close()


print(a[0])

f1 = open('text.txt','r')
GG = f1.read()
f1.close()
print(GG)
print(GG[1])
'''


#import requests
#tokenVK = 'a2d06454d4d521caa6370dcd5729e96318367448e71b4c3cf015790853fa69e0aa7a3592cef9cc34ad093'

#def getGroupName(tokenVK,group_id):
    # функция принимает на вход токен приложения вконтакте и id группы в целочисленном типе или строковом
    # возвращает имя группы по его id
    # для работы требуется подключить библиотеку "import requests"
#    method = 'groups.getById'  # выполняемый метод
#    vk_URL = 'https://api.vk.com/method/'  # просто сокраение для компактности строк кода
#    params = {'group_id': group_id, 'fields': 'name'}
#    r = requests.get(vk_URL + method + '?v=5.8&access_token=' + tokenVK, params)
#    response = r.json()  # переменная с принятой от VK инфой в ваиде словаря
#    return response['response'][0]['name']

#print(getGroupName(tokenVK,'91715917'))'''

'''
f = open('goga.txt','w')
a = ['142762\n','626271\n','348126\n','346128712\n']
for index in a:
    f.write(index)
f.close()
print(str(len(a)))
print(a)


b = []
f = open('goga.txt','r')
for line in f:
    b.append(line)
f.close()
print(b)
'''



tmp = []
f = open('goga.txt', 'r')
for line in f: tmp.append(line[0:len(line) - 1])
f.close()
print(tmp)
print(tmp==[''])
print(tmp==[])
print(len(tmp))
