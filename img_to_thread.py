from PIL import Image, ImageOps
from xiaolinWusLineAlgorithm import draw_line
import numpy as np


class StringArt:
    def __init__(self, nails, input_image, thickness=2): #TODO invert picture
        self.image      = self.load_image(input_image)
        self.scale      = 1-(thickness-1)/self.image.width
        self.image      = self.image.resize((round(self.image.width*self.scale), round(self.image.height*self.scale)), Image.Resampling.LANCZOS)
        self.nails      = nails
        self.radius     = min(self.image.height, self.image.width)*0.49
        self.midx       = self.image.width / 2
        self.midy       = self.image.height / 2
        self.operations = []


    def load_image(self, path):
        image = Image.open(path).convert("L")  # Convert to grayscale
        # Convert the image to a NumPy array
        return image

    def nailToCoordinate(self, nail):
        #from polar coordinates
        return round(self.midx + self.radius*np.cos(2*np.pi*(nail/self.nails))), round(self.midy + self.radius*np.sin(2*np.pi*nail/self.nails))
    
    def getLine(self, start, end):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        if p1==p0:
            return 0
        sum = [0.0, 0.1]
        def pixel(img, p, color, transparency):
            sum[0] += transparency*img.getpixel(p)
            sum[1] += transparency
        draw_line(self.image, p0, p1, 0, pixel)
        return sum[0]/sum[1]

    def drawLine(self, start, end, color=200):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        draw_line(self.image, p0, p1, color)
        self.operations.append((start, end))

    def tryChange(self, start, end, color=200):
        self.pending_img = self.image.copy()
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        draw_line(self.pending_img, p0, p1, color)
        self.pending_operation = (start,end)
        
        return self.pending_img
    
    def acceptChange(self):
        self.image = self.pending_img
        self.operations.append(self.pending_operation)
    
    def printOperations(self, file=None):
        pass # TODO
    
    def invert(self):
        self.image = ImageOps.invert(self.image)

    

def random_pattern(nails, thread):
    import random
    print(nails)
    for i in range(thread):
        a = random.randint(0,nails)
        b = random.randint(0,nails)
        print(f"{a} {b}")
