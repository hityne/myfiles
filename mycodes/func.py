import os
import time


def get_data(repo_path, name):
    path = os.path.join(repo_path, name)
    data = {'dirs': [], 'files': [], 'path': name.split('/')}
    for each in os.listdir(path):
        if each.startswith('.') is False and each.startswith('~') is False:
            mypath = os.path.join(path, each)
            if os.path.isdir(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = '-'
                data['dirs'].append({'name': myname, 'time': mytime, 'size': mysize, 'path': name})
            elif os.path.isfile(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = str(format(round(os.path.getsize(mypath) / 1024), ',')) + ' KB'
                data['files'].append({'name': myname, 'time': mytime, 'size': mysize, 'path': name})

    return data
