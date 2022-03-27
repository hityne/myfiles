from django.test import TestCase
import os, time


# Create your tests here.

def get_data():
    repo_path = r'C:\Users\douxi\PycharmProjects\myfiles\myrepo'
    # print(os.listdir(repo_path))
    data = {}
    data['dirnames'] = []
    data['filenames'] = []
    for each in os.listdir(repo_path):
        if each.startswith('.') is False and each.startswith('~') is False:
            mypath = os.path.join(repo_path, each)
            if os.path.isdir(mypath):
                data['dirnames'].append(each)
            elif os.path.isfile(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = str(round(os.path.getsize(mypath) / 1024)) + ' KB'
                data['filenames'].append({'name': myname, 'time': 222, 'size': mysize})
    print(data)
    return data


def get_file_type(file_name):
    return file_name[file_name.rfind('.') + 1:]


def get_nav_path(file_path):
    file_path = 'test1/test2/test3'
    file_path_list = file_path.split('/')
    file_path_url = []
    print(file_path_list)
    for n, each in enumerate(file_path_list):
        file_path_url.append('/' + '/'.join(file_path_list[:n + 1]))
    result = list(zip(file_path_list, file_path_url))
    return result
