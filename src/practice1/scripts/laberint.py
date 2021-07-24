#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time
import tf
import numpy as np

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
state=0
vel=Twist()

forward_dist=0
left_dist=0
right_dist=0
red = 0
flag = 0 
last_angle = 0 
giro = 0 
counter = 0

pi = np.pi
def mask_callback(data):
  global red
  red = data.data

def scan_callback(data):
  global forward_dist
  global left_dist
  global right_dist
  forward_dist=data.ranges[360]
  left_dist=data.ranges[719]
  right_dist=data.ranges[0]

def callback(data):
  x=data.pose.pose.position.x
  y=data.pose.pose.position.y
  euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
  yaw=euler[2] 
  global state
  global flag
  global last_angle
  global giro
  global counter
  
  # Rotate
  if state == 0:
    if (yaw < pi/2):
      vel.angular.z = -0.2  
    else:
      vel.angular.z = 0
      state = 1

  if state == 1:
    # Go forward
    if (forward_dist > 0.5 and flag == 0):
      vel.linear.x = 0.25
      last_angle = yaw
      giro = right_dist - left_dist
    else:
      vel.linear.x = 0.0
      dif = abs(last_angle - yaw)
      flag = 1

    # Rotate
      if (giro > 0 and dif < pi/2):
        vel.angular.z = 0.2
      elif (giro < 0 and dif < pi/2):
        vel.angular.z = -0.2
      else:
        flag = 0 
        vel.linear.x = 0
        vel.angular.z = 0
        last_angle = yaw
        state = 2

  # Verify
  if state == 2:
    if (red == 1):
      counter += 1
    print(counter)
    state = 1
  pub.publish(vel)

def listener():
  rospy.init_node('laberint', anonymous=True)
  rospy.Subscriber("odom", Odometry, callback)
  rospy.Subscriber("scan", LaserScan, scan_callback)
  rospy.Subscriber("mask", Int32, mask_callback)
  rospy.spin()

if __name__ == '__main__':
  listener()
