import cv2
import math
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
import numpy as np
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)                                                                                                                                                                       #captures video

cap.set(3,1280)                                                                                                                                                                                 # sets the width of the video
cap.set(4,720)                                                                                                                                                                                  # sets the height of the video

detector = HandDetector(detectionCon=0.8)                                                                                                                                                       #detectionCon is detection confidence which is used for the accuracy of detection of hand                       #

keys = [["Q","W","E","R","T","Y","U","I","O","P"],                                                                                                                                              # Keys for the keyboard to display
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""                                                                                                                                                                                  # text to be displayed in the box when a button is pressed

keyboard = Controller()                                                                                                                                                                         # gives us access to the actual keyboard

#bold coloured key generation function

# def drawAll(img,buttonList):                                                                                                                                                                   #This function draws all the keys in the keyboard
#     for button in buttonList:
#         x,y = button.pos                                                                                                                                                                        # assigning the values of x and y from the postion
#         w,h = button.size                                                                                                                                                                       # initializing the width and height of the button
#         cv2.rectangle(img,(x,y), (x+w, y+h), (75, 74, 76), cv2.FILLED)                                                                                                                          # drawing the rectangle for the button
#         cv2.putText(img, button.text, (x+25, y+65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)                                                                                      # drawing the inner text of the button
#     return img                                                                                                                                                                                  # returning the image after the drawing of the buttons



#transparent colored key generation function

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)           # blank image
    for button in buttonList:                       # iterating through all buttons
        x, y = button.pos                           # copying x and y values of position
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),25, rt=0)                                                                                         #creating green colored corner lines for the keys
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),(75, 74, 76), cv2.FILLED)                                                                                       #creating button
        cv2.putText(imgNew, button.text, (x + 40, y + 60),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)                                                                                           #inner text of the button

    out = img.copy()                                                                                                                                                                               #copying the original video image to out
    alpha = 0.5                                                                                                                                                                                    # setting alpha channel for opacity
    mask = imgNew.astype(bool)                                                                                                                                                                     # setting mask for the output image
    # print(mask.shape)                                                                                                                                                                            # prints the shape of the mask
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]                                                                                                                            # The addWeighted function is a function that helps in adding two images and also blending those by passing the alpha, beta and gamma values. In order to analyse images, this helps in adjusting the gradients and in the processing of the image. The blending of the images depends on alpha and beta values which are passed as arguments to this function.
    return out                                                                                                                                                                                     # returning the final output image




class Button():                                                                                                                                                                                     #Class for the button to store the information about button
    def __init__(self,pos,text,size = [100,100]):                                                                                                                                                   # button initialization with different parameters
        self.pos = pos                                                                                                                                                                              # initializing x and y positions of the key
        self.size = size                                                                                                                                                                            # initializing the size of the key
        self.text = text                                                                                                                                                                            #initializing the inner text of the key
        self.pos[0] = math.floor(self.pos[0])                                                                                                                                                       # converting the float value of pos[0] into the integer value
        self.pos[1] = math.floor(self.pos[1])                                                                                                                                                       # converting the float value of pos[1] into the integer value



buttonList = []                                                                                                                                                                                       # list of the buttons are appended in this after creating buttons

x_axis_keys_distance = 1.1                                                                                                                                                                            #distance of x-axis between two adjacent horizontal keys
y_axis_keys_distance = 1.1                                                                                                                                                                            #distance of y-axis between two adjacent vertical keys

for i in range(len(keys)) :                                                                                                                                                                           # iterating over each row of the buttons
    for j, key in enumerate(keys[i]):                                                                                                                                                                 # iterating over each column of the buttons
        buttonList.append(Button([100 * j*x_axis_keys_distance + 50, 100*i*y_axis_keys_distance+50], key))                                                                                            #appending new buttons to the buttonlist



while True:
    success ,img = cap.read()                                                                                                                                                                          # reads the image from the video camera
    img= detector.findHands(img)                                                                                                                                                                       #used for detection of the hands and to form the lines in the hands for tracking
    lmList,bboxInfo = detector.findPosition(img)                                                                                                                                                       #used to create a single bounding box in the image where the hands are visible
                                                                                                                                                                                                       #lmList is landmark and bboxInfo is bounding box info

    img = drawAll(img,buttonList)                                                                                                                                                                      #This function draws all the keys in the keyboard


    if lmList:                                                                                                                                                                                         #checking the condition if the hand exist in the image
        for button in buttonList:                                                                                                                                                                      # iterating through all the buttons in the button list
            x,y = button.pos                                                                                                                                                                           # copying the value of the starting position of the button
            w,h = button.size                                                                                                                                                                          # copying the values of the size of the button

            if x < lmList[8][0] < x+w and y < lmList[8][1]<y+h:                                                                                                                                        # checking condition in which button the index key lies on
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),cv2.FILLED)                                                                                                                     # drawing the green rectangle for the button when it is in contact with index button
                cv2.putText(img, button.text, (x + 25, y + 65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)                                                                                 # text inside the green button
                distance,_,_ = detector.findDistance(8,12,img,draw=False)                                                                                                                              #refer this document for index finger and middle finger points : https://google.github.io/mediapipe/solutions/hands.html
                                                                                                                                                                                                       #findDistance function finds the distance between the given two points of the hand

                #when index and middle finger are touched the below code runs
                if distance < 35:                                                                                                                                                                       #checking if the index finger and the middle finger is touched and calculating its area
                    keyboard.press(button.text)                                                                                                                                                         # it writes the button which is pressed to the notepad or other applications
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255),                                                                                                                             # if index finger and middle finger are touched then changing the button color to red
                                  cv2.FILLED)  # drawing the rectangle for the button
                    cv2.putText(img, button.text, (x + 25, y + 65), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255),3)                                                                               # text inside the red button
                    finalText+=button.text                                                                                                                                                              # writing the pressed button inside the rectangular box
                    sleep(0.2)                                                                                                                                                                          #decreasing the touch sensitivity


    cv2.rectangle(img, (40,400), (1200,500), (118,116,108), cv2.FILLED)                                                                                                                                 # drawing the rectangle or long box for showing the output of the key pressed
    cv2.putText(img,finalText, (50,475), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 255, 255), 3)                                                                                                         # drawing the key which was pressed inside the rectangle


    cv2.imshow("Image",img)                                                                                                                                                                             # displays the image of the video
    cv2.waitKey(1)                                                                                                                                                                                      # waits for onesecond to display the image