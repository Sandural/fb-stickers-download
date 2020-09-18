'''
Description  : 
Author       : Lizishan
Date         : 2020-09-02 19:39:34
LastEditors  : Lizishan
LastEditTime : 2020-09-03 13:11:00
FilePath     : /sticker2gif/tools.py
'''
import os, shutil
import urllib.request

sep = os.path.sep
ope = os.path.exists
opj = os.path.join

def PathOrUrl(inpt):
    # If path return True else it is assumed a url
    print("inpt url", inpt)
    if os.path.exists(inpt):
        print("If path return True")
        return True
    try:
        print("访问URL")
        proxy=urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1087', 'https': 'https://127.0.0.1:1087'})  #使用urllib.request.ProxyHandler()设置代理服务器信息
        opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler) #创建全局默认opener对象使urlopen()使用opener
        urllib.request.install_opener(opener) 
        urllib.request.urlopen(inpt)
    except:
        raise TypeError('Boolean Required!')
    return False

def Download(url):
    pic = 'temp/img.png'
    try:
        urllib.request.urlretrieve(url , pic)
        return pic
    except:
        raise ConnectionError

def Rename(name):
    if not name:
        name = 'Sample'

    for i in os.listdir():
        if name + '.gif' == i:
            name += '1'
    
    return name

def Clean():
    try:
        shutil.rmtree('temp')
    except:
        pass

def Log(text, switch):
    if switch:
        print(text)
