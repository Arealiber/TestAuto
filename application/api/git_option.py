# -*- coding:utf-8 -*-
import os


def create_tag(project_path, tag):
    cmd = os.path.join(project_path, tag)
    return os.system(cmd)







