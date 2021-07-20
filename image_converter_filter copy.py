#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from cv_bridge import CvBridge, CvBridgeError

pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
vel = Twist()
forward_dist=0
left_dist=0
right_dist=0

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera
    rospy.Subscriber("scan", LaserScan, self.callback_scan)

  def callback_scan(self,data):
    global forward_dist
    global left_dist
    global right_dist
    forward_dist=data.ranges[360]
    left_dist=data.ranges[719]
    right_dist=data.ranges[0]

  def callback(self,data):
    global forward_dist
    global left_dist
    global right_dist

    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    lower =(0, 0, 0) # lower bound for each channel
    upper = (55, 35, 80)
    mask = cv2.inRange(cv_image, lower, upper) # mask = 0_1	
    right = mask[:, 391:639]
    center = mask[:, 250:390]
    left = mask[:, 0:249]
    if (np.sum(right) >= np.sum(left) and np.sum(right) >= np.sum(center)):
      vel.angular.z = 0.15
      print('right', np.sum(right))
      print("forward: ", forward_dist)
      
    if (np.sum(left) > np.sum(right) and np.sum(left) > np.sum(center)):
      vel.angular.z = -0.15
      print('left', np.sum(left))
      print("forward: ", forward_dist)

    if (np.sum(center) > np.sum(right) and np.sum(center) > np.sum(left)):
      if(forward_dist>0.5):
        vel.linear.x = 0.20
      else:
        vel.linear.x = 0
        vel.angular.z = 0
      print("forward: ", forward_dist)
      print('center', np.sum(center))

    
    cv2.imshow("Image window", cv_image)
    cv2.imshow("Filter", mask)
    pub.publish(vel)
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)