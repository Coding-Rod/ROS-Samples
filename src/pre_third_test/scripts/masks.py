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
    self.max_value = rospy.Publisher("mask",Int32,queue_size=10) # topic from camera
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback) # topic from camera

  def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        # blue_mask
        lower =(80, 0, 0) # lower bound for each channel
        upper = (250, 80, 80)
        mask1 = cv2.inRange(cv_image, lower, upper) # mask = 0_1	
        total1 = mask1[:, 0:639]
        total_mask = np.array([np.sum(total1)])
        max_malue1 = np.max(total_mask)

        # green_mask
        lower =(36,25,25) # lower bound for each channel
        upper = (86,255,255)
        mask2 = cv2.inRange(cv_image, lower, upper) # mask = 0_1	
        total2 = mask2[:, 0:639]
        total_mask = np.array([np.sum(total2)])
        max_malue2 = np.max(total_mask)

        print(max_malue1)
        print(max_malue2)
        print()
        if max_malue1 > 0 or max_malue2 > 0:
            self.max_value.publish(1 if max_malue1 > max_malue2 else 2)
        
        cv2.imshow("Image window", cv_image)
        cv2.imshow("Filter blue", total1)
        cv2.imshow("Filter green", total2)
        cv2.waitKey(3)

def main(args):
    ic = image_converter()
    rospy.init_node('masks', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)