import cv2
import numpy as np

def MYfunc(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

cv2.namedWindow('Tracker')
cv2.resizeWindow('Tracker',640,240)

# for lmabo
cv2.createTrackbar('Hue Min','Tracker',0,179,MYfunc)
cv2.createTrackbar('Hue Max','Tracker',179,179,MYfunc)
cv2.createTrackbar('Satu Min','Tracker',59,255,MYfunc)
cv2.createTrackbar('Satu Max','Tracker',255,255,MYfunc)
cv2.createTrackbar('val Min','Tracker',94,255,MYfunc)
cv2.createTrackbar('val Max','Tracker',255,255,MYfunc)

# #for gra
# cv2.createTrackbar('Hue Min','Tracker',81,179,MYfunc)
# cv2.createTrackbar('Hue Max','Tracker',116,179,MYfunc)
# cv2.createTrackbar('Satu Min','Tracker',60,255,MYfunc)
# cv2.createTrackbar('Satu Max','Tracker',255,255,MYfunc)
# cv2.createTrackbar('val Min','Tracker',60,255,MYfunc)
# cv2.createTrackbar('val Max','Tracker',255,255,MYfunc)



while True:
    img=cv2.imread('assets/lambo.jpg')
    img=cv2.resize(img,(300,250))

    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos('Hue Min','Tracker')
    h_max=cv2.getTrackbarPos('Hue Max','Tracker')
    s_min=cv2.getTrackbarPos('Satu Min','Tracker')
    s_max=cv2.getTrackbarPos('Satu Max','Tracker')
    v_min=cv2.getTrackbarPos('val Min','Tracker')
    v_max=cv2.getTrackbarPos('val Max','Tracker')
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])

    mask=cv2.inRange(imgHSV,lower,upper)
    imgresult=cv2.bitwise_and(img,img,mask=mask)
    stackimg=stackImages(0.6,([img,imgHSV],[mask,imgresult]))

    # cv2.imshow('normal img',img)
    # cv2.imshow('Hsv img',imgHSV)
    # cv2.imshow('mask',mask)
    # cv2.imshow('imgresult',imgresult)
    cv2.imshow('stackimg',stackimg)

    if cv2.waitKey(1) & 0xFF ==13:
        break