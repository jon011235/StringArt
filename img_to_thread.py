from PIL import Image, ImageOps
from xiaolinWusLineAlgorithm import draw_line
import numpy as np
from queue import PriorityQueue


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

    def drawLine(self, start, end, color=200, alpha_correction=1, function=None):
        p0 = self.nailToCoordinate(start)
        p1 = self.nailToCoordinate(end)
        if function is None:
            draw_line(self.image, p0, p1, color, alpha_correction)
        else:
            draw_line(self.image, p0, p1, color, alpha_correction, function)
        self.operations.append((start, end))

    def tryChange(self, start, end, color=200, alpha_correction=1, function=None):
        self.pending_img = self.image.copy()
        draw_line(self.pending_img, start, end, color, alpha_correction, function)
        self.pending_operation = (start,end)
        
        return self.pending_img
    
    def acceptChange(self):
        self.image = self.pending_img
        self.operations.append(self.pending_operation)

    def invert(self):
        self.image = ImageOps.invert(self.image)
    
    def printOperations(self, file=None):
        erg = str(self.nails)+"\n"+"\n".join([f"{i[0]} {i[1]}" for i in self.operations])
        if file is None:
            print(erg)
        else:
            with open(file, "w") as file:
                file.write(erg)
    

def greedy(art, iterations=100):
    prev_nail = 0
    for i in range(iterations):
        print(f"{i} iteration")
        maxi = 0
        max_nail = 0
        for i in range(0,nails):
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

def copyQueue(q):
    q2 = PriorityQueue()
    q2.queue = q.queue.copy()
    return q2

def drawMoreLines(art, lines, color=100, alpha_correction=1, max_lines=4000):  # remmber to make a new image
    i=0
    while i<max_lines:
        v, start, end = lines.get()
        if lines.empty():
            break
        new_v = art.getLine(start,end)
        if lines.queue[0][0] >= new_v:
            art.drawLine(start, end, color, alpha_correction)
            i+=1
            print(i)
        else:
            lines.put((art.getLine(start,end), start, end))
            

def drawWithPrecalculation(art, color=250, alpha_correction=0.5, max_lines= 4000):
    l = PriorityQueue()
    for start in range(art.nails):  # Try every possible string
        print(f"batch {start}")
        for end in range(art.nails):
            brightness = art.getLine(start,end)
            l.put((brightness, start, end))

    ret = copyQueue(l)
    drawMoreLines(art, l, color, alpha_correction, max_lines)
    return ret # Allows you to play around with different percent

def draw_blank(art):
    im = Image.new(mode="L", size=(art.image.width, art.image.height))
    new = StringArt(art.nails, im, 1)
    for start, end in art.operations:
        new.drawLine(start, end, 200)
    return new

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

"""
two ideas below taken from halfmonty
"""
def pixel(img, p, color, alpha_correction, transparency):
    # in this implementation if color gets negative crashes
    # will happen if error gets small enough one pixel is enoug
    img.putpixel(p, round(img.getpixel(p)-transparency*color))  

def make_stringArt(image, nails=288, lines=4000, line_weight=20, min_distance=20):
    # min_distance say the minimum amount of pins the next pin has to be away
    try:
        nails = image.nails
        art = image
    except:
        art = StringArt(nails, image)
        art.invert()
    
    nail = 0
    last_nails = []

    for l in range(lines):
        max_err = -1
        best_nail = -1

        for offset in range(min_distance, nails-min_distance):
            test_nail = (nail + offset) % nails
            if test_nail in last_nails:
                continue
            line_err = art.getLine(nail, test_nail)

            if line_err > max_err:
                max_err  = line_err
                best_nail = test_nail

        art.drawLine(nail, best_nail, line_weight, function=pixel)
        
        last_nails.append(nail)
        if len(last_nails) > 20:
            last_nails.pop(0)
        nail = best_nail
    
        if l%100==0:
            print(l)
    
    return art


if __name__ == "__main__":
    t = StringArt(300, "test-images/einstein.jpg", 50)
    save = drawWithPrecalculation(t, 250, 0.5, 4000)
    t.image.show()
    draw_blank(t).image.show()
    t.printOperations("out.art")
