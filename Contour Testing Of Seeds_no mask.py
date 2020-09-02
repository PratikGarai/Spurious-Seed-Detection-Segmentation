#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy
import random   # for testing purpose only


# In[2]:


def process_contour(contour):
    x,y,w,h = cv.boundingRect(contour)
    im = img[y:y+h, x:x+w]     # this is the array to be sent to the function
    segments.append(im)
    #result = somefunction(im)
    result = random.randint(0,1)
    return result


# In[3]:


def filter_contours(contours, hierarchy):
    c = []
    for i,j in zip(contours,hierarchy[0]):
        if(j[3]==-1):
            c.append(i)
    return c


# In[4]:


def get_contoured_image(im):
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    imblur = cv.GaussianBlur(imgray,(5,5),sigmaX=0, sigmaY=0)
    imc = cv.Canny(imblur,30,220)
    ret, thresh = cv.threshold(imc, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = filter_contours(contours, hierarchy)
    for index,i in enumerate(contours):
        if process_contour(i)==1:
            color = (0,255,0)
        else :
            color = (0,0,255)
        cv.drawContours(im, contours, index, color, 2)
    return im


# In[5]:


def segment_printer(segments):
    for index,i in enumerate(segments):
        cv.imshow(str(index+1), cv.resize(i, (200,int(200/i.shape[1]*i.shape[0]))))
        cv.waitKey()
        cv.destroyAllWindows()


# In[6]:


img = cv.imread('images/img2.jpg')
segments = []     #for testing purpose only     

cv.imshow("Input", img)
new_image = get_contoured_image(img.copy())
cv.imshow("Output", new_image)
cv.waitKey()
cv.destroyAllWindows()
segment_printer(segments)    # for testing only


# In[ ]:




