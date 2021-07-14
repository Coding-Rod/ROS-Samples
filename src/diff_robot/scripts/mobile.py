#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import LaserScan
points=720

xpos=0
ypos=0
xposaux=0
yposaux=0
pos=0
roll=0
pitch=0
yaw=0
place=0

def get_pose(data):
    global roll,pitch,yaw
    #rospy.loginfo("X: %f",data.pose.pose.position.x)
    #rospy.loginfo("Y: %f",data.pose.pose.position.y)
    global xpos
    global ypos
    global xposaux
    global yposaux
    orientation_q=data.pose.pose.orientation
    orientation_list=[orientation_q.x,orientation_q.y,orientation_q.z,orientation_q.w]
    (roll,pitch,yaw)=euler_from_quaternion(orientation_list)
    xpos=data.pose.pose.position.x
    ypos=data.pose.pose.position.y
    yaw=yaw+3.141593
    #rospy.loginfo("euler orientation: roll %f, pitch:%f, yaw:%f",roll,pitch,yaw)

def index(data):
    global place
    place=data.data

def publisher():
    rospy.init_node('mobile_subscriber',anonymous=True)
    global place
    global dist
    global roll,pitch,yaw
    global xpos
    global ypos
    rospy.Subscriber('odom',Odometry,get_pose)
    rospy.Subscriber('Place',Int32,index)
    vel_pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)
    vel=Twist()
    yaw2=0
    rate=rospy.Rate(30)
    while not rospy.is_shutdown():
        rate.sleep()
	print place       
	if(place==2):
            while(place==2):
                vel.linear.x=0.3
                vel.angular.z=0
                vel_pub.publish(vel)
		print place
	        rate.sleep()
	if(place==1):
            while(place==1):
                vel.linear.x=0.3
                vel.angular.z=-0.35
                vel_pub.publish(vel)
		print place
	        rate.sleep()
	if(place==3):
            while(place==3):
                vel.linear.x=0.3
                vel.angular.z=0.35
                vel_pub.publish(vel)
		print place
	        rate.sleep()



if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
	
