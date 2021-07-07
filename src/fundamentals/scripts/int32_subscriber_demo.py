#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def subscriber():

    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber("counter", Int32, callback)

    rospy.spin() #waiting for messages...

if __name__ == '__main__':
    subscriber()