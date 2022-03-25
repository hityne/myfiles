from django.http import FileResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
import os, time, json

# Create your views here.
from django.utils.http import urlquote


def index(request):
    repo_path = './myrepo'
    # print(os.listdir(repo_path))
    data = {}
    dirnames = []
    filenames = []
    for each in os.listdir(repo_path):
        if each.startswith('.') is False and each.startswith('~') is False:
            mypath = os.path.join(repo_path, each)
            if os.path.isdir(mypath):
                dirnames.append(each)
            elif os.path.isfile(mypath):
                myname = each
                print(time.localtime(os.path.getmtime(mypath)))
                # mytime = time.strftime('%y-%m-%d %H:%M:%S', time.mktime(os.path.getmtime(mypath)))
                mysize = str(os.path.getsize(mypath)/1024)+' KB'
                filenames.append({'name':myname, 'time': 222, 'size': mysize})
    data['dirs'] = dirnames
    data['files'] = filenames

    return render(request, 'index.html', {'data': data})


def deep(request, name):
    repo_path = './myrepo'
    new_path = os.path.join(repo_path, name)
    if os.path.isfile(new_path):
        # 读取文件
        file = open(new_path, 'rb')
        response = FileResponse(file)

        # 使用urlquote对文件名称进行编码
        name = name[name.rfind('/') + 1:]
        response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(name)

        return response
    elif os.path.isdir(new_path):
        data = {}
        dirnames = []
        filenames = []
        for each in os.listdir(new_path):
            if each.startswith('.') is False and each.startswith('~') is False:
                if os.path.isdir(os.path.join(new_path, each)):
                    dirnames.append(each)
                elif os.path.isfile(os.path.join(new_path, each)):
                    filenames.append(each)
        data['dirs'] = dirnames
        data['files'] = filenames
        print(data)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('查无此文件')
