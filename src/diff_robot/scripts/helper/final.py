#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import Float64MultiArray, Int32, String
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist, Point
from time import sleep
point = 0
forward_dist = 0
blue_percentage = 0
green_percentage = 0
red_percentage = 0
yaw = 0.0
flag = True
red = 0 
green = 0
vel=Twist()

pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)

def movebase_client(x):
	global point
        global objct
        global blue_percentage
        global red_percentage
        global green_percentage
	global red
	global green
        global flag
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()
	print("Etapa: ", point)
	print("Rojos: ", red)
	print("Verdes: ", green)


	if x==0:
		goal.target_pose.pose.position.x = 3
		goal.target_pose.pose.position.y = 1
		goal.target_pose.pose.orientation.z = 0.05
		goal.target_pose.pose.orientation.w = 1.00
	elif x==1:
		goal.target_pose.pose.position.x = 3
		goal.target_pose.pose.position.y = -1
		goal.target_pose.pose.orientation.z = 0.996
		goal.target_pose.pose.orientation.w = 0.094
	elif x==2:
		goal.target_pose.pose.position.x = -2.34
		goal.target_pose.pose.position.y = 0.09
		goal.target_pose.pose.orientation.z = 1.00
		goal.target_pose.pose.orientation.w = 0.02
	elif x==3:
		goal.target_pose.pose.position.x = -4.69
		goal.target_pose.pose.position.y = 0.77
		goal.target_pose.pose.orientation.z = 1.00
		goal.target_pose.pose.orientation.w = 0.04
	elif x==4:
		goal.target_pose.pose.position.x = -4.73
		goal.target_pose.pose.position.y = -2.12
		goal.target_pose.pose.orientation.z = 0.06
		goal.target_pose.pose.orientation.w = 1.00

	client.send_goal(goal)
	wait = client.wait_for_result()
	if not wait:
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available!")
	else:
		return client.get_result()

def callback_multi(data):
	global id
	global percentage
	id = data.data[0]
	percentage = data.data[1]

def callback_scan(data):
	global left_dist
	global right_dist
	global forward_dist
	global flag
	flag = 0
	left_dist = data.ranges[90]
	right_dist = data.ranges[270]
	forward_dist = data.ranges[0]

def callback_filter(data):
        global red_percentage
        global green_percentage

        red_percentage=int(data.y)
        green_percentage=int(data.z)


if __name__ == '__main__':
	c=0
        global objct

	try:
		rospy.Subscriber("scan", LaserScan, callback_scan)
                rospy.Subscriber("filter", Point, callback_filter)
		while True:
			rospy.init_node('send_goal')
			if point == 0:
			    result = movebase_client(0)
			    rospy.loginfo("Point 1 Reached!")
		            point = 1
			if point == 1:
                            if red_percentage >= 200:
				red += 1
				result = movebase_client(1)
				point = 2
                            if green_percentage >= 200:
				green += 1
				result = movebase_client(1)
				point = 2
			    else:
			        vel.angular.z = 0.5
                                pub.publish(vel)
                                if red_percentage >= 200:
				    red += 1
				    result = movebase_client(1)
				    point = 2
                                if green_percentage >= 200:
				    green += 1
				    result = movebase_client(1)
				    point = 2

			if point == 2:
                            if red_percentage >= 200:
				red += 1
				result = movebase_client(2)
				point = 3
                            if green_percentage >= 200:
				green += 1
				result = movebase_client(2)
				point = 3
			    else:
			        vel.angular.z = 0.5
                                pub.publish(vel)
                                if red_percentage >= 200:
				    red += 1
				    result = movebase_client(2)
				    point = 3
                                if green_percentage >= 200:
				    green += 1
				    result = movebase_client(2)
				    point = 3

			if point == 3:
                            if red_percentage >= 200:
				red += 1
				result = movebase_client(3)
				flag = False
				point = 4
                            if green_percentage >= 200:
				green += 1
				result = movebase_client(3)
				point = 4
			    else:
			        vel.angular.z = 0.5
                                pub.publish(vel)
                                if red_percentage >= 200:
				    red += 1
				    result = movebase_client(3)
				    flag = False
				    point = 4
                                if green_percentage >= 200:
				    green += 1
				    result = movebase_client(3)
				    point = 4

			if point == 4:
                            if red_percentage >= 200:
				red += 1
				result = movebase_client(4)
				point = 5
                            if green_percentage >= 200:
				green += 1
				result = movebase_client(4)
				point = 5
			    else:
			        vel.angular.z = 0.5
                                pub.publish(vel)
                                if red_percentage >= 200:
				    red += 1
				    result = movebase_client(4)
				    point = 5
                                if green_percentage >= 200:
				    green += 1
				    result = movebase_client(4)
				    point = 5

			c=c+1
			#print c
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation test finished.")

