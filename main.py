import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from time import sleep

cap = cv2.VideoCapture(0)                                                   #captures video

cap.set(3,1280)                                                             # sets the width of the video
cap.set(4,720)                                                              # sets the height of the video

detector = HandDetector(detectionCon=0.8)                                   #detectionCon is detection confidence which is used for the accuracy of detection of hand                       #

keys = [["Q","W","E","R","T","Y","U","I","O","P"],                          # Keys for the keyboard to display
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""

def drawALL(img,buttonList):                                                                                    #This function draws all the keys in the keyboard
    for button in buttonList:
        x,y = button.pos                                                                                        # assigning the values of x and y from the postion
        w,h = button.size                                                                                       # initializing the width and height of the button
        cv2.rectangle(img,(x,y), (x+w, y+h), (75, 74, 76), cv2.FILLED)                                          # drawing the rectangle for the button
        cv2.putText(img, button.text, (x+25, y+65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)      # drawing the inner text of the button
    return img                                                                                                  # returning the image after the drawing of the buttons


class Button():                                                 #Class for the button to store the information about button
    def __init__(self,pos,text,size = [100,100]):               # button initialization with different parameters
        self.pos = pos                                          # initializing x and y positions of the key
        self.size = size                                        # initializing the size of the key
        self.text = text                                        #initializing the inner text of the key
        self.pos[0] = math.floor(self.pos[0])                   # converting the float value of pos[0] into the integer value
        self.pos[1] = math.floor(self.pos[1])                   # converting the float value of pos[1] into the integer value



buttonList = []

x_axis_keys_distance = 1.1                                      #distance of x-axis between two adjacent horizontal keys
y_axis_keys_distance = 1.1                                      #distance of y-axis between two adjacent vertical keys

for i in range(len(keys)) :
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j*x_axis_keys_distance + 50, 100*i*y_axis_keys_distance+50], key))



while True:
    success ,img = cap.read()
    img= detector.findHands(img)                         #used for detection of the hands and to form the lines in the hands for tracking
    lmList,bboxInfo = detector.findPosition(img)         #used to create a single bounding box in the image where the hands are visible
                                                         #lmList is landmark and bboxInfo is bounding box info

    img = drawALL(img,buttonList)                        #This function draws all the keys in the keyboard


    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            # print(lmList[8])

            if x < lmList[8][0] < x+w and y < lmList[8][1]<y+h:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),cv2.FILLED)  # drawing the rectangle for the button
                cv2.putText(img, button.text, (x + 25, y + 65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)
                distance,_,_ = detector.findDistance(8,12,img,draw=False)              #refer this document for index finger and middle finger points
                # print(distance)

                #when index and middle finger are touched the below code runs
                if distance < 35:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255),
                                  cv2.FILLED)  # drawing the rectangle for the button
                    cv2.putText(img, button.text, (x + 25, y + 65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255),
                                3)
                    finalText+=button.text
                    sleep(0.2)       #decreasing the touch sensitivity


    cv2.rectangle(img, (100,400), (900,500), (175,0,175), cv2.FILLED)  # drawing the rectangle for the button
    cv2.putText(img,finalText, (110,475), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)


    cv2.imshow("Image",img)                              # displays the image
    cv2.waitKey(1)                                       # waits for onesecond to display the image