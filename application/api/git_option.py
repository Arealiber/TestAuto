# -*- coding:utf-8 -*-
import os


def create_tag(project_path, tag):
    os.system('cd %s' % project_path)
    cmd_str = 'git tag %s' % tag
    res = os.popen(cmd_str).readlines()
    os.system('git push --tag')
    # os.system('git tag -d %s' % tag)
    print(res)
    return res







