import os
import re
import time


def get_file_icon(file_name):
    file_type = file_name[file_name.rfind('.') + 1:]
    if file_type in ['mp4', 'avi', 'mov']:
        file_icon = 'film'
    elif file_type in ['mp3', 'wav']:
        file_icon = 'file-earmark-music'
    elif file_type in ['xlsx', 'xls', 'doc', 'docx', 'ppt', 'pptx', 'pdf']:
        file_icon = 'file-earmark-font'
    elif file_type in ['pdf']:
        file_icon = 'file-earmark-pdf-fill'
    elif file_type in ['jpg', 'gif', 'png']:
        file_icon = 'image'
    else:
        file_icon = 'file'
    return file_icon


def get_data(repo_path, file_path):
    path = os.path.join(repo_path, file_path)
    data = {'dirs': [], 'files': [], 'path': file_path.split('/')}
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
                mysize = str(format(round(os.path.getsize(mypath) / 1024), ',')) + ' KB'
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
