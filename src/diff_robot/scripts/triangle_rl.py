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
velo = 0.2
aux = 0
aux_nuevo = 0
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
    global velo
    global aux
    global aux_nuevo
    print ("state ",state)

    # Giro en su propio eje
    if state == 0:
        if yaw < (pi/4):
            vel.linear.x = 0
            vel.angular.z = -velo
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 1
    # movimiento rectilineo
    if state == 1:
        if y < 2:
            vel.linear.x = velo
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 2

    if state == 2:
        if yaw > (-pi/4):
            vel.linear.x = 0
            vel.angular.z = velo
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 3

    if state == 3:
        if y > 0:
            vel.linear.x = velo
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 4

    if state == 4:
        if (yaw < 0):
            vel.linear.x = 0
            vel.angular.z = velo
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 5

    if state == 5:
        if x > 0:
            vel.linear.x = velo
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            state = 6
    if state == 6:
        vel.linear.x = 0
        vel.angular.z = 0
        state = 0

    pub.publish(vel)
def listener():

    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()