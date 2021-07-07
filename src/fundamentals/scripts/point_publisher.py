#!/usr/bin/env python 
# Set executable
import rospy # Ros python packages
from geometry_msgs.msg import Point # We can import Float64, Header, String

def point_publisher():
    pub = rospy.Publisher('position', Point, queue_size=10) # counter => Topic (same topic get the message), Point => Message type, queue_size(A huge queue could generate messaje delay)
    rospy.init_node('point_publisher', anonymous=True) #Point_point_publisher => node name, anonynous=True means no ID
    rate = rospy.Rate(1) # 1Hz => delay(Hz)
    pos = Point()
    while not rospy.is_shutdown(): # While ros is running
        pos.x += 0.1
        pos.y += 0.2
        pos.z += 0.05
        pub.publish(pos)
        rate.sleep() # Transform rate(Hz) into seconds 

if __name__ == '__main__': # int main()
    try:
        point_publisher()
    except rospy.ROSInterruptException:
        pass