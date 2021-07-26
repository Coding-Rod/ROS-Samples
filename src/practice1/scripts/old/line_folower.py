#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist


class Image_object_tracker:
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) #topic from camera
    self.red_mask = rospy.Subscriber("mask", Int32, self.mask_callback)
    self.pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
    self.cont=rospy.Publisher('hydrants', Int32, queue_size=1)
    self.vel=Twist()
    self.m_decision = 0
    self.red = 0
    self.prev_red = 0
    self.counter = 0
    self.verif = 0
    self.flag = False
  
  def mask_callback(self, data):
    self.prev_red = self.red
    self.red = data.data

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    hsv_image=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
    lower =(90, 50, 70) 
    upper = (128, 255, 255)
    mask = cv2.inRange(hsv_image, lower, upper) # mask = 0_1    
    percentage=cv2.countNonZero(mask)

    right = mask[:,380:639] 
    left = mask[:,0:260]
    centre = mask[:,260:380]
      
    if (np.sum(centre)>np.sum(right)  and np.sum(centre)>np.sum(left) ):
      self.vel.angular.z = 0.5
    else:
      if (np.sum(right) >= np.sum(left)):
        self.vel.angular.z = 0.5
      else:
        self.vel.angular.z = -0.5

    self.vel.linear.x = 0.5

    if(self.flag):
      self.verif += 1
      self.vel.linear.x =0.2
      print(self.verif)
      if(self.verif > 200):
        self.flag = False
        self.verif = 0

    if(self.prev_red == 1 and self.red == 0 and not self.flag):
      self.counter += 1
      self.flag = True
    
    if(np.sum(mask) == 0):
      self.vel.linear.x = 0
      self.vel.angular.z = 0
    cv2.imshow("Image window", cv_image)
    # cv2.imshow("Right Mask", right)
    # cv2.imshow("Left Mask", left)
    cv2.imshow("Centre Mask", centre)
    cv2.waitKey(3)
    self.pub.publish(self.vel)
    self.cont.publish(self.counter)

def main(args):
  robot_tracker = Image_object_tracker()
  rospy.init_node('line_folower', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)