'''
Description  :
Author       : Lizishan
Date         : 2020-09-18 20:02:19
LastEditors  : Lizishan
LastEditTime : 2020-09-18 20:16:00
FilePath     : /sticker2gif/test.py
'''
import os
import shutil
rootpath = 'images'
path = 'Cute'
tempath = os.path.join(rootpath, path, 'temp')
cutpath = os.path.join(rootpath, path, 'cut')
outputpath = os.path.join(rootpath, path, 'gif')

if os.path.exists(outputpath):
    print('outputpath')
    shutil.rmtree(outputpath)
    os.makedirs(outputpath)
else:
    os.makedirs(outputpath)

if os.path.exists(cutpath):
    print('cutpath')
    shutil.rmtree(cutpath)
    os.makedirs(cutpath)
else:
    os.makedirs(cutpath)

if os.path.exists(tempath):
    print('tempath')
    shutil.rmtree(tempath)
    os.makedirs(tempath)
else:
    os.makedirs(tempath)
