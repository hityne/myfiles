import json
import os
import time
import re

from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
# Create your views here.
from django.utils.http import urlquote

from mycodes.func import get_data, file_iterator

from django.contrib.auth.decorators import login_required
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import mimetypes


# def index(request):
#     data = get_data('./myrepo', '')
#     return render(request, 'index.html', locals())

@login_required
def deep(request, name):
    repo_path = './myrepo'
    new_path = os.path.join(repo_path, name)

    if os.path.isdir(new_path):
        data = get_data(repo_path, name)
        # print(data)
        return render(request, 'index.html', {'data': data})
    elif os.path.isfile(new_path):
        # if new_path.endswith('.jpg'):
        #     return render(request, 'img.html', {'data': {'name': name}})
        # # 读取文件
        # else:
        #     file = open(new_path, 'rb')
        #     response = FileResponse(file)
        #
        #     # 使用urlquote对文件名称进行编码
        #     name = name[name.rfind('/') + 1:]
        #     response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(name)
        #
        #     return response
        return HttpResponse('')
    else:
        return HttpResponse('访问出错！')


def user_login(request):
    if request.method != 'POST':
        next = request.GET.get('next', '')
        return render(request, 'login2.html', {'next': next})
    else:
        _username = request.POST.get('username')
        _password = request.POST.get('password')

        user = authenticate(username=_username, password=_password)

        if user:

            login(request, user)
            # 这一步就是登陆，login会与数据库交互，会创建session使下次登陆不需验证
            # print(user.is_authenticated)
            # return HttpResponse("Hello, {}".format(user.username))

            ########
            # data = pd.read_excel('./demo/files/财务181学生名单.xls', header=4)
            # x = data.to_dict('split')
            # result = [[each[0], each[1], each[2], each[5]] for each in x['data']]
            #
            next = request.POST.get('next')
            print("next:", next)
            if next:
                return redirect(next)
            else:
                return redirect('/')

            ########

        else:
            return render(request, "login2.html", {"message": "用户名或密码有误！"})


@login_required
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
        # return HttpResponseRedirect('/' + a)
        return HttpResponse("文件删除成功！")
    else:
        return HttpResponse("没有此文件！")

def user_logout(request):
    logout(request)
    return redirect('/login/')

def player(request):
    file_path = request.GET.get('file_path')
    return render(request, 'player.html', locals())

def stream_video(request, path):
    """ responds to the video file as """
    # path = 'static/media/show.mp4'  # 此为我的视频路径
    path=os.path.join('./myrepo/',path)
    print(path)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        if first_byte:
            first_byte = int(first_byte)
        else:
            first_byte = 0
        last_byte = first_byte + 1024 * 1024 * 8  # 8M per piece, the maximum volume of the response body
        if last_byte > size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(file_iterator(path, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        # When the video stream is not obtained, the entire file is returned in the generator mode to save memory.
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
