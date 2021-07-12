#!/usr/bin/env python
import rospy
from sympy import*
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

t1=Symbol('t1')
t2=Symbol('t2')
t3=Symbol('t3')
t4=Symbol('t4')

def dh_matrix (t,d,a,aph):

	T=Matrix([[cos(t), -sin(t)*cos(aph),sin(t)*sin(aph), a*cos(t)],[sin(t), cos(t)*cos(aph), -cos(t)*sin(aph), a*sin(t)],[0,sin(aph), cos(aph), d],[0, 0, 0, 1]])
	return T

T01 =    dh_matrix(0,0,0,0)
T12 =    dh_matrix(t1,0.4,0,pi/2)
T23 =    dh_matrix(t2,0,0.4,0)
T33p=    dh_matrix(t3,0,0.1,0)
T3p4=    dh_matrix(pi/2,0,0,pi/2)
T45 =    dh_matrix(t4,0,0,0)

T02=T01*T12
T03=T02*T23
T03p=T03*T33p
T04=T03p*T3p4
T05=T04*T45

pub = rospy.Publisher('joint_states', JointState, queue_size=1)
pos = rospy.Publisher('position', Point, queue_size=1)
position = Point()
header = Header()
seq = 0
header.frame_id=''
joint_msg=JointState()
joint_msg.name = ['joint1','joint2','joint3','joint4'] #modify
angles=[0.0,0.0,0.0,0.0] #modify

def callback(data):
    angles[0]=data.x
    angles[1]=data.y
    angles[2]=data.z
    angles[3]=data.w
    global seq
    seq=seq+1
    header.seq = seq
    header.stamp = rospy.get_rostime()
    joint_msg.header=header
    joint_msg.position=angles
    pub.publish(joint_msg)
    T05n=T05.subs([(t1,data.x),(t2,data.y),(t3,data.z),(t4,data.w)]) #modify
    position.x= T05n[0,3] #modify variable name T0Xn
    position.y= T05n[1,3] #modify variable name T0Xn
    position.z= T05n[2,3] #modify variable name T0Xn
    pos.publish(position)
    print(angles)

def listener():
    rospy.init_node('for_kin_kuka_4_dof', anonymous=True)   
    rospy.Subscriber("angles", Quaternion, callback)

    rospy.spin() #keep alive
if __name__ == '__main__':
    listener()
