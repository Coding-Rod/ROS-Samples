#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import time

def callback(data):
    #rospy.loginfo( "Angle max %f", data.angle_max)
    Angle_max=data.angle_max
    #rospy.loginfo( "Angle min %f", data.angle_min)
    Angle_min=data.angle_min
    #rospy.loginfo( "Angle increment %f", data.angle_increment)
    Angle_increment=data.angle_increment
    #rospy.loginfo( "Samples %f", (Angle_max-Angle_min)/Angle_increment)
    Samples=(Angle_max-Angle_min)/Angle_increment
    current_distance=data.ranges[0]
    min_distance=10000
    for i in range (1,int(Samples)+1):
	if data.ranges[i] < min_distance:
	    min_distance=data.ranges[i]
	current_distance=data.ranges[i]
    rospy.loginfo( "Min distance %f", min_distance)
    rospy.loginfo( "Central distance %f", data.ranges[int(Samples/2)])

def listener():

    rospy.init_node('scan', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
