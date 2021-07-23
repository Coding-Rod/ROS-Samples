#!/usr/bin/env python
# from __future__ import print_function
# import roslib
import sys
import rospy
from sympy import *
import numpy as np
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan

class laser_points:

  def __init__(self):
    self.three_dist = Point()
    self.cross_dist = rospy.Publisher("laser_dist", Point, queue_size=1) # topic from camera
    self.laser_sub = rospy.Subscriber("scan", LaserScan, self.callback)

  def callback(self,data):
    self.three_dist.x = data.ranges[346]    # right 
    self.three_dist.y = data.ranges[356]  # forward
    self.three_dist.z = data.ranges[366]  # left
    self.cross_dist.publish(self.three_dist)

def main(args):
  rospy.init_node('laser', anonymous=True)
  ic = laser_points()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)