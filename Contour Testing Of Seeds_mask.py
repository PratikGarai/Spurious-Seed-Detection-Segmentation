import cv2 as cv
import numpy
import random   # for testing purpose only

def sharpen(img, k_size, factor):
    kernel = -1*(numpy.ones((k_size, k_size), dtype=numpy.uint8))
    kernel[int((k_size-1)/2),int((k_size-1)/2)] = factor
    img = cv.filter2D(img, -1, kernel)
    return img

def unshadow(img):
    rgb_planes = cv.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv.dilate(plane, numpy.ones((7,7), numpy.uint8))
        bg_img = cv.medianBlur(dilated_img, 21)
        diff_img = 255 - cv.absdiff(plane, bg_img)
        norm_img = cv.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv.merge(result_planes)
    result_norm = cv.merge(result_norm_planes)
    return(result, result_planes)

def get_img_from_mask(contour, show_masks):
    filled = numpy.zeros(img.shape, dtype= img.dtype)*255
    im = filled.copy()
    cv.drawContours(filled, [contour], 0, (255,255,255) , -1)
    x,y,w,h = cv.boundingRect(contour)
    if show_masks:
        cv.imshow("Output", filled)
        cv.waitKey()
        cv.destroyAllWindows()
    im[filled==(255,255,255)] = img[filled==(255,255,255)]
    im = im[y:y+h, x:x+w]
    return im

def process_contour(contour):
    im = get_img_from_mask(contour, show_masks=0)
    segments.append(im)
    #result = somefunction(im)
    result = random.randint(0,1)
    return result

def filter_contours(contours, hierarchy):
    c = []
    for i,j in zip(contours,hierarchy[0]):
        if(j[3]==-1):
            c.append(i)
    return c

def get_contoured_image(im, blur, canny_low, canny_ratio):
    imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    imblur = cv.GaussianBlur(imgray,(blur,blur),sigmaX=0, sigmaY=0)
    imc = cv.Canny(imblur,canny_low,canny_low*canny_ratio)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
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

def segment_printer(segments):
    for index,i in enumerate(segments):
        cv.imshow(str(index+1), cv.resize(i, (200,int(200/i.shape[1]*i.shape[0]))))
        cv.waitKey()
        cv.destroyAllWindows()


# <h3>Testing of full stuff</h3>
def full_test():
    cv.imshow("Input", img)
    new_image = get_contoured_image(img.copy(), blur = 5, canny_low=25, canny_ratio=5)
    cv.imshow("Output", new_image)
    cv.waitKey()
    cv.destroyAllWindows()
    #segment_printer(segments)    # for testing only

# <h3>Testing of unshadowing</h3>
def unshadow_tester():
    cv.imshow("Input", img)
    new_image = unshadow(img.copy())
    cv.imshow("Output Non", new_image[0])
    cv.imshow("Output With", new_image[0])
    cv.waitKey()
    cv.destroyAllWindows()

# <h3>Testing of Sharpening</h3>
def sharpening_tester():
    cv.imshow("Input", img)
    new_image = sharpen(img.copy(), 9, 85)
    cv.imshow("Output", new_image)
    cv.waitKey()
    cv.destroyAllWindows()

# <h3>Hyper-parameter testing (quite literally)</h3>
def hyper_tuner():
    for blur in range(1,9,2):
        for canny_low in range(10,150,30):
            for canny_ratio in range(1,10):
                if canny_low*canny_ratio>=255 :
                    break
                new_image = get_contoured_image(img.copy(), blur = blur, canny_low=canny_low, canny_ratio=canny_ratio)
                cv.imshow("Blur {}, canny low {}, ratio {} ".format(blur, canny_low, canny_ratio), new_image)
                cv.waitKey()
                cv.destroyAllWindows()

img = cv.imread('images/fenugreek seed.jpeg')
img = cv.resize(img, (700,700))
segments = []     #for testing purpose only     

if __name__=='__main__':
    full_test()
    unshadow_tester()
    sharpening_tester()
    hyper_tuner()
