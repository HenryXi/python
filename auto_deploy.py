import os
import sys
import time
import urllib2

import BeautifulSoup

hudson_host = 'http://192.168.5.221:8080/hudson/view/LHJH/job/M_LHJH_'
war_host = 'http://192.168.100.195/build/LHJH/'
print('==========projects list=========')
path = os.getcwd()
project_list = []
i = 0
for target_file in os.listdir(path):
    if target_file[-3:] == "war":
        print '[' + str(i) + '] ' + target_file[:-4]
        project_list.append(target_file[:-4])
        i += 1
if not project_list:
    sys.exit("no project found.")
deploy_war = input('choose the num to auto deploy:')
target_project = project_list[deploy_war]
print 'choose the project: ' + target_project
project_build_url = hudson_host + project_list[deploy_war] + '/build?delay=0sec'
war_url = war_host + project_list[deploy_war] + "/M_LHJH_" + target_project + "/"
print('==========begin building=========')
content = urllib2.urlopen(project_build_url).read()
current_content = urllib2.urlopen(war_url).read()
dom = BeautifulSoup.BeautifulSoup(current_content)
current_war = dom.findAll('a')[-1].getText()[:-1]
target_url = ""
while True:
    time.sleep(3)
    current_content = urllib2.urlopen(war_url).read()
    dom = BeautifulSoup.BeautifulSoup(current_content)
    print('...')
    if current_war != dom.findAll('a')[-1].getText()[:-1]:
        target_url = war_url + dom.findAll('a')[-1].getText()[:-1]
        print('==========download url=========')
        print(target_url)
        break
print('============delete old war=============')
os.remove(path + "/" + target_project + ".war")
while True:
    time.sleep(1)
    print('...')
    if not os.path.isdir(path + "/" + target_project):
        break
print('============download war=============')
out = os.path.join(path, target_project + ".war")
page = urllib2.urlopen(target_url + "/" + target_project + ".war")
open(out, "wb").write(page.read())
print('============deploying war=============')
while True:
    time.sleep(1)
    print('...')
    if os.path.isdir(path + "/" + target_project):
        break
print('============deploy finish!=============')
