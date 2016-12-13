from __future__ import print_function

import os
import subprocess
import sys

time_out = 60


def get_program_list():
    print('==========programs list=========')
    program_list = []
    i = 0
    for target_file in os.listdir("D:\shortcut\start_on_boot"):
        if target_file[-3:] == "lnk":
            # todo open cpu and disk lnk file fail do not know why
            program_list.append("D:\shortcut\start_on_boot\\" + target_file)
            i += 1
    return program_list


def start_program(program_list):
    for program in program_list:
        p = subprocess.Popen("start /B " + program + " /WAIT", shell=True)


def main():
    print('==========Auto start program v1.0============')
    program_list = get_program_list()
    start_program(program_list)
    print(program_list)


def print_loading(num):
    if num == time_out - 1:
        sys.exit("auto deploy timeout! ")
    print('=' * num + '>')
    num += 1


if __name__ == '__main__':
    main()
