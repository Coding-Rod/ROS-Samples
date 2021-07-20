#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import time
import tf

pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
state=0
m_decision = 0
vel=Twist()
forward_dist=0
left_dist=0
right_dist=0
prev_yaw=0
right_move=False
left_move=False
pi = 3.14159265359
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
    global state
    global m_decision
    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w))
    yaw=euler[2]

    if(state==0):
        if(forward_dist>0.5):
            vel.linear.x = 0.25
            vel.angular.z = 0
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            m_decision = 1
    if(m_decision == 1):
        if(forward_dist<0.5 and left_dist<1.5 and right_dist>1):
            state = 2
            m_decision = 0
        if(forward_dist>1):
            state = 0
            m_decision = 0
        if(forward_dist<0.5 and left_dist>1 and right_dist<1.5):
            state = 3
            m_decision = 0

    if(state == 2):
        if(yaw<-pi/2):
            vel.linear.x = 0
            vel.angular.z = 0.25
        else:
            vel.linear.x = 0
            vel.angular.z = 0
            m_decision = 1

    '''
    print("state: ", state)
    print("prev_yaw: ", prev_yaw)
    print("right_move: ", right_move)
    print("yaw: ", yaw)
    '''
    print("forward_dist: ", forward_dist)
    print("left_dist: ", left_dist)
    print("right_dist: ", right_dist)
    pub.publish(vel)

def listener():
    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.Subscriber("scan", LaserScan, callback_scan)

    rospy.spin()
	
if __name__ == '__main__':
    listener()