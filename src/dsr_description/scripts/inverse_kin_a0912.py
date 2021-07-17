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
t5=Symbol('t5')
t6=Symbol('t6')

header = Header()
joint_msg = JointState()
seq = 0
header.frame_id = ''
joint_msg.name =  ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
angles = [0.0, 0.0, 0.0, 0.0,0.0,0.0]
alpha=0.3 #learning rate
iterations = 100
pub = rospy.Publisher('joint_states', JointState, queue_size=10)

px=-0.124*(-(-sin(t2)*sin(t3)*cos(t1) + cos(t1)*cos(t2)*cos(t3))*cos(t4) + sin(t1)*sin(t4))*sin(t5) - 2.53e-5*(-sin(t2)*sin(t3)*cos(t1) + cos(t1)*cos(t2)*cos(t3))*sin(t4) + 0.124*(sin(t2)*cos(t1)*cos(t3) + sin(t3)*cos(t1)*cos(t2))*cos(t5) - 2.53e-5*sin(t1)*cos(t4) - 0.0392191*sin(t1) - 3.37211696e-5*sin(t2)*sin(t3)*cos(t1) + 0.516*sin(t2)*cos(t1)*cos(t3) + 0.56*sin(t2)*cos(t1) + 0.516*sin(t3)*cos(t1)*cos(t2) + 3.37211696e-5*cos(t1)*cos(t2)*cos(t3)
py=-0.124*(-(-sin(t1)*sin(t2)*sin(t3) + sin(t1)*cos(t2)*cos(t3))*cos(t4) - sin(t4)*cos(t1))*sin(t5) - 2.53e-5*(-sin(t1)*sin(t2)*sin(t3) + sin(t1)*cos(t2)*cos(t3))*sin(t4) + 0.124*(sin(t1)*sin(t2)*cos(t3) + sin(t1)*sin(t3)*cos(t2))*cos(t5) - 3.37211696e-5*sin(t1)*sin(t2)*sin(t3) + 0.516*sin(t1)*sin(t2)*cos(t3) + 0.56*sin(t1)*sin(t2) + 0.516*sin(t1)*sin(t3)*cos(t2) + 3.37211696e-5*sin(t1)*cos(t2)*cos(t3) + 2.53e-5*cos(t1)*cos(t4) + 0.0392191*cos(t1)
pz=0.124*(-sin(t2)*sin(t3) + cos(t2)*cos(t3))*cos(t5) - 2.53e-5*(-sin(t2)*cos(t3) - sin(t3)*cos(t2))*sin(t4) + 0.124*(-sin(t2)*cos(t3) - sin(t3)*cos(t2))*sin(t5)*cos(t4) - 0.516*sin(t2)*sin(t3) - 3.37211696e-5*sin(t2)*cos(t3) - 3.37211696e-5*sin(t3)*cos(t2) + 0.516*cos(t2)*cos(t3) + 0.56*cos(t2) + 0.19

J=Matrix([[diff(px,t1),diff(px,t2),diff(px,t3),diff(px,t4),diff(px,t5),diff(px,t6)],
          [diff(py,t1),diff(py,t2),diff(py,t3),diff(py,t4),diff(py,t5),diff(py,t6)],
          [diff(pz,t1),diff(pz,t2),diff(pz,t3),diff(pz,t4),diff(pz,t5),diff(pz,t6)]])
def callback(data): #callback function
    
    target=Matrix([data.x,data.y,data.z])
    ti=Matrix([random(),random(),random(),random(),random(),random()])
    for i in range(0,iterations):
        cp= Matrix([px.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4]),(t6,ti[5])]),py.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4]),(t6,ti[5])]),pz.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4]),(t6,ti[5])])])
        e=target-cp
        Jsubs=J.subs([(t1,ti[0]),(t2,ti[1]),(t3,ti[2]),(t4,ti[3]),(t5,ti[4]),(t6,ti[5])])
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
        angles[5] = ti[5]

        joint_msg.header = header
        joint_msg.position = angles
        pub.publish(joint_msg)
        seq += 1
        time.sleep(0.5)    
def subscriber():
    rospy.init_node('inverse_kin_a0912', anonymous=True)
    rospy.Subscriber("position", Point, callback) 
    rospy.spin()

if __name__ == '__main__':
    subscriber()