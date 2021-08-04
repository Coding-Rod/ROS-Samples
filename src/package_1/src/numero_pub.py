#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32

def publisher():
    pub = rospy.Publisher('numero', Int32, queue_size=10)
    rospy.init_node('numero_pub', anonymous=True)
    rate = rospy.Rate(0.5) # 1Hz
    counter = 0
    while not rospy.is_shutdown():
        rospy.loginfo(counter)
        pub.publish(counter)
        counter+=1
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
