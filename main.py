import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)                #detectionCon is detection confidence which is used for the accuracy of detection of hand                       #

while True:
    success ,img = cap.read()
    img= detector.findHands(img)                         #used for detection of the hands and to form the lines in the hands for tracking
    lmList,bboxInfo = detector.findPosition(img)         #used to create a single bounding box in the image where the hands are visible
                                                         #lmList is landmark and bboxInfo is bounding box info

    cv2.imshow("Image",img)
    cv2.waitKey(1)