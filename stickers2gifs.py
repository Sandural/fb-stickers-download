import os, shutil, ai
import cv2
from PIL import Image
from tools import *
import shutil  


class Makers:
    def __init__(self, log=False):
        self.rootpath = 'images'
        self.path = 'Cute'
        self.rawpath = os.path.join(self.rootpath, self.path, 'raw')
        self.tempath = os.path.join(self.rootpath, self.path, 'temp')
        self.cutpath = os.path.join(self.rootpath, self.path, 'cut')
        self.outputpath = os.path.join(self.rootpath, self.path, 'gif')

        self.log = log

    def findAllFile(self, base):
        for root, ds, fs in os.walk(base):
            for f in fs:
                fullname = os.path.join(root, f)
                yield fullname

    def getImgList(self):
        # 读取 imageList
        imageList = []
        
        for i in self.findAllFile(self.rawpath):
            imageList.append(i)

        return imageList

    def cv2_crop(self, im, box):
        '''
        :param im: cv2加载好的图像
        :param box: 裁剪的矩形，(left, upper, right, lower)元组
        '''
        # 取最大的box
        print(box)
        
        return im.copy()[box[1]:box[3], box[0]:box[2], :]

    def get_transparent_location(self, image):
        '''
        获取基于透明元素裁切图片的左上角、右下角坐标

        :param image: cv2加载好的图像
        :return: (left, upper, right, lower)元组
        '''
        # 1. 扫描获得最左边透明点和最有点透明点坐标
        height, width, channel = image.shape
        assert channel == 4 # 无透明通道报错
        first_location = None  # 最先遇到的透明点
        last_location = None  # 最后遇到的透明点
        first_transparency = []  # 从左往右最先遇到的透明点，元素个数小于等于图像高度
        last_transparency = []  # 从左往右最后遇到的透明点，元素个数小于等于图像高度

        for y, rows in enumerate(image):
            
            for x, BGRA in enumerate(rows):
                alpha = BGRA[3]
                # with open('a.txt', 'a') as f:
                #     f.write(str(alpha))

                if alpha != 0:
                    if not first_location or first_location[1] != y:  # 透明点未赋值或为同一列
                        first_location = (x, y)  # 更新最先遇到的透明点
                        first_transparency.append(first_location)
                    last_location = (x, y)  # 更新最后遇到的透明点
            
            if last_location:
                last_transparency.append(last_location)
        
        # 2.矩形四个边的中点
        top = first_transparency[0]
        bottom = first_transparency[-1]
        left = None
        right = None
        for first, last in zip(first_transparency, last_transparency):
            if not left:
                left = first
            if not right:
                right = last
            if first[0] < left[0]:
                left = first
            if last[0] > right[0]:
                right = last

        # 3. 左上角、右下角
        upper_left = (left[0], top[1])  # 左上角
        bottom_right = (right[0], bottom[1])  # 右下角

        return upper_left[0], upper_left[1], bottom_right[0], bottom_right[1]
    
    def calBox(self, boxes):
        aDict = []
        x1List = []
        y1List = []
        x0List = []
        y0List = []

        for i, v in enumerate(boxes):
            z = {}
            z['index'] = i
            z['x1'] = v[0]
            z['y1'] = v[1]
            z['x0'] = v[2]
            z['y0'] = v[3]
            aDict.append(z)

        for item in aDict:
            x1List.append(item['x1'])
            y1List.append(item['y1'])
            x0List.append(item['x0'])
            y0List.append(item['y0'])

        return (min(x1List), min(y1List), max(x0List), max(y0List))

    def changeRawName(self, filename, imageName, rows, columns, size):
        os.rename(filename, f'{self.rawpath}/{imageName}-{size[0]}x{size[1]}-{rows}x{columns}.png')

    def gifImg(self, imageList):
        
                
        for img in imageList:
            # cut Image
            print(img) # images/Cute/raw/88254863-1152x1152-4x4.png
            (filepath,tempfilename) = os.path.split(img)
            (filename,extension) = os.path.splitext(tempfilename)
            imageName = filename.split("-")[0]
            sticker = Image.open(img)
            size = sticker.size

            rows = int(filename.split("-")[2].split('x')[0])
            columns = int(filename.split("-")[2].split('x')[1])

            # Using basic AI to determine mini images in each row and column
            # Log('\nAI Running...', self.log)
            # AI = ai.Brain(sticker)
            # columns, rows = AI.run()
            Log('\nRows: {}, Columns: {}'.format(rows, columns), self.log)

            # 这里的rows 和 columns 可能会计算不准确, 所以不在这里写这段代码了
            # self.changeRawName(img, imageName, rows, columns, size)  

            # Getting the fixed size of each mini image
            x, y = round(size[0] / columns), round(size[1] / rows)

            # Setting up cordinates
            cd = (0, 0, x, y)

            print('\nCutting process...', cd)
            n = 0
            for _ in range(rows):

                for _ in range(columns):

                    # Cropping the mini image
                    minSticker = sticker.crop(cd)
                    
                    colors = minSticker.convert('RGB').getcolors()
                    if colors == None:
                        colors = [(0, (1, 0, 0))]
                    
                    # Detecting empty mini images and bypassing them
                    if not (sum(colors[0][1]) == 0 and len(colors) == 1):
                        # minSticker.mode = RGBA so that we create a white background
                        # of same mode to avoid black background when converting to gif
                        # os.makedirs('temp', exist_ok=True)
                        os.makedirs(f'{self.tempath}/{imageName}', exist_ok=True)
                        Image.alpha_composite(Image.new('RGBA', (x, y), (0, 0, 0, 0)), minSticker).save(f'{self.tempath}/{imageName}/{n}.png')
                        n += 1
                    
                    # Cordinates of the next image in same row
                    cd = (cd[0] + x, cd[1], cd[2] + x, cd[3])
                
                # Cordinates of the first image in the next row
                cd = (0, cd[1] + y, x, cd[3] + y)

            pics = [i for i in os.listdir(os.path.join(self.tempath, imageName))]
            if '.DS_Store' in pics:
                pics.remove('.DS_Store')
            print("pics-→", pics)

            # Sorting pics ascendingly
            pics.sort(key = lambda x: int(x.split('.')[0]))

            print("pics sorted", pics)

            # 获取可裁剪区域
            boxes = []
            for i in pics:
                image = cv2.imread(os.path.join(self.tempath, imageName, i), cv2.IMREAD_UNCHANGED)
                # 保存裁剪后图片
                boxx = self.get_transparent_location(image)
                boxes.append(boxx)
            

            # print("box-→", boxes)
            box = self.calBox(boxes)
            sequencePngs = []
            
            # 按照最大的框裁剪
            for i in pics:
                image = cv2.imread(os.path.join(self.tempath, imageName, i), cv2.IMREAD_UNCHANGED)
                # 保存裁剪后图片
                result = self.cv2_crop(image, box)
                cutPath = os.path.join(self.cutpath, imageName)
                if not os.path.exists(cutPath):
                    os.makedirs(cutPath)

                print('裁剪后的保存路径: ', os.path.join(cutPath, i))
                cv2.imwrite(os.path.join(cutPath, i), result)
                sequencePngs.append(os.path.join(self.cutpath, imageName, i))
            
            # Create GIF
            Log('\nCreating Gif...', self.log)
            # print(f'convert -delay 20 -loop 0 -dispose 2 {os.path.join(self.rootpath, self.path, "temp", imageName)}/*.png -coalesce {os.path.join(self.rootpath, self.path, "gif")}/{imageName}.gif')
            # os.system(f'convert -delay 15 -loop 0 -dispose 2 {os.path.join(self.rootpath, self.path, "temp", imageName)}/*.png -coalesce {os.path.join(self.rootpath, self.path, "gif")}/{imageName}.gif')
            
            # frames = []
            # for i in pics:
            #     frame = Image.open(os.path.join(self.rootpath, self.path, 'temp', imageName, i))
            #     frames.append(frame)
            
            # print("frames", len(frames))

            # Correct any incorrect input
            # name = Rename(name)

            # tempPath = os.path.join(self.rootpath, self.path, 'temp', imageName)
            
            sequencePngs = ' '.join(sequencePngs)
            print("sequencePngs", sequencePngs)

            # 序列 png 转 animated webp
            print(f'img2webp -loop 0 -d 100 -lossy {sequencePngs} -o {self.outputpath}/{imageName}.webp')
            os.system(f'img2webp -loop 0 -d 100 -lossy {sequencePngs} -o {self.outputpath}/{imageName}.webp')

            # frames[0].save(f'{outputpath}/{imageName}.gif',
            #             format = 'GIF',
            #             save_all = True,
            #             append_images = frames[1:],
            #             duration = 120,
            #             transparency = 255,
            #             loop = 0,
            #             disposal = 2)    
            # os.system(f'apngasm {outputpath}/{imageName}.png {tempPath}/*.png 1 10') # 序列 png 转 动态 png
            # os.system(f'apng2gif -i {outputpath}/{imageName}.png -o {outputpath}/{imageName}.gif -t 128') # 动态 png 转 gif

    def run(self):
        # 删除 raw 文件里的 .DS_Store
        imageList = self.getImgList()
        if '.DS_Store' in imageList:
            imageList.remove('.DS_Store')

        # 清空文件夹里的数据
        if os.path.exists(self.outputpath):
            print('outputpath')
            shutil.rmtree(self.outputpath)
            os.makedirs(self.outputpath)
        else:
            os.makedirs(self.outputpath)

        if os.path.exists(self.cutpath):
            print('cutpath')
            shutil.rmtree(self.cutpath)
            os.makedirs(self.cutpath)
        else:
            os.makedirs(self.cutpath)

        if os.path.exists(self.tempath):
            print('tempath')
            shutil.rmtree(self.tempath)
            os.makedirs(self.tempath)
        else:
            os.makedirs(self.tempath)

        self.gifImg(imageList)

        Log('\nDone!', self.log)
        

# 运行前先确保 raw 文件夹下的文件已经更改里名称， 所以首先要允许 changeRawName.py 文件
tool = Makers(log=True)
tool.run()