import math

"""
***********************************************************************
*                                                                     *
*                            X BASED LINES                            *
*                                                                     *
***********************************************************************
"""

def pixel(img, b0,y0,color):
  pass

def x_perpendicular(img, color, 
                    x0, y0, dx, dy, 
                    xstep, ystep, einit, w_left, w_right, winit, pixel):
    
  threshold = dx - 2*dy
  E_diag= -2*dx
  E_square= 2*dy
  p=q=0

  y= y0
  x= x0
  error= einit
  tk= dx+dy-winit 

  while tk<=w_left:
     pixel(img,x,y, color)
     if error>=threshold:
       x += xstep
       error += E_diag
       tk += 2*dy
     error += E_square
     y += ystep
     tk += 2*dx
     q+=1

  y= y0
  x= x0
  error= -einit
  tk= dx+dy+winit

  while tk<=w_right:
     if p:
       pixel(img,x,y, color)
     if error>threshold:
       x= x - xstep
       error = error + E_diag
       tk += 2*dy

     error += E_square
     y -= ystep
     tk += 2*dx
     p+=1

  if q==0 and p<2:
    pixel(img,x0,y0,color) # we need this for very thin lines

def x_varthick_line(img, color, x0, y0, dx, dy, xstep, ystep, 
                    thickness, pixel, pxstep, pystep):
  p_error= 0
  error= 0
  y= y0
  x= x0
  threshold = dx - 2*dy
  E_diag= -2*dx
  E_square= 2*dy
  length = dx+1
  D= math.sqrt(dx*dx+dy*dy)

  for p in range(length):
    w_left=  thickness*2*D
    w_right= thickness*2*D
    x_perpendicular(img,color,x,y, dx, dy, pxstep, pystep,
                                      p_error,w_left,w_right,error, pixel)
    if (error>=threshold):
    
      y += ystep
      error += E_diag
      if (p_error>=threshold):
        x_perpendicular(img,color,x,y, dx, dy, pxstep, pystep,
                                    (p_error+E_diag+E_square), 
                                     w_left,w_right,error, pixel)
        p_error += E_diag
      
      p_error += E_square
    
    error += E_square
    x += xstep

"""
***********************************************************************
*                                                                     *
*                            Y BASED LINES                            *
*                                                                     *
***********************************************************************
"""

def y_perpendicular(img, color, x0, y0, dx, dy, 
                    xstep, ystep, einit, 
                    w_left, w_right, winit, pixel):
  p=0
  q=0
  threshold = dy - 2*dx
  E_diag= -2*dy
  E_square= 2*dx

  y= y0
  x= x0
  error= -einit
  tk= dx+dy+winit 

  while tk<=w_left:
     pixel(img,x,y, color)
     if error>threshold:
       y+= ystep
       error += E_diag
       tk += 2*dx
     
     error += E_square
     x += xstep
     tk += + 2*dy
     q+=1

  y= y0
  x= x0
  error= einit
  tk= dx+dy-winit

  while tk<=w_right:
     if p:
       pixel(img,x,y, color)
     if error>=threshold:
       y -= ystep
       error+= E_diag
       tk+= 2*dx
     
     error += E_square
     x-= xstep
     tk+= 2*dy
     p+=1

  if q==0 and p<2:
     pixel(img,x0,y0,color); #  we need this for very thin lines

def y_varthick_line(img, color, x0, y0, dx, dy, 
                    xstep, ystep, thickness, pixel,
                    pxstep, pystep):
  p_error= 0
  error= 0
  y= y0
  x= x0
  threshold = dy - 2*dx
  E_diag= -2*dy
  E_square= 2*dx
  length = dy+1
  D= math.sqrt(dx*dx+dy*dy)

  for p in range(length):
  
    w_left=  thickness*2*D
    w_right= thickness*2*D
    y_perpendicular(img,color,x,y, dx, dy, pxstep, pystep,
                                      p_error,w_left,w_right,error, pixel)
    if error>=threshold:
    
      x += xstep
      error += E_diag
      if p_error>=threshold:
      
        y_perpendicular(img,color,x,y, dx, dy, pxstep, pystep,
                                     p_error+E_diag+E_square,
                                     w_left,w_right,error, pixel)
        p_error += E_diag
      
      p_error += E_square
    
    error += E_square
    y += ystep

"""
***********************************************************************
*                                                                     *
*                                ENTRY                                *
*                                                                     *
***********************************************************************
"""

def draw_varthick_line(img, color, x0, y0, x1, y1, thickness, pixel):
  dx= x1-x0
  dy= y1-y0
  if dx == 0 and dy == 0:
    return
  xstep = 1
  ystep= 1

  if dx<0: 
    dx= -dx
    xstep= -1
  if dy<0:
    dy= -dy
    ystep= -1

  if dx==0:
    xstep= 0
  if dy==0:
    ystep= 0

  xch= 0
  match (xstep + ystep*4):
    case (-5):
      pystep= -1
      pxstep= 1
      xch= 1
    case -1 :
      pystep= -1
      pxstep= 0
      xch= 1
    case 3 :
      pystep=  1
      pxstep= 1
    case  -4 :
      pystep=  0
      pxstep= -1
    case  0:
      pystep=  0
      pxstep= 0
    case  4:
      pystep=  0
      pxstep= 1
    case  3:
      pystep= -1
      pxstep= -1
    case  1:
      pystep= -1
      pxstep= 0
    case  5:
      pystep=  1
      pxstep= -1
      xch=1

  if dx>dy:
    x_varthick_line(img,color,x0,y0,dx,dy,xstep,ystep,
                              thickness, pixel, pxstep,pystep)
  else:
    y_varthick_line(img,color,x0,y0,dx,dy,xstep,ystep,
                              thickness, pixel, pxstep,pystep)
