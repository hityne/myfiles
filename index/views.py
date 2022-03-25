import json
import os
import time
from django.http import FileResponse
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
        # 读取文件
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
