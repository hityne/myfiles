import os
import time


def get_data(repo_path, file_path):
    path = os.path.join(repo_path, file_path)
    data = {'dirs': [], 'files': [], 'path': file_path.split('/')}
    for each in os.listdir(path):
        if each.startswith('.') is False and each.startswith('~') is False:
            mypath = os.path.join(path, each)
            print('file_path:', file_path)
            if file_path == '':
                print(True)
            if os.path.isdir(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = '-'
                data['dirs'].append({'name': myname, 'time': mytime, 'size': mysize, 'path': file_path})
            elif os.path.isfile(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = str(round(os.path.getsize(mypath) / 1024)) + ' KB'
                data['files'].append({'name': myname, 'time': mytime, 'size': mysize, 'path': file_path})

    return data

