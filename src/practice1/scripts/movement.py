#!/usr/bin/env python
# from __future__ import print_function
# import roslib
import sys
import rospy
from sympy import *
import numpy as np
from numpy import pi
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
import tf

class move:

  def __init__(self):
    self.three_dist = Point()
    self.vel = Twist()

    self.laser_sub = rospy.Subscriber("odom", Odometry, self.callback_odom)
    self.action = rospy.Subscriber("state",Int32,self.callback)

    self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    self.stt = rospy.Publisher("state",Int32,queue_size=1)

  def callback_odom(self,data):
    self.x=data.pose.pose.position.x
    self.y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    self.yaw=euler[2] 

  def callback(self,data):
    # SI DETECTA EL RED BOX VA AL MURO DE LA IZQUIERDA Y SE POSICIONA DETRAS DE EL
    state = data.data
    print("state: ",state)
    print("x: ",self.x)
    print("y: ",self.y)
    print("yaw: ",self.yaw)
    
    if(state == 1):
        self.vel.linear.x = 0.5
        if(self.x > 5):
          self.vel.angular.z = -0.2
          self.vel.linear.x = 0
        if(self.yaw > pi/2):
          self.vel.linear.x = 0.5
          self.vel.angular.z = 0
        if(self.y > 5):
          self.vel.linear.x = 0
          

    # SI DETECTA EL MAIL BOX VA AL MURO DE LA DERECHA Y SE POSICIONA DETRAS DE EL
    if(state == 2):
        self.vel.linear.x = 0.5
        if(self.x > 5):
          self.vel.angular.z = 0.2
          self.vel.linear.x = 0
        if(self.yaw < -pi/2):
          self.vel.linear.x = 0.5
          self.vel.angular.z = 0
        if(self.y < -7):
          self.vel.linear.x = 0

    # SI DECTA EL GREEN BOX VA AL MURO QUE ESTA DETRAS DEL ROBOT Y SE POSICIONA DETRAS DE EL
    if(state == 3):
        self.vel.angular.z = -0.2
        
        if(self.yaw > -pi/2):
          self.vel.angular.z = 0
          self.vel.linear.x = 0.5
        if(self.y < -6):
          self.vel.linear.x = 0
          self.vel.angular.z = -0.2
        if(self.yaw > -pi/2):
          self.vel.angular.z = 0
          self.vel.linear.x = 0.5
        if(self.x < -5):
          self.vel.linear.x = 0
    # More objects detected
    state = 0 if state > 3 else state

    # pub
    self.stt.publish(state)
    self.pub.publish(self.vel)

def main(args):
  rospy.init_node('movement', anonymous=True)
  move()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)