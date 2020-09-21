import os
# 自己创建一个存放 webp 的目录， 我这里建的文件夹的名字是 webps2gifs
webpPath = os.path.join('webps2gifs')

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname


def getImgList():
    # 读取 imageList
    imageList = []

    for i in findAllFile(webpPath):
        imageList.append(i)

    return imageList

if __name__ == "__main__":
    imgs = getImgList()
    for img in imgs:
        filename = img.split('/')[1].split('.')[0]
        # webp 转换成 gif
        os.system(f'webp2gif {img} {webpPath}/{filename}.gif')

# webp2gif webps2gifs/48867851.webp result.gif