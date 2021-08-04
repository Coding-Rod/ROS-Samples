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
        
        short_image = cv_image[int(cv_image.shape[0]*0.4):int(cv_image.shape[0]*0.6),int(cv_image.shape[1]*0.4):int(cv_image.shape[1]*0.6)]
        values = [np.sum(short_image[:,:,0]),np.sum(short_image[:,:,1]),np.sum(short_image[:,:,2])]
        colors = ['Blue', 'Green', 'Red']
        colors_rgb = ['Red', 'Green', 'Blue']

        # Red: 1, Green: 2, Blue: 3
        print('Blue: ',values[0])
        print('Green: ',values[1])
        print('Red: ',values[2])
        print('Max color: ', colors[values.index(max(values))])
        print()
        self.max_value.publish(colors_rgb.index(colors[values.index(max(values))])+1)

        cv2.imshow("Image window", short_image)
        cv2.imshow("Blue window", short_image[:,:,0])
        cv2.imshow("Green window", short_image[:,:,1])
        cv2.imshow("Red window", short_image[:,:,2])
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