#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import time
import tf
pi = 3.1415926535
speed = 0.2
aux = 0
new_aux = 0
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
status=0
vel=Twist()
def callback(data):
    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    yaw=euler[2] 
    print ("x ",x)
    print ("y ",y)
    print ("yaw ",yaw)
    global status
    global speed
    global aux
    global new_aux
    print ("status ",status)

    # Giro en su propio eje
    if status == 0:
        if yaw < (pi/4):
            vel.linear.x = 0
            vel.angular.z = -speed
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 1
    # movimiento rectilineo
    if status == 1:
        if y < 2:
            vel.linear.x = speed
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 2

    if status == 2:
        if yaw > (-pi/4):
            vel.linear.x = 0
            vel.angular.z = speed
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 3

    if status == 3:
        if y > 0:
            vel.linear.x = speed
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 4

    if status == 4:
        if (yaw < 0):
            vel.linear.x = 0
            vel.angular.z = speed
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 5

    if status == 5:
        if x > 0:
            vel.linear.x = speed
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            status = 6
    if status == 6:
        vel.linear.x = 0
        vel.angular.z = 0
        status = 0

    pub.publish(vel)
def listener():

    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()