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

class image_converter:
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera
    self.max_value = rospy.Publisher("mask",Int32,self.callback) # topic from camera



  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    # lower =(80, 0, 0) # lower bound for each channel
    # upper = (250, 80, 80)
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 101, 21])
    upper1 = np.array([10, 254, 253])
    mask = cv2.inRange(hsv, lower1, upper1) # mask = 0_1	
    total = mask[:, 0:639]
    total_mask = np.array([np.sum(total)])
    max_malue = np.max(total_mask)

    print('max_malue: ', max_malue)
    if (max_malue >= 1500000 and max_malue <= 15000000):
      self.max_value.publish(1)
    
    cv2.imshow("Image window", cv_image)
    cv2.imshow("Filter", mask)
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('red_mask', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)