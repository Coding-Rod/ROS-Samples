#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

def callback(data):
    if (data.data % 2 == 0): rospy.loginfo(rospy.get_caller_id() + "Numero par: %s", data.data)
    
def listener():

    rospy.init_node('par_sub', anonymous=True)

    rospy.Subscriber("numero", Int32, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()