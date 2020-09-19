from itertools import groupby
from PIL import Image
class Brain:
    def __init__(self, image):
        self.image = image
        
    def detect(self, rgb_img, x, y, i):
        for pixelX in range(0, x):

            # Pixel data will store sum of pixels colors in each line
            pixel_data = []
            for pixelY in range(y):

                # If i == -1 then we reverse the points (When we want to scan horizontal instead of vertical lines)
                point = (pixelX, pixelY)[::i]

                # Sum of (r, g, b) for each pixel
                
                rgb_sum = sum(rgb_img.getpixel(point))
                pixel_data.append(rgb_sum)
            # Checks if this line is transparent or contains colors
            # If True we yield 1 else 0
            detect = sum(pixel_data)
            if detect:
                yield 1
            else:
                yield 0


    def removeExpectedValue(self, v):
        # for index, i in enumerate(v):
        #     if index == 0: 
        #         pre = v[index]
        #     else:
        #         pre = v[index - 1]
            
        #     if index == len(v) - 1:
        #         after = 2
        #     else:
        #         after = v[index + 1]

        #     if pre == after and pre != v[index] or after == 2:
        #         v[index] = 2
        nodeIndex = []
        for index, num in enumerate(v):
            if index == len(v) - 1:
                after = v[index]
            else:
                after = v[index + 1]
            if num != after:
                nodeIndex.append(index)


        for index, i in enumerate(nodeIndex):
            if index == len(nodeIndex) - 1:
                after = nodeIndex[index] + 100
            else:
                after = nodeIndex[index + 1]
                
            if after - nodeIndex[index] <= 2:
                v[i+1] = 2
                v[i+2] = 2

    
        v = [x for x in v if x != 2]
        return v

    def run(self):
        width, height = self.image.size
        rgbImage = self.image.convert('RGB')
        wd = self.detect(rgbImage, width, height, 1)
        ht = self.detect(rgbImage, height, width, -1)
        
        # print(list(wd))
        # print(list(ht))

        # 下面两段代码， 作用大不大呢？对于图片里有分裂的情况，是没啥作用的。
        wd = self.removeExpectedValue(list(wd))
        ht = self.removeExpectedValue(list(ht))
    

        w = [i[0] for i in groupby(wd) if i[0]] # columns
        h = [i[0] for i in groupby(ht) if i[0]] # row

        return sum(w), sum(h)


# if __name__ == "__main__":
#     sticker = Image.open('images/Cute/raw/89687457_533987680850571_5547327863423762432_n.png')
#     AI = Brain(sticker)
#     columns, rows = AI.run()
#     print('\nRows: {}, Columns: {}'.format(rows, columns))