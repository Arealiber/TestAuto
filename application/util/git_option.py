# -*- coding:utf-8 -*-
import os
import re


def create_tag(soft_name, work_path):
    work_path_cmd = 'cd %s' % work_path
    tag_name = get_new_tag(soft_name, work_path)
    git_tag_cmd = ';'.join([work_path_cmd, 'git tag %s' % tag_name])
    git_pull_cmd = ';'.join([work_path_cmd, 'git pull'])
    push_tag_cmd = ';'.join([work_path_cmd, 'git push origin %s' % tag_name])

    os.system(git_pull_cmd)
    os.system(git_tag_cmd)
    res = os.system(push_tag_cmd)
    if res == 0:
        return tag_name
    return False


def get_all_tags(work_path):
    work_path_cmd = 'cd %s' % work_path
    show_tags_cmd = ';'.join([work_path_cmd, 'git tag'])
    tags_list = os.popen(show_tags_cmd).readlines()
    return tags_list


def get_new_tag(soft_name, work_path):
    tag_list = get_all_tags(work_path)
    print(tag_list)
    soft_tags_list = [tag.splitlines() for tag in tag_list if '{0}-test-v'.format(soft_name) in tag]
    if not soft_tags_list:
        return '{0}-test-v0.0.1'.format(soft_name)
    major_pattern = re.compile(r'-test-v(\d).\d.\d')
    child_pattern = re.compile(r'-test-v\d.(\d).\d')
    phase_pattern = re.compile(r'-test-v\d.\d.(\d)')
    max_major_ver_num = max([major_pattern.findall(name)[0] for name in soft_tags_list])
    max_child_ver_num = [child_pattern.findall(name)[0] for name in soft_tags_list]
    max_phase_num = max([phase_pattern.findall(name)[0] for name in soft_tags_list])
    print(max_major_ver_num, max_child_ver_num, max_phase_num)
    if int(max_phase_num) < 9:
        new_tag_name = '{0}-test-v{1}.{2}.{3}'.format(soft_name, max_major_ver_num, max_child_ver_num, max_phase_num+1)
    elif max_child_ver_num < 9:
        new_tag_name = '{0}-test-v{1}.{2}.0'.format(soft_name, max_major_ver_num, max_child_ver_num+1)
    else:
        new_tag_name = '{0}-test-v{1}.0.0'.format(soft_name, max_major_ver_num+1)
    return new_tag_name






