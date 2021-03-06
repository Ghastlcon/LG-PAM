#!/usr/bin/env py
import time
import requests
from random import shuffle
from colorama import Fore, Back, Style, init

init()

dst = '0123456789abcdefghijklmnopqrstuv'

class user :

    def __init__(self, cookie_dict, last_time):
        self.cookie_dict = cookie_dict
        self.last_time = last_time


class task :
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col


data = {'x': 0, 'y': 0, 'color': 0}
user_lst = []
task_que = []


def print_line():
    print(Fore.MAGENTA + '==============================================================================')


times = 0
mlst = []


def check_task(point):
    global times
    global mlst
    if times == 5000 :
        times -= 5000
        time.sleep(10)
    if times == 0 :
        try :
            q = requests.get('https://www.luogu.org/paintBoard/board',
                             cookies = user_lst[0].cookie_dict,
                             headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
        except :
            time.sleep(0.01)
            q = requests.get('https://www.luogu.org/paintBoard/board',
                             cookies = user_lst[0].cookie_dict,
                             headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
        mlst = q.text.split('\n')
        print('Mapping :')
        print(Fore.YELLOW + mlst[0])
    times += 1
    if mlst[point.x][point.y] == dst[point.col]:
        return True
    else :
        return False


with open('cookies.txt', 'r') as cok :
    coks = cok.readlines()
    for i in coks :
        umid = i.split(' ')[0]
        clid = i.split(' ')[1]
        uid  = i.split(' ')[2]
        uid = uid.replace('\n', '')
        user_lst.append(
            user(dict(UM_distinctid = umid, __client_id = clid, _uid = uid), time.time() - 29))
    print_line()
    print(Fore.CYAN + 'Users :')
    for i in user_lst :
        print(Fore.YELLOW + 'cookies : {0}'.format(i.cookie_dict))
    print_line()

base_x = 0
base_y = 0

with open('res.out', 'r') as pic :
    s = pic.readline()
    l = int(str(s).split(' ')[0])
    w = int(str(s).split(' ')[1])
    task_num = l * w

    lst = pic.readlines()
    for i in range(l):
        lst[i] = lst[i].replace('\n', '')
        print(lst[i])
        for j in range(w):
            task_que.append(task(j + base_x, i + base_y, int(lst[i].split(' ')[j])))
    print(Fore.GREEN + 'height : {0} width : {1}'.format(l, w))
    print(Fore.GREEN + '{0} tasks added'.format(l * w))
    shuffle(task_que)
    print_line()

task_success = 0
task_success_que = []
log_timer = time.time()
while len(task_que) > 0 :
    now_task = task_que[0]
    task_que.pop(0)
    stat = check_task(now_task)
    if stat == False :
        data['x'] = now_task.x
        data['y'] = now_task.y
        data['color'] = now_task.col
        user = user_lst[0]
        user_lst.pop(0)

        if 30 + user.last_time > time.time():
            time.sleep(30 + user.last_time - time.time())
        try :
            r = requests.post('https://www.luogu.org/paintBoard/paint',
                              data = data, cookies = user.cookie_dict, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
            print(data)
            print(user.cookie_dict)
        except :
            time.sleep(0.01)
            r = requests.post('https://www.luogu.org/paintBoard/paint',
                              data = data, cookies = user.cookie_dict, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'})
        if str(r.text).find('500') != -1 :
            out = Fore.RED
            print(out + 'Paint failed')
        else :
            out = Fore.GREEN
            print(out + 'Paint succeed')
            task_success += 1
            task_success_que.append(time.time())
            if len(task_success_que) != 0 :
                if time.time() - task_success_que[0] > 30 :
                    task_success_que.pop(0)
        print(out + 'ret_code : {0} text : {1}'.format(
            r.status_code, r.text))
        print(out + 'user : {0}'.format(user.cookie_dict))
        print(Fore.CYAN + 'pos & color : {0}'.format(data))
        print_line()
        user.last_time = time.time() + 1
        user_lst.append(user)
    task_que.append(now_task)

    if time.time() - log_timer > 5 :
        with open('stat.log', 'w') as logger :
            logger.write('30s {0}\n'.format(len(task_success_que)))
            logger.write('all {0}\n'.format(task_success))
            logger.write('{0}\n'.format(task_success / task_num))
        log_timer = time.time()
print('==============FINISHED=================')
print_line()
