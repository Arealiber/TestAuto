# -*- coding:utf-8 -*-
import os


def create_tag(tag):
    os.system('git pull')
    cmd_str = 'git tag %s' % tag
    res = os.popen(cmd_str).readlines()
    os.popen('git push --tags').readline()
    # os.system('git tag -d %s' % tag)
    print(res)
    return res







