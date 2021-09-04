





import cv2
import random
from pytesseract import pytesseract
from pytesseract import Output
#############################################
frameWidth = 640
frameHeight = 480
nPlateCascade = cv2.CascadeClassifier("assets/haarcascade_russian_plate_number.xml")
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
minArea = 200
color = (0,255,0)
###############################################
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)


while True:
    success, img = cap.read()
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10)
    # print(numberPlates)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area >minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            
            imgRoi = img[y:y+h,x:x+w]
            # image = cv2.imread(imgRoi)
            image_data = pytesseract.image_to_string(imgRoi)
            print(image_data)
            cv2.rectangle(img,(x-10,y),(x+250,y-30),(0,0,0),cv2.FILLED)
            cv2.putText(img,image_data,(x,y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,color,1)
            cv2.imshow("ROI",imgRoi)

    cv2.imshow("Result", img)
    

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Scanned/NoPlate_"+str(random.randint(1000, 100000))+".jpg",imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_DUPLEX,
                    2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        