#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import time
import tf

def callback(data):

    rospy.loginfo( "Position X: %f", data.pose.pose.position.x)
    rospy.loginfo( "Position Y: %f", data.pose.pose.position.y)
    rospy.loginfo( "Position Z: %f", data.pose.pose.position.z)
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    print("Yaw",euler[2])

def listener():

    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
