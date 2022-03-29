import os
import re
import time
import shutil


def get_file_icon(file_name):
    file_type = file_name[file_name.rfind('.') + 1:]
    if file_type in ['mp4', 'avi', 'mov', 'mkv']:
        file_icon = 'film'
    elif file_type in ['mp3', 'wav']:
        file_icon = 'file-earmark-music'
    elif file_type in ['iso', 'ISO']:
        file_icon = 'server'
    elif file_type in ['xlsx', 'xls', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'csv']:
        file_icon = 'file-earmark-font'
    elif file_type in ['pdf']:
        file_icon = 'file-earmark-pdf-fill'
    elif file_type in ['txt', 'md']:
        file_icon = 'file-text'
    elif file_type in ['jpg', 'gif', 'png']:
        file_icon = 'image'
    elif file_type in ['py', 'sh', 'js', 'ipynb', 'asp', 'php', 'net', 'jsp', 'jar', 'css', 'html', 'htm', 'c', 'C']:
        file_icon = 'file-earmark-code'
    elif file_type in ['exe']:
        file_icon = 'windows'
    elif file_type in ['zip', 'rar', 'gz']:
        file_icon = 'file-earmark-zip'
    else:
        file_icon = 'file-earmark'
    return file_icon


def get_nav_path(file_path):
    file_path_list = file_path.split('/')
    file_path_url = []
    # print(file_path_list)
    for n, each in enumerate(file_path_list):
        file_path_url.append('/' + '/'.join(file_path_list[:n + 1]))
    result = list(zip(file_path_list, file_path_url))
    return result


def get_data(repo_path, file_path):
    path = os.path.join(repo_path, file_path)
    data = {'dirs': [], 'files': [], 'path': get_nav_path(file_path)}
    for each in os.listdir(path):
        if each.startswith('.') is False and each.startswith('~') is False:
            mypath = os.path.join(path, each)
            if os.path.isdir(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                mysize = '-'
                data['dirs'].append({'name': myname, 'time': mytime, 'size': mysize, 'path': file_path})

            elif os.path.isfile(mypath):
                myname = each
                mytime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(mypath)))
                a = os.path.getsize(mypath)
                if a // 1024 < 1024:
                    mysize = str(delete_extra_zero(round(a / 1024, 0))) + ' K'
                elif 1024 <= a // 1024 < 1024 * 1024:
                    mysize = str(delete_extra_zero(round(a / 1024 / 1024, 1))) + ' M'
                else:
                    mysize = str(delete_extra_zero(round(a / 1024 / 1024 / 1024, 1))) + ' G'
                # mysize = str(format(round(os.path.getsize(mypath) / 1024), ',')) + ' KB'
                myicon = get_file_icon(each)
                data['files'].append(
                    {'name': myname, 'time': mytime, 'size': mysize, 'path': file_path, 'icon': myicon})

    return data


# 视频播放

def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data


def delete_extra_zero(n):
    """删除小数点后多余的0"""
    n = '{:g}'.format(n)
    n = float(n) if '.' in n else int(n)  # 含小数点转float否则int
    return n


def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    return {'total': total // (2 ** 30), 'used': used // (2 ** 30), 'free': free // (2 ** 30)}
