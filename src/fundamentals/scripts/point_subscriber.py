#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Point

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " X: %s", data.x)
    rospy.loginfo(rospy.get_caller_id() + " Y: %s", data.y)
    rospy.loginfo(rospy.get_caller_id() + " Z: %s\n", data.z)
    
def subscriber():

    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber("position", Point, callback)

    rospy.spin() #waiting for messages...

if __name__ == '__main__':
    subscriber()