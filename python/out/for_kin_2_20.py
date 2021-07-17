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
a1 = Symbol('A1')
d1 = Symbol('D1')
l1 = Symbol('L1')
d2 = Symbol('D2')
l2 = Symbol('L2')
d3 = Symbol('D3')
l3 = Symbol('L3')
d4 = Symbol('D4')


def dh_matrix (t,d,a,aph):
	T=Matrix([[cos(t), -sin(t)*cos(aph),sin(t)*sin(aph), a*cos(t)],[sin(t), cos(t)*cos(aph), -cos(t)*sin(aph), a*sin(t)],[0,sin(aph), cos(aph), d],[0, 0, 0, 1]])
	return T

T01=dh_matrix(0,d1,0,0)
T12=dh_matrix(t1,l1,d2,pi/2)
T23=dh_matrix(t2,-d3,-l2,0)
T34=dh_matrix(t3+pi,d4,-l3,pi/2)
T45=dh_matrix(0,a1,0,0)

T02=T01*T12
T03=T02*T23
T04=T03*T34
T05=T04*T45

print("px= "+str(T05[0,3].subs([(d1, 0.0925), (l1, 0.2105), (d2, 0.1), (l2, 0.25), (d3, 0.05), (l3, 0.25), (d4, 0.06)])))
print("py= "+str(T05[1,3].subs([(d1, 0.0925), (l1, 0.2105), (d2, 0.1), (l2, 0.25), (d3, 0.05), (l3, 0.25), (d4, 0.06)])))
print("pz= "+str(T05[2,3].subs([(d1, 0.0925), (l1, 0.2105), (d2, 0.1), (l2, 0.25), (d3, 0.05), (l3, 0.25), (d4, 0.06)])))

pub = rospy.Publisher('joint_states', JointState, queue_size=1)
pos = rospy.Publisher('position', Point, queue_size=1)
position = Point()
header = Header()
seq = 0
header.frame_id=''
joint_msg=JointState()

joint_msg.name = ['joint1','joint2','joint3','joint4','joint5']
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
    T05n=T05.subs([(t1,data.linear.x),(t2,data.linear.y),(t3,data.linear.z),(t4,data.angular.x),(a1,data.angular.y),(d1, 0.0925), (l1, 0.2105), (d2, 0.1), (l2, 0.25), (d3, 0.05), (l3, 0.25), (d4, 0.06)])
    position.x= T05n[0,3] #modify variable name T0Xn
    position.y= T05n[1,3] #modify variable name T0Xn
    position.z= T05n[2,3] #modify variable name T0Xn
    pos.publish(position)
    print(angles)

def listener():
    rospy.init_node('for_kin_2_20', anonymous=True)   
    rospy.Subscriber("angles", Twist, callback)

    rospy.spin() #keep alive
if __name__ == '__main__':
    listener()
