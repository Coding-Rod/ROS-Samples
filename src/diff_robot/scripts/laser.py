#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
import math
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from sensor_msgs.msg import LaserScan

minim = []
maxim = []
mean = []
angles = [] 

class Laser_counter:

  def __init__(self):
    self.laser_sub = rospy.Subscriber("scan", LaserScan, self.callback)
    self.forward_counter = 0

  def callback(self,data):
    aux1 = 1000000
    self.counter = 0
    global minim
    global maxim
    global mean
    global angles
    minim = []
    maxim = []
    mean = []
    angles = [] 
    for i in range(0,720):
        self.dist=math.ceil(data.ranges[i])
        if aux1 > (self.dist+1):
            self.counter += 1
            minim.append(i) 
        
        if (aux1+1) < self.dist:
            if i != 0:
                maxim.append(i)
        
        aux1 = self.dist

    mean = [(x+y)/2 for (x,y) in zip(minim,maxim)]
    angles = [x//4 for x in mean]

    print("Numero de objetos: ",self.counter)
    print("Posicion minim: ", minim)
    print("Posicion maxim: ",maxim)
    print("angless: ", angles)

def main(args):
  laser_counter = Laser_counter()
  rospy.init_node('laser_counter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)