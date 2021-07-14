#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import numpy as np
from sensor_msgs.msg import LaserScan

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
pub_filter = rospy.Publisher('filter', Int32, queue_size=1)
vel=Twist()

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback)
  

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    (rows,cols,channels) = cv_image.shape
    ## convert to hsv
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    
    mask1 = cv2.inRange(hsv, (0, 50, 50), (30, 200,200))

    mask2 = cv2.inRange(hsv, (150,50,50), (180, 200, 200))

    ## final mask and masked
    #mask = cv2.bitwise_or(mask1, mask2)
    #target = cv2.bitwise_and(cv_image,cv_image, mask=mask)
    #lower_red=np.array([0,0,27])  Hidrante Rojo
    #upper_red=np.array([5,5,40])  Hidrante ROjo
    lower_red=np.array([30,101,30])  
    upper_red=np.array([32,103,32])  
    redmask=cv2.inRange(cv_image,lower_red,upper_red)
    target2= cv2.bitwise_and(cv_image,cv_image, redmask)
    percentage=np.sum(redmask)/(redmask.shape[0]*redmask.shape[1])*100
    print (percentage)
    #left=np.sum(mask[:,0:cols/2])
    #right=np.sum(mask[:,cols/2:cols])
    


    cv2.imshow("Image window", redmask)
    cv2.waitKey(3)
    pub_filter.publish(int(percentage))
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('simple_filter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
