import cv2
import numpy as np 
from pynput.keyboard import Key, Controller
cap=cv2.VideoCapture(0)
keyboard=Controller()

while True:
    _,frame=cap.read()
    hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    low_black=np.array([0,0,0])
    high_black=np.array([180,255,30])
    mask=cv2.inRange(hsv_frame,low_black,high_black)
    mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)
    black_center=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.rectangle(frame,(0,0),(212,240),(0,255,0),2)
    cv2.putText(frame, "A", (106,120),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,(212,0),(424,240),(0,255,0),2)
    cv2.putText(frame, "Up", (318,120),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,(424,0),(640,240),(0,255,0),2)
    cv2.putText(frame, "B", (530,120),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,(0,240),(212,480),(0,255,0),2)
    cv2.putText(frame, "Lft", (106,360),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,(212,240),(424,480),(0,255,0),2)
    cv2.putText(frame, "Dwn", (318,360),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,(424,240),(640,480),(0,255,0),2)
    cv2.putText(frame, "Rgt", (530,360),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if len(black_center)>0:
        black_area=max(black_center, key=cv2.contourArea)
        (x,y,w,h)=cv2.boundingRect(black_area)
        M = cv2.moments(black_area)
        if M["m00"] == 0: 
            center = (int(M["m10"]), int(M["m01"]))
        else :
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        cv2.putText(frame, "black rabbit", (center[0]-20,center[1]-20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        if center[0]<212 :  
            if center[1]<240 :
                #print("A")
                keyboard.press("z")
                #keyboard.release("z")
            else:
                #print("Left")
                keyboard.press(Key.left)
                keyboard.release(Key.left)
        elif center[0]<424:
            if center[1]<240:
                #print("Up")
                keyboard.press(Key.up)
                keyboard.release(Key.up)
            else:
                #print("Down")
                keyboard.press(Key.down)
                keyboard.release(Key.down)
        elif center[0]>=424:
            if center[1]<240:
                #print("B")
                keyboard.press("X")
                keyboard.release("X")
            else:
                #print("Right")
                keyboard.press(Key.right)
                keyboard.release(Key.right)
    cv2.imshow("Frame",frame)
    #cv2.imshow("mask",mask)

    key=cv2.waitKey(1)
    if key == 27 :
        break
cv2.destroyAllWindows()

