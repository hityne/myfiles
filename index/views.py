import json
import os
import time
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.utils.http import urlquote

from mycodes.func import get_data


# def index(request):
#     data = get_data('./myrepo', '')
#     return render(request, 'index.html', locals())

def deep(request, name):
    repo_path = './myrepo'
    new_path = os.path.join(repo_path, name)
    if os.path.isfile(new_path):
        if new_path.endswith('.jpg'):
            return render(request, 'img.html', {'data': {'name': name}})
        # 读取文件
        else:
            file = open(new_path, 'rb')
            response = FileResponse(file)

            # 使用urlquote对文件名称进行编码
            name = name[name.rfind('/') + 1:]
            response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(name)

            return response
    elif os.path.isdir(new_path):
        data = get_data(repo_path, name)
        return render(request, 'index.html', {'data': data})
    else:
        return HttpResponse('查无此文件')


def img(request):
    # data = get_data('./myrepo', '')
    return render(request, 'img.html', locals())


def delete(request):
    a = request.GET.get('a')
    print(a)
    b = request.GET.get('b')

    print(b)
    repo_path = './myrepo'
    new_path = os.path.join(repo_path, a, b)
    if os.path.exists(new_path):
        print(new_path)
        os.remove(new_path)
        return HttpResponseRedirect('/'+a)
    else:
        return HttpResponse("没有此文件！")