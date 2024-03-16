from PIL import Image, ImageOps
import math


class StringArt:
    def __init__(self, nails, input_image, resolution=0.7):
        if type(input_image) == str: 
            self.image  = self.load_image(input_image)
        else:
            self.image  = input_image
        self.scale      = resolution
        self.image      = self.image.resize((round(self.image.width*self.scale), round(self.image.height*self.scale)), Image.Resampling.LANCZOS)
        self.nails      = nails
        self.radius     = min(self.image.height, self.image.width)*0.49
        self.midx       = self.image.width / 2
        self.midy       = self.image.height / 2
        self.operations = []


    def load_image(self, path):
        image = Image.open(path).convert("L")  # Convert to grayscale
        return image

    def nailToCoordinate(self, nail):
        #from polar coordinates
        return round(self.midx + self.radius*math.cos(2*math.pi*(nail/self.nails))), round(self.midy + self.radius*math.sin(2*math.pi*nail/self.nails))
    
    def getLine(self, start, end):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        sum = [0.0, 0.1]
        def pixel(img, p, color, alpha_correction, transparency):
            sum[0] += transparency*img.getpixel(p)
            sum[1] += transparency
        self.bresenham(p0, p1, function=pixel)
        return sum[0]/sum[1]

    def drawLine(self, start, end, color=20, alpha_correction=1, function=None):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        self.bresenham(p0, p1, color, alpha_correction, function)
        self.operations.append((start, end))

    def tryChange(self, start, end, color=20, transparency=1, function=None):
        self.pending_img = self.image.copy()
        self.bresenham(start, end, color, transparency, function)
        self.pending_operation = (start,end)
        
        return self.pending_img
    
    def acceptChange(self):
        self.image = self.pending_img
        self.operations.append(self.pending_operation)

    def invert(self):
        self.image = ImageOps.invert(self.image)
    
    def bresenham(self, p0, p1, color=20, transparency=1, function=None):
        pass # implement anti aliasing of task 1 here

    def printOperations(self, file=None):
        pass # first output number of nails then each in a new line the start and end nail of a line seperated by a " "
 
