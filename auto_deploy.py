import os
import sys
import time
import urllib2

import BeautifulSoup

hudson_host = 'http://192.168.5.221:8080/hudson/view/LHJH/job/M_LHJH_'
war_host = 'http://192.168.100.195/build/LHJH/'
path = os.getcwd()
time_out = 60


def get_project_list():
    print('==========projects list=========')
    project_list = []
    i = 0
    for target_file in os.listdir(path):
        if target_file[-3:] == "war":
            print '[' + str(i) + '] ' + target_file[:-4]
            project_list.append(target_file[:-4])
            i += 1
    return project_list


def choose_built_project(project_list):
    if not project_list:
        sys.exit("no project found.")
    deploy_war = input('choose the num to auto deploy:')
    target_project = project_list[deploy_war]
    print 'choose the project: ' + target_project
    if 'ROOT' == target_project:
        target_project = 'lhjh-support-web'
    return target_project


def build_supp_service(target_project):
    if '-web' in target_project:
        service_project = target_project.replace('-web', '-service')
        service_project_build_url = hudson_host + service_project + '/build?delay=0sec'
        service_war_url = war_host + service_project + "/M_LHJH_" + service_project + "/"
        print('==========build lhjh-supp-service first=========')
        urllib2.urlopen(service_project_build_url).read()
        service_war_content = urllib2.urlopen(service_war_url).read()
        service_dom = BeautifulSoup.BeautifulSoup(service_war_content)
        service_current_war = service_dom.findAll('a')
        for waiting_time in range(1, time_out):
            time.sleep(7)
            service_current_content = urllib2.urlopen(service_war_url).read()
            service_dom = BeautifulSoup.BeautifulSoup(service_current_content)
            print_loading(waiting_time)
            if service_current_war.__len__() != service_dom.findAll('a').__len__():
                print('==========lhjh-supp-service build finish=========')
                break


def build_interface(target_project):
    if '-service' in target_project:
        interface_project = target_project.replace('-service', '-interface')
        interface_project_build_url = hudson_host + interface_project + '/build?delay=0sec'
        interface_war_url = war_host + interface_project + "/M_LHJH_" + interface_project + "/"
        print('==========build interface first=========')
        urllib2.urlopen(interface_project_build_url).read()
        interface_content = urllib2.urlopen(interface_war_url).read()
        interface_dom = BeautifulSoup.BeautifulSoup(interface_content)
        interface_current_war = interface_dom.findAll('a')
        for waiting_time in range(1, time_out):
            time.sleep(5)
            interface_current_content = urllib2.urlopen(interface_war_url).read()
            interface_dom = BeautifulSoup.BeautifulSoup(interface_current_content)
            print_loading(waiting_time)
            if interface_current_war.__len__() != interface_dom.findAll('a').__len__():
                print('==========interface build finish=========')
                break


def build_target_project(target_project):
    print('==========begin building ' + target_project + '=========')
    project_hudson_url = hudson_host + target_project + '/build?delay=0sec'
    war_url = war_host + target_project + "/M_LHJH_" + target_project + "/"
    urllib2.urlopen(project_hudson_url).read()
    war_current_content = urllib2.urlopen(war_url).read()
    target_project_dom = BeautifulSoup.BeautifulSoup(war_current_content)
    current_war = target_project_dom.findAll('a')
    for waiting_time in range(1, time_out):
        time.sleep(5)
        war_current_content = urllib2.urlopen(war_url).read()
        target_project_dom = BeautifulSoup.BeautifulSoup(war_current_content)
        print_loading(waiting_time)
        if current_war.__len__() != target_project_dom.findAll('a').__len__():
            old_set = set()
            new_set = set()
            for old in current_war:
                old_set.add(old.getText())
            for new in target_project_dom.findAll('a'):
                new_set.add(new.getText())
            target_war_url = new_set - old_set
            target_url = war_url + next(iter(target_war_url))
            print('==========build finish=========')
            print('==========download url=========')
            print(target_url)
            return target_url


def undeploy_old_project(target_project):
    print('============delete old war=============')
    if 'lhjh-support-web' == target_project:
        target_project = 'ROOT'
    os.remove(path + "/" + target_project + ".war")
    for waiting_time in range(1, time_out):
        time.sleep(1)
        print_loading(waiting_time)
        if not os.path.isdir(path + "/" + target_project):
            print('============delete finish=============')
            break


def deploy_new_war(target_project, target_url):
    print('============download war=============')
    if 'lhjh-support-web' == target_project:
        out = os.path.join(path, "ROOT.war")
    else:
        out = os.path.join(path, target_project + ".war")
    page = urllib2.urlopen(target_url + "/" + target_project + ".war")
    open(out, "wb").write(page.read())
    print('============deploying war=============')
    for waiting_time in range(1, time_out):
        time.sleep(3)
        print_loading(waiting_time)
        if os.path.isdir(path + "/" + target_project):
            break
        elif 'lhjh-support-web' == target_project and os.path.isdir(path + "/ROOT"):
            break
    print('============deploy finish!=============')


def replace_js_config(target_project):
    print('============replace js config=============')
    for waiting_time in range(1, time_out):
        time.sleep(1)
        print_loading(waiting_time)
        if os.path.isdir(path + "/" + target_project):
            if os.path.isfile(path + "/" + target_project + "/mall/js/config_test.js"):
                os.remove(path + "/" + target_project + "/mall/js/config.js")
                os.rename(path + "/" + target_project + "/mall/js/config_test.js",
                          path + "/" + target_project + "/mall/js/config.js")
                break
            else:
                break
    print('============replace js config finish!=============')


def main():
    print '==========Auto deploy lhjh project v1.0============'
    project_list = get_project_list()
    target_project = choose_built_project(project_list)
    build_supp_service(target_project)
    build_interface(target_project)
    target_url = build_target_project(target_project)
    undeploy_old_project(target_project)
    deploy_new_war(target_project, target_url)
    replace_js_config(target_project)
    print '====Auto deploy ' + target_project + ' finish!======'
    print '=====God bless ' + target_project + ' without bug======='


def print_loading(num):
    if num == time_out - 1:
        sys.exit("auto deploy timeout! ")
    print '=' * num + '>';
    num += 1


if __name__ == '__main__':
    main()
