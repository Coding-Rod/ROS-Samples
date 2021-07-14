#!/usr/bin/env python 
#executable path
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import sympy as sym
def talker():
    #topic name --> position, message type-->twist, queue_size--> 10 messages   that will be stored in buffer
    rosp = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    #node name --> point_publisher
    rospy.init_node('move_robot', anonymous=True)
    #10Hz-->messages per second
    rate = rospy.Rate(0.1)
    vel = Twist() 
    while not rospy.is_shutdown():
	vel.linear.x=-0.1
	vel.angular.z=0
	rosp.publish(vel)
	rate.sleep()
	vel.linear.x=0
	vel.angular.z=0.1
	rosp.publish(vel)
	rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
