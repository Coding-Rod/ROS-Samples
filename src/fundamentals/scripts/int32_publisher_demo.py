#!/usr/bin/env python 
# Set executable
import rospy # Ros python packages
from std_msgs.msg import Int32 # We can import Float64, Header, String

def publisher():
    pub = rospy.Publisher('counter', Int32, queue_size=10) # counter => Topic (same topic get the message), Int32 => Message type, queue_size(A huge queue could generate messaje delay)
    rospy.init_node('int32_publisher', anonymous=True) #int32_publisher => node name, anonynous=True means no ID
    rate = rospy.Rate(1) # 1Hz => delay(Hz)
    counter = 0 # Variable
    while not rospy.is_shutdown(): # While ros is running
        rospy.loginfo(counter) # Similar to print(), but includes a time stamp
        pub.publish(counter) # Publish a message make use of: rostopic echo /counter
        counter+=1 # Increment value
        rate.sleep() # Transform rate(Hz) into seconds 

if __name__ == '__main__': # int main()
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass