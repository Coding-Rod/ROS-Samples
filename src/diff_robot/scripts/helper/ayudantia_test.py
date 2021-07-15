#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import time
import tf

pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
state=0
vel=Twist()
forward_dist=0
left_dist=0
right_dist=0
prev_yaw=0
right_move=False
left_move=False
current_area=0
check_point=0
checkpoint=0
checkpoint1=0
filter_percentage = 0
def callback_filter(data):
    global filter_percentage
    filter_percentage=data.data

def giro_derecha():
    vel.linear.x=0
    vel.angular.z=0.2
def giro_izquierda():
    vel.linear.x=0
    vel.angular.z=-0.2
def adelante():
    vel.linear.x=0.3
    vel.angular.z=0
def atras():
    vel.linear.x=-0.3
    vel.angular.z=0
def stop():
    vel.linear.x=0
    vel.angular.z=0

def callback_scan(data):
    global forward_dist
    global left_dist
    global right_dist
    global back_dist
    forward_dist=data.ranges[360]
    left_dist=data.ranges[719]
    right_dist=data.ranges[0]

def callback(data):
    global forward_dist
    global left_dist
    global right_dist
    global prev_yaw
    global right_move
    global left_move
    global current_area
    global forward_dist
    global filter_percentage
    global check_point
    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w))
    yaw=euler[2]
    #print("x ", x)
    #print("y ", y)
    #print("yaw ", yaw)
    global state
    #print("state ", state)
    print("forward: ", forward_dist)
    print("left: ", left_dist)
    print("right: ", right_dist)
    print("check: ",check_point)

    if state==0:
        if (forward_dist>1.47) and (left_dist<0.8 or right_dist<0.8):
            adelante()
	elif (forward_dist<1.40) and (left_dist<0.8 or right_dist<0.8):
	    atras()
	else:
            state=1

    if state==1:
        if yaw<1.5707:
            giro_izquierda()
 	else:
	    state=2

    if state == 2:
        if y<2:
            adelante()
        else:
	    state=3

    if state==3:
	if yaw>0:
            giro_derecha()
        else:
            state=4

    if state==4:
        if x>0.015:
	    atras()
        elif x<-0.015:
            adelante()
	else:
            state=5
   
    if state==5:
        if yaw<1.5707:
            giro_izquierda()
 	else:
	    state=6

    if state==6:
        if (forward_dist>0.3):
            adelante()
 	else:
	    state=7

    if state==7:
	
        if forward_dist>0.35:
            
            vel.linear.x=0.35
            vel.angular.z=0
	    if checkpoint==11 and filter_percentage==0:
		
	        vel.linear.x=0
                vel.angular.z=0
  	    if checkpoint==11 and filter_percentage>0:
                vel.linear.x=0.35
                vel.angular.z=0
                checkpoint=checkpoint+1
        else:
            vel.linear.x=0
            vel.angular.z=0
            state=8	

    if state == 8:
        if right_dist > 1.2 and left_dist < 0.8:
            state=9
            

        if left_dist > 1.2 and right_dist < 0.8:
            state=10
    if state == 9:
        if prev_yaw==0:
            if yaw > -1.5707:
                right_move=True
            else:
                right_move=False
                prev_yaw=prev_yaw+1
                if prev_yaw > 3:
                    prev_yaw=0

                state=7               

        if prev_yaw==1:
            if abs(yaw)<3.14:
                right_move=True
            else:
                right_move=False
                prev_yaw=prev_yaw+1
                if prev_yaw > 3:
                    prev_yaw=0

                state=7
        
        if prev_yaw==2:
            if yaw > 1.57:
                right_move=True
            else:
                right_move=False 
                prev_yaw=prev_yaw+1
                if prev_yaw > 3:
                    prev_yaw=0
 
                state=7
               
        if prev_yaw==3:
            if yaw > 0:
                right_move=True
            else:
                right_move=False
                prev_yaw=prev_yaw+1
                if prev_yaw > 3:
                    prev_yaw=0
 
                state=7
        if right_move:
            vel.linear.x=0
            vel.angular.z=0.4
            
        else:
            vel.linear.x=0
            vel.angular.z=0
            
      
    if state == 10:
        if prev_yaw==0 and state!=0:
            if yaw < 1.5707:
                left_move=True
            else:
                left_move=False
                prev_yaw=prev_yaw-1
                if prev_yaw < 0:
                    prev_yaw=3

                state=7               

        if prev_yaw==1 and state!=0:
            if yaw<0:
                left_move=True
            else:
                left_move=False
                prev_yaw=prev_yaw-1
                if prev_yaw < 0:
                    prev_yaw=3

                state=7
        
        if prev_yaw==2 and state!=0:
            if abs(yaw) > 1.57:
                left_move=True
            else:
                left_move=False 
                prev_yaw=prev_yaw-1
                if prev_yaw < 0:
                    prev_yaw=3
 
                state=7
               
        if prev_yaw==3 and state!=0:
            if yaw < 0:
                left_move=True
            else:
                left_move=False
                prev_yaw=prev_yaw-1
                if prev_yaw < 0:
                    prev_yaw=3
 
                state=7
        if left_move:
            vel.linear.x=0
            vel.angular.z=-0.4
            
        else:
            vel.linear.x=0
            vel.angular.z=0
    


    pub.publish(vel)
    print("state: ", state)
    print("yaw: ", yaw)

'''

'''

def listener():
    rospy.init_node('odom', anonymous=True)
    rospy.Subscriber("odom", Odometry, callback)
    rospy.Subscriber("scan", LaserScan, callback_scan)
    rospy.Subscriber("filter", Int32, callback_filter)

    rospy.spin()
	
if __name__ == '__main__':
    listener()

