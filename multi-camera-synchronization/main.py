#Thanks to Toptechboy
#https://toptechboy.com/ai-on-the-jetson-nano-lesson-46-synchronizing-multiple-cameras-with-opencv/

from threading import Thread
import cv2
import time
import numpy as np

class vStream:
    def __init__(self,src,width,height):
        self.width=width
        self.height=height
        self.capture=cv2.VideoCapture(src)
        self.thread=Thread(target=self.update,args=())
        self.thread.daemon=True
        self.thread.start()
    def update(self):
        while True:
            _,self.frame=self.capture.read()
            self.frame2=cv2.resize(self.frame,(self.width,self.height))
    def getFrame(self):
        return self.frame2
flip=2
dispW=640
dispH=480
cam1=vStream(0,dispW,dispH)
cam2=vStream(1,dispW,dispH)
font=cv2.FONT_HERSHEY_SIMPLEX
startTime=time.time()
dtav=0
while True:
    try:
        myFrame1=cam1.getFrame()
        myFrame2=cam2.getFrame()
        myFrame3=np.hstack((myFrame1,myFrame2))
        dt=time.time()-startTime
        startTime=time.time()
        dtav=.9*dtav+.1*dt
        fps=1/dtav
        cv2.rectangle(myFrame3,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(myFrame3,str(round(fps,1))+' fps',(0,25),font,.75,(0,255,255),2)
        cv2.imshow('ComboCam',myFrame3)
        cv2.moveWindow('ComboCam',0,0)



    except:
        print('frame not available')
        
    if cv2.waitKey(1)==ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)
        break