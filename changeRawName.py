'''
Description  : 
Author       : Lizishan
Date         : 2020-09-18 14:17:44
LastEditors  : Lizishan
LastEditTime : 2020-09-18 19:15:56
FilePath     : /sticker2gif/getRAC.py
'''
import os
import ai
from PIL import Image
rootpath = 'images'
path = 'Cute'


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def getImgList():
    # 读取 imageList
    imageList = []

    rawpath = os.path.join(rootpath, path, 'raw')

    for i in findAllFile(rawpath):
        imageList.append(i)

    return imageList


def changeRawName(filename, imageName, rows, columns, size):
    os.rename(filename, f'images/Cute/raw/{imageName}-{size[0]}x{size[1]}-{rows}x{columns}.png')


imageList = getImgList()
if '.DS_Store' in imageList:
    imageList.remove('.DS_Store')

for img in imageList:
    sticker = Image.open(img)

    AI = ai.Brain(sticker)
    columns, rows = AI.run()

    size = sticker.size

    print(img)
    print('\nRows: {}, Columns: {}'.format(rows, columns))
    print(size)
    print('=================')
    imageName = img.split('/')[3].split('_')[0]
    changeRawName(img, imageName, rows, columns, size)
