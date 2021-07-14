#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
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
prev_yaw=0
right_move=False
left_move=False
checkpoint=0
checkpoint1=0
blue_percentage = 0
green_percentage = 0
red_percentage = 0
current_area=0


def callback_filter(data):
    global filter_blue_percentage
    global filter_red_percentage
    global filter_green_percentage

    filter_blue_percentage=int(data.x)
    filter_red_percentage=int(data.y)
    filter_green_percentage=int(data.z)


def giro_derecha():
    vel.linear.x=0
    vel.angular.z=0.21
def giro_izquierda():
    vel.linear.x=0
    vel.angular.z=-0.25
def adelante():
    vel.linear.x=0.2
    vel.angular.z=0
def atras():
    vel.linear.x=-0.2
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
    global prev_yaw
    global right_move
    global left_move
    global checkpoint
    global checkpoint1
    global filter_blue_percentage
    global filter_red_percentage
    global filter_green_percentage

    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w))
    yaw=euler[2]
    global state
    #print("state ", state)
    print("forward: ", forward_dist)
    print("left: ", left_dist)
    print("right: ", right_dist)
    print("check: ",checkpoint)
    print ("x ",x)
    print ("y ",y)

    if state == 0:
        if filter_red_percentage < 700:
            vel.linear.x=0
	    vel.angular.z=0.3
        elif filter_red_percentage >= 700 and filter_red_percentage < 2000:
            vel.linear.x=0.1
	    vel.angular.z=0.0
	else:
            vel.linear.x=0.0
	    vel.angular.z=0.0
    

    print("checkpoint: ",checkpoint)
    print("state: ", state)
    print("prev_yaw: ", prev_yaw)
    print("right_move: ", right_move)
    print("yaw: ", yaw)
    print("Red_Filt: ",filter_red_percentage)
    pub.publish(vel)



def listener():
    rospy.init_node('p3', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.Subscriber("scan", LaserScan, callback_scan)
    rospy.Subscriber("filter", Point, callback_filter)

    rospy.spin()
	
if __name__ == '__main__':
    listener()

