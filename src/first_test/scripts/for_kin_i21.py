#!/usr/bin/env python
import rospy
from sympy import*
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Header


t1 = Symbol('t1')
t2 = Symbol('t2')
t3 = Symbol('t3')
t4 = Symbol('t4')
t5 = Symbol('t5')
l1 = Symbol('L1')
l2 = Symbol('L2')
l3 = Symbol('L3')
l4 = Symbol('L4')
l5 = Symbol('L5')


def dh_matrix (t,d,a,aph):
	T=Matrix([[cos(t), -sin(t)*cos(aph),sin(t)*sin(aph), a*cos(t)],[sin(t), cos(t)*cos(aph), -cos(t)*sin(aph), a*sin(t)],[0,sin(aph), cos(aph), d],[0, 0, 0, 1]])
	return T

T01=dh_matrix(0,l1,0,0)
T12=dh_matrix(t1+pi,0,-l2,-pi/2)
T23=dh_matrix(t2,0,l3,pi)
T34=dh_matrix(t3,0,0,pi/2)
T45=dh_matrix(t4+pi,-l4,0,pi/2)
T56=dh_matrix(t5-pi/2,0,l5,0)

T02=T01*T12
T03=T02*T23
T04=T03*T34
T05=T04*T45
T06=T05*T56

print("px= "+str(T06[0,3].subs([(l1, 0.55), (l2, 0.15), (l3, 0.825), (l4, 0.625), (l5, 0.11)])))
print("py= "+str(T06[1,3].subs([(l1, 0.55), (l2, 0.15), (l3, 0.825), (l4, 0.625), (l5, 0.11)])))
print("pz= "+str(T06[2,3].subs([(l1, 0.55), (l2, 0.15), (l3, 0.825), (l4, 0.625), (l5, 0.11)])))

pub = rospy.Publisher('joint_states', JointState, queue_size=1)
pos = rospy.Publisher('position', Point, queue_size=1)
position = Point()
header = Header()
seq = 0
header.frame_id=''
joint_msg=JointState()

joint_msg.name = ['joint_1','joint_2','joint_3','joint_4','joint_5']
angles = [0.0,0.0,0.0,0.0,0.0]

def callback(data):
    angles[0]=data.linear.x
    angles[1]=data.linear.y
    angles[2]=data.linear.z
    angles[3]=data.angular.x
    angles[4]=data.angular.y
    global seq
    seq=seq+1
    header.seq = seq
    header.stamp = rospy.get_rostime()
    joint_msg.header=header
    joint_msg.position=angles
    pub.publish(joint_msg)
    T06n=T06.subs([(t1,data.linear.x),(t2,data.linear.y),(t3,data.linear.z),(t4,data.angular.x),(t5,data.angular.y),(l1, 0.55), (l2, 0.15), (l3, 0.825), (l4, 0.625), (l5, 0.11)])
    position.x= T06n[0,3] #modify variable name T0Xn
    position.y= T06n[1,3] #modify variable name T0Xn
    position.z= T06n[2,3] #modify variable name T0Xn
    pos.publish(position)
    print(angles)

def listener():
    rospy.init_node('for_kin_i21', anonymous=True)   
    rospy.Subscriber("angles", Twist, callback)

    rospy.spin() #keep alive
if __name__ == '__main__':
    listener()
