#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy
import random   # for testing purpose only


# In[2]:


def get_img_from_mask(contour):
    filled = numpy.ones(img.shape, dtype= img.dtype)*255
    cv.drawContours(filled, [contour], 0, (0,0,0) , -1)
    x,y,w,h = cv.boundingRect(contour)
    im = cv.bitwise_xor(img.copy(),filled)
    im = im[y:y+h, x:x+w]
    return im


# In[3]:


def process_contour(contour):
    im = get_img_from_mask(contour)
    segments.append(im)
    #result = somefunction(im)
    result = random.randint(0,1)
    return result


# In[4]:


def filter_contours(contours, hierarchy):
    c = []
    for i,j in zip(contours,hierarchy[0]):
        if(j[3]==-1):
            c.append(i)
    return c


# In[5]:


def get_contoured_image(im):
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    imblur = cv.GaussianBlur(imgray,(7,7),sigmaX=0, sigmaY=0)
    imc = cv.Canny(imblur,30,220)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    imc = cv.dilate(imc, kernel)
    ret, thresh = cv.threshold(imc, 127, 255,0 )
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = filter_contours(contours, hierarchy)
    for index,i in enumerate(contours):
        if process_contour(i)==1:
            color = (0,255,0)
        else :
            color = (0,0,255)
        cv.drawContours(im, contours, index, color, 2)
    return im


# In[6]:


def segment_printer(segments):
    for index,i in enumerate(segments):
        cv.imshow(str(index+1), cv.resize(i, (200,int(200/i.shape[1]*i.shape[0]))))
        cv.waitKey()
        cv.destroyAllWindows()


# In[7]:


img = cv.imread('images/img2.jpg')
segments = []     #for testing purpose only     

cv.imshow("Input", img)
new_image = get_contoured_image(img.copy())
cv.imshow("Output", new_image)
cv.waitKey()
cv.destroyAllWindows()
segment_printer(segments)    # for testing only

