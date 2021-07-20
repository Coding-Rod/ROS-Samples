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
from cv_bridge import CvBridge, CvBridgeError

pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
vel = Twist()

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    lower =(0, 0, 20) # lower bound for each channel
    upper = (50, 50, 80)
    mask = cv2.inRange(cv_image, lower, upper) # mask = 0_1	
    right = mask[:, 320:639]
    left = mask[:, 0:319]
    if (np.sum(right) >= np.sum(left)):
      vel.angular.z = 0.2
      print('right', np.sum(right))
      
    else:
      vel.angular.z = -0.2
      print('left', np.sum(left))
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
