#!/usr/bin/env python 
import rospy #ros python packages
from sensor_msgs.msg import JointState #import JointState message from sensor_msgs
import std_msgs.msg

class Publisher():
    def __init__(self):
        self.pub = rospy.Publisher('joint_states', JointState, queue_size=20) #position -> Topic, Point -> Message type, queue_size
        self.rate = rospy.Rate(5) # 5Hz -> delay(Hz)
        self.msg = JointState() # Point topic object
        self.h = std_msgs.msg.Header() #init Header message instance
        self.angles = [0.6960722122802938, #init Angles 
                      -0.936421503573102,
                       0.9384565574808001,
                       0.0,
                       0.025970499269635905,
                       1.8851301250790282]
        self.msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6'] #define names 
        self.ctrl_c = False #init ctrl_c instance
        rospy.on_shutdown(self.shutdownhook) #init shutdownhook

    def movement_sequence(self):
        if(self.h.seq < 8):
            #first movement sequence
            self.angles[0] += 0.0
            self.angles[1] += 0.1
            self.angles[2] += 0.1
            self.angles[3] += 0.05
            self.angles[4] += 0.05
            self.angles[5] += 0.9
        
        if(self.h.seq >= 8 and self.h.seq < 16):
            #second movement sequence
            self.angles[0] += 0.0
            self.angles[1] -= 0.1
            self.angles[2] -= 0.1
            self.angles[3] -= 0.05
            self.angles[4] -= 0.05
            self.angles[5] += 0.9
        
        if(self.h.seq >= 16 and self.h.seq < 24):
            #third movement sequence
            self.angles[0] += 0.2
            self.angles[1] += 0.0
            self.angles[2] += 0.0
            self.angles[3] += 0.0
            self.angles[4] += 0.0
            self.angles[5] += 0.9

        if(self.h.seq >= 24 and self.h.seq < 32):
            #fourth movement sequence
            self.angles[0] += 0.0
            self.angles[1] += 0.1
            self.angles[2] += 0.1
            self.angles[3] += 0.05
            self.angles[4] += 0.05
            self.angles[5] += 0.9

        if(self.h.seq >= 32 and self.h.seq < 40):
            #fifth movement sequence
            self.angles[0] += 0.0
            self.angles[1] -= 0.1
            self.angles[2] -= 0.1
            self.angles[3] -= 0.05
            self.angles[4] -= 0.05
            self.angles[5] += 0.9
        
        if(self.h.seq >= 40 and self.h.seq < 56):
            #sixth movement sequence
            self.angles[0] -= 0.2
            self.angles[1] += 0.0
            self.angles[2] += 0.0
            self.angles[3] += 0.0
            self.angles[4] += 0.0
            self.angles[5] += 0.9

        if(self.h.seq >= 56 and self.h.seq < 64):
            #seventh movement sequence
            self.angles[0] += 0.0
            self.angles[1] += 0.1
            self.angles[2] += 0.1
            self.angles[3] += 0.07
            self.angles[4] += 0.05
            self.angles[5] += 0.9
        
        if(self.h.seq >= 64 and self.h.seq < 72):
            #eight movement sequence
            self.angles[0] += 0.0
            self.angles[1] -= 0.1
            self.angles[2] -= 0.1
            self.angles[3] -= 0.07
            self.angles[4] -= 0.05
            self.angles[5] += 0.9

        if(self.h.seq >= 72 and self.h.seq < 80):
            #ninth movement sequence
            self.angles[0] += 0.2
            self.angles[1] += 0.0
            self.angles[2] += 0.0
            self.angles[3] += 0.0
            self.angles[4] += 0.0
            self.angles[5] += 0.9

        if(self.h.seq >= 80):
            #tenth movement sequence
            self.angles[0] += 0.0
            self.angles[1] += 0.0
            self.angles[2] += 0.0
            self.angles[3] += 0.0
            self.angles[4] += 0.0
            self.angles[5] += 0.0

    def move_robot(self):
        while not self.ctrl_c: #while ros is running
            self.h.stamp = rospy.Time.now() #init time
            self.h.seq +=1 #increment the sequence
            self.msg.header = self.h #assign the h message data to message for JointState
            self.msg.position = self.angles #assign the angles to position message for JointState
            self.movement_sequence() #call movement_sequence method
            rospy.loginfo(self.msg) # show log message in console
            self.pub.publish(self.msg) #Publish a message
            self.rate.sleep() #transforms rate(Hz) in seconds

    def shutdownhook(self):
        self.ctrl_c = True #replace the rospy.is_shutdown


if __name__ == '__main__':
    rospy.init_node('joint_states_publisher_rr', anonymous=True) #point_publisher -> node name, anonymous=True -> no id
    kuka_joint_states = Publisher() #Init the Publisher class
    try:
        kuka_joint_states.move_robot() #Call the move_robot method
    except rospy.ROSInterruptException:
        pass