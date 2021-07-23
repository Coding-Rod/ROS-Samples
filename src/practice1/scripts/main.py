#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point, Twist

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
vel=Twist()

def callback(data):
  left = round(data.x,1)
  dist = round(data.y,1)
  right = data.z
  vel.linear.x = 0
  vel.angular.z = 0
  if (dist > 0.5):
    vel.linear.x= 0.2
  if left > right:
    vel.angular.z = -0.2
  if left < right:
    vel.angular.z = 0.2
  pub.publish(vel)

def listener():
  rospy.init_node('main', anonymous=True)
  rospy.Subscriber("laser_dist", Point, callback)
  rospy.spin()

if __name__ == '__main__':
  listener()
