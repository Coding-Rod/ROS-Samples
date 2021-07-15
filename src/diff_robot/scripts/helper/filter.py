#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import Int32
import numpy as np
from sensor_msgs.msg import LaserScan
from matplotlib import pyplot as plt

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
pub_filter = rospy.Publisher('filter', Point, queue_size=1)
vel=Twist()

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)
  

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    (rows,cols,channels) = cv_image.shape

#bluemask


    lower_red=np.array([0,0,102])
    upper_red=np.array([0,0,121])
    redmask=cv2.inRange(cv_image,lower_red,upper_red)
    target1= cv2.bitwise_and(cv_image,cv_image, redmask)
    percentage=np.sum(redmask)/(redmask.shape[0]*redmask.shape[1])*100

    lower_g=np.array([0,102,0]) 
    upper_g=np.array([0,122,0])
    gmask=cv2.inRange(cv_image,lower_g,upper_g)
    target2= cv2.bitwise_and(cv_image,cv_image, gmask)
    gpercentage=np.sum(gmask)/(gmask.shape[0]*gmask.shape[1])*100


    print ("red: ",percentage)
    print ("green: ",gpercentage)

    #para ver colores bgr pasar a rgb
    #plt.imshow(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))  
    #plt.draw() 
    #plt.show() 

    cv2.imshow("Image window", gmask)
    cv2.imshow("Image window", redmask)
    cv2.waitKey(3)
    percent=Point()
    percent.y =percentage
    percent.z=gpercentage
    pub_filter.publish(percent)
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
