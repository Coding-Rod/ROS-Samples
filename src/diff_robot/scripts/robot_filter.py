#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String , Float64
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

import numpy as np

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
vel=Twist()

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback)
    self.scan_sub = rospy.Subscriber("scan", LaserScan, self.callback_scan)
    self.scan_sub = rospy.Subscriber("center", Float64, self.callback_center)
    self.center=0

  def callback_center(self, data):
    self.center=data.data

  def callback_scan(self, data):
    #rospy.loginfo( "Angle max %f", data.angle_max)
    Angle_max=data.angle_max
    #rospy.loginfo( "Angle min %f", data.angle_min)
    Angle_min=data.angle_min
    #rospy.loginfo( "Angle increment %f", data.angle_increment)
    Angle_increment=data.angle_increment
    #rospy.loginfo( "Samples %f", (Angle_max-Angle_min)/Angle_increment)
    Samples=(Angle_max-Angle_min)/Angle_increment
    current_distance=data.ranges[0]
    min_distance=10000
    for i in range (1,int(Samples)+1):
	if data.ranges[i] < min_distance:
	    min_distance=data.ranges[i]
	current_distance=data.ranges[i]
    rospy.loginfo( "Min distance %f", min_distance)
    rospy.loginfo( "Central distance %f", data.ranges[int(Samples/2)])

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    (rows,cols,channels) = cv_image.shape
    ## convert to hsv
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, (0, 50, 30), (30, 255,255))
    mask2 = cv2.inRange(hsv, (170,50,30), (200, 255, 255))

    ## final mask and masked
    mask = cv2.bitwise_or(mask1, mask2)
    target = cv2.bitwise_and(cv_image,cv_image, mask=mask)
    left=np.sum(mask[:,0:cols/2])
    right=np.sum(mask[:,cols/2:cols])
    if self.center<0.5: 
        print("object is left")
	vel.angular.z=-0.4*(0.5-self.center)
	vel.linear.x=0
    else:
        print("object is right")
        vel.angular.z=0.4*(self.center-0.5)
	vel.linear.x=0


    pub.publish(vel)

    cv2.imshow("Image window", target)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
