#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time
import tf

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
state=0
vel=Twist()
def callback(data):
    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    yaw=euler[2] 
    print ("x ",x)
    print ("y ",y)
    print ("yaw ",yaw)
    global state
    print ("state ",state)

    if state == 0 :
	if x<2:
	   vel.linear.x=0.2
	   vel.angular.z=0
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=1

    if state == 1 :
	if yaw > -1.5707:
	   vel.linear.x=0
	   vel.angular.z=0.2
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=2

    if state == 2 :
	if y > -2:
	   vel.linear.x=0.2
	   vel.angular.z=0
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=3

    if state == 3 :
	if abs(yaw) < 3.14:
	   vel.linear.x=0
	   vel.angular.z=0.2
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=4

    if state == 4 :
	if x > 0 :
	   vel.linear.x=0.2
	   vel.angular.z=0
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=5

    if state == 5 :
	if abs(yaw) > 1.57:
	   vel.linear.x=0
	   vel.angular.z=0.2
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=6

    if state == 6 :
	if y < 0 :
	   vel.linear.x=0.2
	   vel.angular.z=0
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=7

    if state == 7 :
	if yaw > 0:
	   vel.linear.x=0
	   vel.angular.z=0.2
	else:
	   vel.linear.x=0
	   vel.angular.z=0
	   state=0

    pub.publish(vel)
def listener():

    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
