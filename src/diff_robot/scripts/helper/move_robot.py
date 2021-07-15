#!/usr/bin/env python 
#executable path
import rospy
from geometry_msgs.msg import Twist

def movement_sequence():
    rosp = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    rospy.init_node('move_robot', anonymous=True)
    rate = rospy.Rate(0.15) # set delay
    vel = Twist() # instance vel
    while not rospy.is_shutdown():
        # Forward
        vel.linear.x=0.1
        vel.angular.z=0
        rosp.publish(vel)
        rate.sleep() # delay
        
        # Turn
        vel.linear.x=0
        vel.angular.z=0.1
        rosp.publish(vel)
        rate.sleep() # delay

if __name__ == '__main__':
    try:
        movement_sequence()
    except rospy.ROSInterruptException:
        pass
