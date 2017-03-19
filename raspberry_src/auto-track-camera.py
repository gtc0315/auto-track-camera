#import necessary libraries
import numpy as np
import math
import cv2
import time 
import RPi.GPIO as GPIO   
from picamera import PiCamera
from picamera.array import PiRGBArray                                                          

#declare the GPIO output pins based on BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

#create masks for convenience
chanX_list = (13,19,20)
chanY_list = (10,9,11)

#the resolution of the piCamera
resolutionX = 640
resolutionY = 480

#predefined haar cascade classifiers (face, 45 degree side face, eye)
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_alt.xml')
profileface_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_eye.xml')

#create piCamera module, set the resolution, framerate and rotation
camera = PiCamera()
camera.resolution = (resolutionX,resolutionY)
camera.framerate = 40
camera.rotation = 270

#extract the raw data from camera module for a faster face detection computation
rawCapture = PiRGBArray(camera, size=(resolutionX, resolutionY))

#Camera warm-up time
time.sleep(0.1)

#initialize the previous pixel differences and previous time
prevdeltaX = 0
prevdeltaY = 0
prevTime = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	#initialize flags
	hasFace = 0
	largestFace = 0
	faceSize = 0
	
	#grab the raw frame array and create gray image for face detection 
	image = frame.array
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#find faces with parameters (1.3 scaling and 4 neighbors)
	faces = face_cascade.detectMultiScale(gray, 1.3, 4)
	
	#check if front face exists
	if len(faces)==0:
                #find right side faces with parameters (1.3 scaling and 4 neighbors)
                faces = profileface_cascade.detectMultiScale(gray, 1.3, 4)
                
                #check if right side face exists
                if len(faces)==0:
                        #find left side faces using right side face cascade and flipped image
                        faces = profileface_cascade.detectMultiScale(cv2.flip(gray,1), 1.3, 4)

                        #check if left side face exists
                        if len(faces)==0:
                                #indicate there is no face
                                hasFace = 0
                        else:
                                #translate the location of faces from flipped image to normal image
                                for i in range(0,len(faces)):
                                        faces[i][0] = resolutionX - faces[i][0] - faces[i][2]
                                hasFace = 1
                else:
                        hasFace = 1
	else:
                hasFace = 1                
                                
        
	if hasFace==1:
                #find the largest face by comparing the sums of length and width of face
                for j in range(0,len(faces)):
                       if  (faces[j][2]+faces[j][3])>faceSize:
                               faceSize = faces[j][2]+faces[j][3]
                               largestFace = j

                #choose the largest face for following computation
                #(x,y) represents the left top corner of the face, (w,h) represents the width and the height of the face
                x = faces[largestFace][0]
                y = faces[largestFace][1]
                w = faces[largestFace][2]
                h = faces[largestFace][3]
                
                #calculate the distance between the center of the face and the center of the image in term of pixel
                deltaX = round(x+w/2) - resolutionX/2
                deltaY = round(y+h/2) - resolutionY/2

                #calculate the difference between the pixel distance in current iteration and the pixel distance in previous iteration
                diffX = deltaX - prevdeltaX
                diffY = deltaY - prevdeltaY

                #the PD controller

                distX = 0.7*abs(deltaX) + 0.3*abs(diffX)
                distY = 0.7*abs(deltaY) + 0.3*abs(diffY)

                #update the previous pixel distance
                prevdeltaX = deltaX
                prevdeltaY = deltaY

                #encode the direction (4 directions: --, -+, +-, ++) of the motor movement into two Bit GPIO signal and one interrupt signal
                if deltaX>0 and deltaY>0: #--
                        GPIO.output(5,GPIO.HIGH)
                        GPIO.output(6,GPIO.HIGH)
                        GPIO.output(21,not GPIO.input(21)) #toggle
                elif deltaX>0 and deltaY<0: #-+
                        GPIO.output(5,GPIO.HIGH)
                        GPIO.output(6,GPIO.LOW)
                        GPIO.output(21,not GPIO.input(21)) #toggle
                elif deltaX<0 and deltaY>0: #+-
                        GPIO.output(5,GPIO.LOW)
                        GPIO.output(6,GPIO.HIGH)
                        GPIO.output(21,not GPIO.input(21)) #toggle
                elif deltaX<0 and deltaY<0: #++
                        GPIO.output(5,GPIO.LOW)
                        GPIO.output(6,GPIO.LOW)
                        GPIO.output(21,not GPIO.input(21)) #toggle

                #quantize and encode the x-axis pixel distance into 8 levels
                if distX>(resolutionX/2):
                        GPIO.output(chanX_list,(GPIO.HIGH,GPIO.HIGH,GPIO.HIGH))
                elif distX>200:
                        GPIO.output(chanX_list,(GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                elif distX>100:
                        GPIO.output(chanX_list,(GPIO.HIGH,GPIO.LOW,GPIO.HIGH))
                elif distX>60:
                        GPIO.output(chanX_list,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                elif distX>40:
                        GPIO.output(chanX_list,(GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                elif distX>20:
                        GPIO.output(chanX_list,(GPIO.LOW,GPIO.HIGH,GPIO.LOW))
                elif distX>10:
                        GPIO.output(chanX_list,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                else:
                        GPIO.output(chanX_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

                #quantize and encode the y-axis pixel distance into 8-level servo speed/step
                if distY>(resolutionY/2):
                        GPIO.output(chanY_list,(GPIO.HIGH,GPIO.HIGH,GPIO.HIGH))
                elif distY>200:
                        GPIO.output(chanY_list,(GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
                elif distY>100:
                        GPIO.output(chanY_list,(GPIO.HIGH,GPIO.LOW,GPIO.HIGH))
                elif distY>60:
                        GPIO.output(chanY_list,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))
                elif distY>40:
                        GPIO.output(chanY_list,(GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
                elif distY>20:
                        GPIO.output(chanY_list,(GPIO.LOW,GPIO.HIGH,GPIO.LOW))
                elif distY>10:
                        GPIO.output(chanY_list,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))
                else:
                        GPIO.output(chanY_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

                #draw the box for target face
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
	else:
                #set the servo speed/step to 0
                GPIO.output(chanX_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))
                GPIO.output(chanY_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))

        #the following two lines are used to calculate the elapsed time of each iteration
	#print(repr(time.time()-prevTime))
	#prevTime = time.time()
                
	#show the frame with timestamp
	cv2.putText(image,str(time.ctime()),(20,resolutionY-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
	#save the image to the path for streaming
	cv2.imwrite('/home/pi/stream/pic.jpg',image)
	cv2.imshow("Frame", image)
	#intialize key interrupt
	key = cv2.waitKey(1) & 0xFF
 
	#clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	#if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

#set the servo speed/step to 0
GPIO.output(chanX_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))
GPIO.output(chanY_list,(GPIO.LOW,GPIO.LOW,GPIO.LOW))
#clean GPIO
GPIO.cleanup()
