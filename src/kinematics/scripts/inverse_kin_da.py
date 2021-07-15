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
d1=Symbol('d1')
d2=Symbol('d2')
l1=Symbol('L1')
l2=Symbol('L2')
l3=Symbol('L3') 
l4=Symbol('L4') 

header = Header()
joint_msg = JointState()
seq = 0
header.frame_id = ''
joint_msg.name =  ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
angles = [0.0, 0.0, 0.0, 0.0, 0.0]
alpha=0.3 #learning rate
iterations = 100
pub = rospy.Publisher('joint_states', JointState, queue_size=10)
px= -0.4*(-sin(t1)*sin(t2) - cos(t1)*cos(t2))*cos(t3) - 0.4*(-sin(t1)*cos(t2) + sin(t2)*cos(t1))*sin(t3) + 0.3*sin(t1)*sin(t2) + 0.07*sin(t1) + 0.3*cos(t1)*cos(t2)
py= -0.4*(sin(t1)*sin(t2) + cos(t1)*cos(t2))*sin(t3) - 0.4*(-sin(t1)*cos(t2) + sin(t2)*cos(t1))*cos(t3) + 0.3*sin(t1)*cos(t2) - 0.3*sin(t2)*cos(t1) - 0.07*cos(t1)
pz= -d1 - d2 + 0.4

J=Matrix([[diff(px,t1),diff(px,t2),diff(px,t3),diff(px,d1),diff(px,d2)],
          [diff(py,t1),diff(py,t2),diff(py,t3),diff(py,d1),diff(py,d2)],
          [diff(pz,t1),diff(pz,t2),diff(pz,t3),diff(pz,d1),diff(pz,d2)]])
def callback(data): #callback function
    
    target=Matrix([data.x,data.y,data.z])
    ti=Matrix([random(),random(),random(),random(),random()])
    for i in range(0,iterations):
        cp= Matrix([px.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(d1,ti[3]),(d2,ti[4])]),
                    py.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(d1,ti[3]),(d2,ti[4])]),
                    pz.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(d1,ti[3]),(d2,ti[4])])])
        e=target-cp
        Jsubs=J.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(d1,ti[3]),(d2,ti[4])])
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
        angles[3] = ti[3]
        angles[4] = ti[4]

        joint_msg.header = header
        joint_msg.position = angles
        pub.publish(joint_msg)
        seq += 1
        time.sleep(0.5)
        print("Iteration: ("+ str(i)+"/" +str(iterations)+")")

def subscriber():
    rospy.init_node('inverse_kin_da', anonymous=True)
    rospy.Subscriber("position", Point, callback) 
    rospy.spin()

if __name__ == '__main__':
    subscriber()