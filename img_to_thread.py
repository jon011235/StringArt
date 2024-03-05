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
        if file is None:
            print(str(self.nails))
            print("\n".join([f"{i[0]} {i[1]}" for i in self.operations]))
        else:
            with open(file, "w") as file:
                file.write(self.nails)
                file.write("\n".join([f"{i[0]} {i[1]}" for i in self.operations]))
    
    def invert(self):
        self.image = ImageOps.invert(self.image)

    

def greedy(art, iterations=100):
    prev_nail = 0
    for i in range(iterations):
        print(f"{i} iteration")
        maxi = 0
        max_nail = 0
        for i in range(0,nails): # try all reachable nails
            if i==prev_nail:
                continue
            brightness = art.getLine(prev_nail, i)
            if brightness > maxi:
                maxi = brightness
                max_nail = i
        art.tryChange(prev_nail, max_nail)
        art.acceptChange()
        prev_nail = max_nail
    return art

def drawMorePercent(art, lines, cut_at_percent=0.3, color=100, max_lines=4000):  # remmber to make a new image
    threshold_point = round(cut_at_percent*len(lines))
    print(len(lines), round(cut_at_percent*len(lines)))
    #[art.drawLine(start, end, color) for v, start, end in lines if threshold>art.getLine(start,end)]
    i=0
    for v, start, end in lines[art.nails:threshold_pointe+art.nails]: # art.nails: since the first ones are nail to same nail
        if lines[threshold_point][0]>art.getLine(start,end):
            i+=1
            if i>max_lines:
                break
            art.drawLine(start, end, color)
    print(i)
            

def drawUntilThreshold(art, cut_at_percent=0.6, color=220, max_lines= 4000):
    l = []
    for start in range(art.nails):  # Try every possible string
        print(f"batch {start}")
        for end in range(art.nails):
            brightness = art.getLine(start,end)
            l.append((brightness, start, end))

    l.sort()
    drawMorePercent(art, l, cut_at_percent, color, max_lines)
    return l # Allows you to play around with different percent

def random_pattern(nails, thread):
    import random
    print(nails)
    for i in range(thread):
        a = random.randint(0,nails)
        b = random.randint(0,nails)
        print(f"{a} {b}")

def gcode_to_thread(path):
    with open(path) as file:
        a = file.read()
    for i in a.split("\n"):
        b = i.split("\t")
        instructions.append(b[0]+" "+b[1])
        maximum = max(int(b[0]),int(b[1]),maximum)
    print(maximum)
    print("\n".join(instructions))


if __name__ == "__main__":
    t = img_to_thread.StringArt(300, "test-images/face.jpg", 100)
    save = img_to_thread.drawUntilThreshold(t, 0.85, 100)
    t.printOperations("out.art")
