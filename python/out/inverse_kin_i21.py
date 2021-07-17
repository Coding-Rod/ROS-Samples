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

t1 = Symbol('t1')
t2 = Symbol('t2')
t3 = Symbol('t3')
t4 = Symbol('t4')
t5 = Symbol('t5')


header = Header()
seq = 0
header.frame_id = ''
joint_msg = JointState()
iterations = 100
alpha=0.3 #learning rate
pub = rospy.Publisher('joint_states', JointState, queue_size=10)
joint_msg.name = ['joint_1','joint_2','joint_3','joint_4','joint_5']
angles = [0.0,0.0,0.0,0.0,0.0]


#///////////////////////////////////////////////////
# Paste your px, py, pz params HERE
#///////////////////////////////////////////////////


J=Matrix([[diff(px,t1),diff(px,t2),diff(px,t3),diff(px,t4),diff(px,t5)],
          [diff(py,t1),diff(py,t2),diff(py,t3),diff(py,t4),diff(py,t5)],
          [diff(pz,t1),diff(pz,t2),diff(pz,t3),diff(pz,t4),diff(pz,t5)]])

def callback(data): #callback function
    target=Matrix([data.x,data.y,data.z])
    ti=Matrix([random(),random(),random(),random(),random()])
    for i in range(0,iterations):
        cp =Matrix([px.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4])]),py.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4])]),pz.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4])])])
        Jsubs=J.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4])])
        e=target-cp
        Jinv=Jsubs.H*(Jsubs*Jsubs.H)**-1
        dt=Jinv*e
        ti=ti+alpha*dt
        global seq
        header.seq = seq
        header.stamp = rospy.Time.now()

        angles[0] = ti[0]
        angles[1] = ti[1]
        angles[2] = ti[2]
        angles[3] = ti[3]
        angles[4] = ti[4]

        joint_msg.header = header
        joint_msg.position = angles
        pub.publish(joint_msg)
        seq += 1
        time.sleep(0.5)    
def subscriber():
    rospy.init_node('inverse_kin_i21', anonymous=True)
    rospy.Subscriber("position", Point, callback) 
    rospy.spin()

if __name__ == '__main__':
    subscriber()