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
                data['dirnames'] .append(each)
            elif os.path.isfile(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = str(round(os.path.getsize(mypath)/1024))+' KB'
                data['filenames'].append({'name':myname, 'time': 222, 'size': mysize})
    print(data)
    return data



path = 'test4'

print(path.split('/'))