#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String, Int32
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

state = 0
class detect:
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera
    self.max_value = rospy.Publisher("mask",Int32,queue_size=1) # topic from camera
    self.stt = rospy.Publisher("state",Int32,queue_size=1)

  def callback(self,data):
    global state
    if state == 0:
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # red mask
        lower1 = np.array([0, 99, 21])
        upper1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower1, upper1) # mask = 0_1	
        centre1 = mask1[:,260:380]
        max_malue1 = np.max(centre1)/255

        # blue mask
        lower2 =(90, 50, 50) 
        upper2 = (128, 255, 255)
        mask2 = cv2.inRange(hsv, lower2, upper2) # mask = 0_1    
        centre2 = mask2[:,260:380]
        max_malue2 = np.max(centre2)/255

        # green mask
        lower3 = np.array([36,25,25]) 
        upper3 = np.array([86,255,255])
        mask3 = cv2.inRange(hsv, lower3, upper3) # mask = 0_3	
        centre3 = mask3[:,260:380]
        max_malue3 = np.max(centre3)/255

        self.max_value.publish()
        state = max_malue1+max_malue2*2+max_malue3*3
        
        cv2.imshow("Image", cv_image)
        cv2.imshow("Centre", centre1+centre2+centre3)
        print("max_malue1: ",max_malue1 )
        print("max_malue2: ",max_malue2 )
        print("max_malue3: ",max_malue3 )
        # cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)
        self.stt.publish(state)

def main(args):
  rospy.init_node('detector', anonymous=True)
  detect()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)