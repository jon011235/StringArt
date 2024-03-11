"""
Inspired by the implementation from rosettacode.org
"""
from PIL import Image


def _fpart(x):
    return x - int(x)

def _rfpart(x):
    return 1 - _fpart(x)

def pixel(img, p, color=20, alpha_correction=1, transparency=0.8):
    # substract "error"
    transparency *= alpha_correction
    color = max(0, round(img.getpixel(p)-transparency*color))
    img.putpixel(p, color)  

def draw_line(img, p1, p2, color=200, alpha_correction=1, pixel=putpixel):
    """Draws an anti-aliased line in img from p1 to p2 with the given color."""
    x1, y1 = p1
    x2, y2 = p2
    if x1>x2:
        x1,x2 = x2,x1
        y1,y2 = y2,y1
        p1,p2 = p2,p1
    dx, dy = x2-x1, y2-y1
    steep = abs(dx) < abs(dy)
    p = lambda px, py: ((px,py), (py,px))[steep]

    if steep:
        x1, y1, x2, y2, dx, dy = y1, x1, y2, x2, dy, dx
    if x2 < x1:
        x1, x2, y1, y2 = x2, x1, y2, y1

    if dx == 0:
        return
    grad = dy/dx
    intery = y1 + _rfpart(x1) * grad
    def draw_endpoint(pt):
        x, y = pt
        xend = round(x)
        yend = y + grad * (xend - x)
        xgap = _rfpart(x + 0.5)
        px, py = int(xend), int(yend)
        pixel(img, p(px, py), color, alpha_correction, _rfpart(yend) * xgap)
        pixel(img, p(px, py+1), color, alpha_correction, _fpart(yend) * xgap)
        return px

    xstart = draw_endpoint(p(*p1)) + 1
    xend = draw_endpoint(p(*p2))

    for x in range(xstart, xend):
        y = int(intery)
        pixel(img, p(x, y), color, alpha_correction, _rfpart(intery))
        pixel(img, p(x, y+1), color, alpha_correction, _fpart(intery))
        intery += grad
