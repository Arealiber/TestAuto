# -*- coding:utf-8 -*-
import os
import re


def create_tag(soft_name, work_path):
    os.chdir(work_path)
    work_path_cmd = 'cd %s' % work_path
    tag_name = get_new_tag(soft_name, work_path)
    option_cmd = ';'.join([work_path_cmd, 'git pull origin master', 'git tag -a %s -m "创建版本发布测试tag"' % tag_name,
                           'git tag -f %s' % tag_name, 'git push origin %s -m "创建版本发布测试tag"' % tag_name])
    res = os.system(option_cmd)
    if res == 0:
        return tag_name
    return False


def delete_tag(work_path, tag_name):
    os.chdir(work_path)
    option_cmd = ';'.join(['git tag -d %s' % tag_name, 'git push origin --delete %s' % tag_name])
    res = os.system(option_cmd)
    if res == 0:
        return True
    return False


def get_all_tags(work_path):
    work_path_cmd = 'cd %s' % work_path
    show_tags_cmd = ';'.join([work_path_cmd, 'git tag'])
    tags_list = os.popen(show_tags_cmd).readlines()
    return tags_list


def get_new_tag(soft_name, work_path):
    tag_list = get_all_tags(work_path)
    soft_tags_list = [tag.splitlines()[0] for tag in tag_list if '{0}-test-v'.format(soft_name) in tag]
    if not soft_tags_list:
        return '{0}-test-v0.0.1'.format(soft_name)

    major_pattern = re.compile(r'-test-v(\d).\d.\d')
    max_major_ver_num = max([major_pattern.findall(name)[0] for name in soft_tags_list if major_pattern.findall(name)])
    child_pattern = re.compile(r'-test-v%d.(\d).\d' % int(max_major_ver_num))
    max_child_ver_num = max([child_pattern.findall(name)[0] for name in soft_tags_list if child_pattern.findall(name)])
    phase_pattern = re.compile(r'-test-v%d.%d.(\d)' % (int(max_major_ver_num), int(max_child_ver_num)))
    max_phase_num = max([phase_pattern.findall(name)[0] for name in soft_tags_list if phase_pattern.findall(name)])
    if int(max_phase_num) < 9:
        new_tag_name = '{0}-test-v{1}.{2}.{3}'.format(soft_name, str(max_major_ver_num), str(max_child_ver_num),
                                                      str(int(max_phase_num)+1))
    elif int(max_child_ver_num) < 9:
        new_tag_name = '{0}-test-v{1}.{2}.0'.format(soft_name, str(max_major_ver_num), str(int(max_child_ver_num)+1))
    else:
        new_tag_name = '{0}-test-v{1}.0.0'.format(soft_name, str(int(max_major_ver_num)+1))
    return new_tag_name






