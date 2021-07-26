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
from nav_msgs.msg import Odometry
import tf

state = 0
class detect:
  def __init__(self):
    self.bridge = CvBridge()
    self.vel = Twist()

    self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

    self.laser_sub = rospy.Subscriber("odom", Odometry, self.callback_odom)
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback) # topic from camera

  def callback_odom(self,data):
      self.x=data.pose.pose.position.x
      self.y=data.pose.pose.position.y
      euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
      self.yaw=euler[2] 
  def callback(self,data):
    global state
    print("state: ",state)
    print("x: ",self.x)
    print("y: ",self.y)
    # Detect green
    if state == 0:
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        self.vel.angular.z = 0.5

        # green mask
        lower3 = np.array([36,25,25]) 
        upper3 = np.array([86,255,255])
        mask3 = cv2.inRange(hsv, lower3, upper3) # mask = 0_3	
        centre3 = mask3[:,260:380]
        max_malue3 = np.sum(centre3)

        aux = mask3[0:100,260:380]
        print(state)
        state = 1 if max_malue3 > 1600000 else 0

        cv2.imshow("Image", cv_image)
        cv2.imshow("Centre", centre3)
        print("max_malue3: ",max_malue3 )
        # cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)
        if state == 1:
            self.vel.angular.z = 0
            print('detected')
        self.pub.publish(self.vel)
    # Go Outside
    if state == 1:
      try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      except CvBridgeError as e:
        print(e)

      hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

      lower_white = np.array([0,0,150], dtype=np.uint8)
      upper_white = np.array([0,0,255], dtype=np.uint8)

      mask = cv2.inRange(hsv, lower_white, upper_white)
    
      percentage=cv2.countNonZero(mask)

      mask = mask[mask.shape[0]/4:,:]
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
      
      cv2.imshow("Image window", cv_image)
      # cv2.imshow("Right Mask", right)
      # cv2.imshow("Left Mask", left)
      cv2.imshow("Centre Mask", centre)
      cv2.waitKey(3)
      self.pub.publish(self.vel)
      state = 2 if ((self.x<-3.25 or self.x>3.25) or (self.y<-3.25 and self.y>3.25)) else 1
    # Go green
    if state == 2:
      try:
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      except CvBridgeError as e:
        print(e)

      hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

      lower3 = np.array([36,25,25]) 
      upper3 = np.array([86,255,255])
      mask = cv2.inRange(hsv, lower3, upper3) # mask = 0_3	
    
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
      if(np.sum(mask) == 0):
        self.vel.linear.x=0
      
      cv2.imshow("Image window", cv_image)
      # cv2.imshow("Right Mask", right)
      # cv2.imshow("Left Mask", left)
      cv2.imshow("Centre Mask", centre)
      cv2.waitKey(3)
      self.pub.publish(self.vel)
    

def main(args):
  rospy.init_node('second_test', anonymous=True)
  detect()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)