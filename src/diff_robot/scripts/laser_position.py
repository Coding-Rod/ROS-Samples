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

class Laser_counter:

  def __init__(self):
    self.laser_sub = rospy.Subscriber("scan", LaserScan, self.callback)
    self.forward_counter = 0

  def callback(self,data):
    aux1 = 1000000
    self.counter = 0
    self.menor_position = []
    self.mayor_position = []
    self.media_position = []
    self.angulo = [] 

    for i in range(0,720):
        self.dist=math.ceil(data.ranges[i])
        if aux1 > (self.dist+1):
            self.counter += 1
            self.menor_position.append(i) 
        if (aux1+1) < self.dist:
            if i != 0:
                self.mayor_position.append(i)
        aux1 = self.dist

    for i,j in zip(self.menor_position, self.mayor_position):
        self.media_position.append((i+j)/2)

    for i in self.media_position:
        self.angulo.append(i//4)

    print("Numero de objetos: ",self.counter)
    print("Posicion menor: ", self.menor_position)
    print("Posicion mayor: ",self.mayor_position)
    print("Posicion media: ", self.media_position)
    print("Angulos: ", self.angulo)

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