#!/usr/bin/env python
import rospy
import time
from sympy import *
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from geometry_msgs.msg import Point 
from std_msgs.msg import String
from std_msgs.msg import Int32
from random import random

t1=Symbol('t1')
t2=Symbol('t2')
t3=Symbol('t3')
t4=Symbol('t4')

header = Header()
joint_msg = JointState()
seq = 0
header.frame_id = ''
joint_msg.name = ['joint1','joint2','joint3','joint4']
angles = [0.0, 0.0, 0.0, 0.0]
alpha=0.3 #learning rate
iterations = 100
pub = rospy.Publisher('joint_states', JointState, queue_size=10)
px=-0.2*sin(t2)*sin(t3)*cos(t1) + 0.2*cos(t1)*cos(t2)*cos(t3) + 0.2*cos(t1)*cos(t2)
py=-0.2*sin(t1)*sin(t2)*sin(t3) + 0.2*sin(t1)*cos(t2)*cos(t3) + 0.2*sin(t1)*cos(t2)
pz=0.2*sin(t2)*cos(t3) + 0.2*sin(t2) + 0.2*sin(t3)*cos(t2) + 0.4

J=Matrix([[diff(px,t1),diff(px,t2),diff(px,t3)],[diff(py,t1),diff(py,t2),diff(py,t3)],[diff(pz,t1),diff(pz,t2),diff(pz,t3)]])
def callback(data): #callback function
    
    target=Matrix([data.x,data.y,data.z])
    ti=Matrix([random(),random(),random()])
    for i in range(0,iterations):
        cp= Matrix([px.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2])]),py.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2])]),pz.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2])])])
        e=target-cp
        Jsubs=J.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2])])
        Jinv=Jsubs.H*(Jsubs*Jsubs.H)**-1
        dt=Jinv*e
        ti=ti+alpha*dt
        #print (cp)
        global seq
        header.seq = seq
        header.stamp = rospy.Time.now()
        angles[0] = ti[0]
        angles[1] = ti[1]
        angles[2] = ti[2]

        joint_msg.header = header
        joint_msg.position = angles
        pub.publish(joint_msg)
        seq += 1
        time.sleep(0.5)    
def subscriber():
    rospy.init_node('inverse_kin', anonymous=True)
    rospy.Subscriber("position", Point, callback) 
    rospy.spin()

if __name__ == '__main__':
    subscriber()