#!/usr/bin/env python 
import rospy #ros python packages
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
 
def point_publisher():
    pub = rospy.Publisher('joint_states', JointState, queue_size=20) #position -> Topic, Point -> Message type, queue_size
    rospy.init_node('joint_states_publisher_rr', anonymous=True) #point_publisher -> node name, anonymous=True -> no id
    rate = rospy.Rate(5) # 5Hz -> delay(Hz)
    msg = JointState() # Point topic object
    h = Header()
    msg.name = ['joint1', 'joint2']
    angles = [0,0]
    counter = 0
    while not rospy.is_shutdown(): #while ros is running
        h.stamp = rospy.Time.now()
        h.seq +=1

        if counter < 25:
            angles[0] += 0.1

        if counter >= 25 and counter < 50:
            angles[0] -= 0.1
            angles[1] += 0.1

        if counter >= 50:
            angles[1] -= 0.1
            
        if counter == 100:
            counter = 0

        counter += 1

        msg.header = h
        msg.position = angles
        pub.publish(msg) #Publish a message
        rate.sleep() #transforms rate(Hz) in seconds

if __name__ == '__main__':
    try:
        point_publisher()
    except rospy.ROSInterruptException:
        pass