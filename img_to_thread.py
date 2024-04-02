from PIL import Image, ImageOps
from xiaolinWusLineAlgorithm import draw_line
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
        def pixel(img, p, color, transparency):
            sum[0] += transparency*img.getpixel(p)
            sum[1] += transparency
        self.bresenham(p0, p1, 20,  1,pixel)
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
    
    def bresenham(self, p0, p1, color=20, transparency=1, function=None): # TODO if switch is active it always starts in the upper right corner
        if p0>p1:
            p0, p1 = p1, p0
        if function is None:
            def function(img, p, color=20, transparency=1):
                # substract "error"
                color = max(0, round((1-transparency)*img.getpixel(p)-transparency*color))
                img.putpixel(p, color)
        def meta_function(img, p, color=20, transparency=1, switch=False):
            if switch:
                x, y = p
                function(img, (y,x), color, transparency)
            else:
                function(img, p, color, transparency)
        if (p1[0]-p0[0]) ==0:
            m = float("inf")*(p1[1]-p0[1])
        else:
            m = (p1[1]-p0[1])/(p1[0]-p0[0])
        if abs(m)>1:
            m = 1/m
            switch = True
            p0 = (p0[1], p0[0])
            p1 = (p1[1], p1[0])
            if p0>p1:
                p0, p1 = p1, p0
        else:
            switch = False
        y = lambda x: m*x+b
        error = 0
        current_x, current_y = p0
        while current_x<p1[0]:
            # 3 options right, right up or right down
            meta_function(self.image, (current_x,current_y), color, transparency, switch)
            error += m
            if -1<error<1:
                current_x+=1
            elif 1<= error <2:
                error-=1
                current_x+=1
                current_y+=1
            elif -2< error <=-1:
                error+=1
                current_x+=1
                current_y-=1

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
def pixel(img, p, color, transparency):
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
