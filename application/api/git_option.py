# -*- coding:utf-8 -*-
import os


def create_tag(project_path, tag):
    print(os.popen('pwd').readlines())
    os.system('cd %s' % project_path)
    print(os.popen('pwd').readlines())
    cmd_str = os.path.join(project_path, 'git tag %s' % tag)
    res = os.popen(cmd_str).readlines()
    os.popen('git push --tags').readline()
    # os.system('git tag -d %s' % tag)
    print(res)
    return res







