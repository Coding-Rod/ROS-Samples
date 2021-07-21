#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import numpy as np
from sympy import *
import tf
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
vel = Twist()
state = 0
rotate = False
class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera
    rospy.Subscriber("odom", Odometry, self.callbackodom)

  def callbackodom(self,data):
    self.x=data.pose.pose.position.x
    self.y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    self.yaw=euler[2] 

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    global state
    global rotate
    lower =(0, 0, 20) # lower bound for each channel
    upper = (50, 50, 80)
    mask = cv2.inRange(cv_image, lower, upper) # mask = 0_1	
    
    # First
    if state == 0:
      if self.x > -1:
        vel.linear.x = 0.25
      else:
        vel.linear.x = 0
        print("sum:"+str(np.sum(cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY))))
        state = 1

    if state == 1:
      if self.x >0:
        vel.linear.x = -0.25
      else:
        vel.linear.x = 0
        state = 2
        
    if state == 2:
      if self.yaw > -1.37:
        vel.angular.z = 0.2
      if self.yaw > -1.47:
        vel.angular.z = 0.1
      elif self.yaw > -1.57:
        vel.angular.z = 0.01
      else:
        state = 0

    cv2.imshow("Image window", cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY))
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


