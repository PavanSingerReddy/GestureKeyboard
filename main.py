import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)                #detectionCon is detection confidence which is used for the accuracy of detection of hand                       #


class Button():
    def __init__(self,pos,text,size = [100,100]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self,img):
        x,y = self.pos
        w,h = self.size

        print("pos : ",self.pos)
        print("size : ",self.size)

        cv2.rectangle(img,(x,y), (x+w, y+h), (75, 74, 76), cv2.FILLED)
        cv2.putText(img, self.text, (x+25, y+65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)

        return img



myButton = Button([100,100],"Q")



while True:
    success ,img = cap.read()
    img= detector.findHands(img)                         #used for detection of the hands and to form the lines in the hands for tracking
    lmList,bboxInfo = detector.findPosition(img)         #used to create a single bounding box in the image where the hands are visible
                                                         #lmList is landmark and bboxInfo is bounding box info

    img = myButton.draw(img)



    cv2.imshow("Image",img)
    cv2.waitKey(1)