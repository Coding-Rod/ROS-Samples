#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import Int32
import time
import tf

pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
state=0
vel=Twist()
forward_dist=0
left_dist=0
right_dist=0
yaw = 0
right_move=False
left_move=False
filter_blue_percentage = 0

def callback_filter(data):
    global filter_blue_percentage
    filter_blue_percentage=int(data.x)

def giro_derecha():
    vel.linear.x=0
    vel.angular.z=0.15

def giro_izquierda():
    vel.linear.x=0
    vel.angular.z=-0.15

def adelante():
    vel.linear.x=0.2
    vel.angular.z=0

def callback_scan(data):
    global forward_dist
    global left_dist
    global right_dist
    forward_dist=data.ranges[360]
    left_dist=data.ranges[719]
    right_dist=data.ranges[0]

def callback(data):
    global forward_dist
    global left_dist
    global right_dist
    global filter_blue_percentage

    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w))
    yaw=euler[2]
    global state
    #print("state ", state)
    # print("forward: ", forward_dist)
    # print("left: ", left_dist)
    # print("right: ", right_dist)
    # print ("x ",x)
    # print ("y ",y)

    left_dist = 0 if left_dist > 10 else left_dist
    right_dist = 0 if right_dist > 10 else right_dist

    if(forward_dist > 0.4):
        adelante()
    else:
        if(left_dist > right_dist):
            if (yaw < 1.4708):
                giro_izquierda()

        if(left_dist < right_dist):
            if (yaw < -1.6708):
                giro_derecha()

    print("yaw: ", yaw)
    pub.publish(vel)



def listener():
    rospy.init_node('p3', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.Subscriber("scan", LaserScan, callback_scan)
    rospy.Subscriber("filter", Point, callback_filter)

    rospy.spin()
	
if __name__ == '__main__':
    listener()

