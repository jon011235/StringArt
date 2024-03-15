from PIL import Image, ImageOps
from xiaolinWusLineAlgorithm import draw_line
import numpy as np


class StringArt:
    def __init__(self, nails, input_image, resolution=0.7,imagecolor='r'):
        self.imagecolor = imagecolor
        self.scale      = resolution
        if type(input_image) == str: 
            self.image  = self.load_image(input_image)
        else:
            self.image  = input_image
        self.image      = self.image.resize((round(self.image.width*self.scale), round(self.image.height*self.scale)), Image.Resampling.LANCZOS)
        self.nails      = nails
        self.radius     = min(self.image.height, self.image.width)*0.49
        self.midx       = self.image.width / 2
        self.midy       = self.image.height / 2
        self.operations = []


    def load_image(self, path):
        image = Image.open(path)
        self.outimage = Image.new('RGB',(round(image.size[0]*self.scale), round(image.size[1]*self.scale)),color='white')
        r,g,b = image.split()
        ori, ogi, obi = self.outimage.split()
        if self.imagecolor == 'r':
            self.outimage = ori
            return r
        elif self.imagecolor == 'b':
            self.outimage = obi
            return b
        elif self.imagecolor == 'g':
            self.outimage = ogi
            return g

    def nailToCoordinate(self, nail):
        #from polar coordinates
        return round(self.midx + self.radius*np.cos(2*np.pi*(nail/self.nails))), round(self.midy + self.radius*np.sin(2*np.pi*nail/self.nails))
    
    def getLine(self, start, end):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        sum = [0.0, 0.1]
        def pixel(img, p, color, alpha_correction, transparency):
            sum[0] += transparency*img.getpixel(p)
            sum[1] += transparency
        draw_line(self.image, p0, p1, 0, 1.0, pixel)
        return sum[0]/sum[1]

    def drawLine(self, start, end, color=20, alpha_correction=1, function=None):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        if function is None:
            draw_line(self.image, p0, p1, color, alpha_correction)
            draw_line(self.outimage, p0, p1, color, alpha_correction)
        else:
            draw_line(self.image, p0, p1, color, alpha_correction, function)
        self.operations.append((start, end))

    def tryChange(self, start, end, color=20, alpha_correction=1, function=None):
        self.pending_img = self.image.copy()
        self.drawLine(start, end, color, alpha_correction, function)
        self.image, self.pending_img = self.pending_img, self.image
        self.operations = self.operations[:-1]
        self.pending_operation = (start,end)
        
        return self.pending_img
    
    def acceptChange(self):
        self.image = self.pending_img
        self.operations.append(self.pending_operation)

    def invert(self):
        self.image = ImageOps.invert(self.image)
    
    def printOperations(self,  file=None):
        string = str(self.nails)
        for operation in self.operations:
            x, y = operation
            string += '\n'+str(x)+' '+str(y)
        return string

def create_strings(art):
  art.invert()
  c0 = 0
  c = 0
  previousNail = 0
  darkestLine = 0
  while len(art.operations) < 2000:#Chnage the number to de- or increase the number of Threads (Heavy influence on the runtime)
    c0 += 1
    darkestLine = 0
    for nail in range(art.nails):
            gotLine = art.getLine(previousNail,nail)
            if darkestLine < gotLine:
                darkestLine = gotLine
                darkestNail = nail
    art.drawLine(previousNail,darkestNail)
    previousNail = darkestNail
    if c0 == 50:
        c += 50
        c0 = 0
        print(c)
  art.invert()
  return art

def create_rgb_strings(rgb):
    art = StringArt(288,'./test-images/akropolis.jpeg',resolution=0.5,imagecolor=rgb) #You can change the filepath and increase the resolution
    art = create_strings(art)
    with open(rgb+'.txt','w') as f:
        f.write(art.printOperations())
    art.outimage.save(rgb+'.png')

import multiprocessing
manager = multiprocessing.Manager()

a = multiprocessing.Process(target=create_rgb_strings, args=('r'))
a.start()
b = multiprocessing.Process(target=create_rgb_strings, args=('g'))
b.start()
c = multiprocessing.Process(target=create_rgb_strings, args=('b'))
c.start()
a.join()
b.join()
c.join()

imager = Image.open('r.png')
imageg = Image.open('g.png')
imageb = Image.open('b.png')
from time import sleep
sleep(2) # to ensure the files are loaded correctly
image = Image.merge('RGB',(imager,imageg,imageb))
image.save('outputImage.png')
image.show()