#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
etapa = 0
id = 0
forward_dist = 0
def movebase_client(x):
	global etapa
	global id
	global forward_dist
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()
	print("Etapa: ", etapa)
	print("F: ", forward_dist)
	print("ID: ", id)

	if x == 0:
		goal.target_pose.pose.position.x = 1.0
		goal.target_pose.pose.position.y = 0.0
		goal.target_pose.pose.orientation.z = -0.7
		goal.target_pose.pose.orientation.w = 0.7
	if x==1:
		goal.target_pose.pose.position.x = 1.0
		goal.target_pose.pose.position.y = 0.0
		goal.target_pose.pose.orientation.z = 0.7
		goal.target_pose.pose.orientation.w = 0.7
	elif x == 2 :
		goal.target_pose.pose.position.x = -1.0
		goal.target_pose.pose.position.y = 1.0
		goal.target_pose.pose.orientation.z = -1.0
		goal.target_pose.pose.orientation.w = 0.0
	if forward_dist < 1:
		if etapa != 0:
			etapa = 0


	client.send_goal(goal)
	wait = client.wait_for_result()
	if not wait:
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available!")
	else:
		return client.get_result()

def callback_multi(data):
	global id
	global per
	id = data.data[0]
	per = data.data[1]

def callback_scan(data):
	global left_dist
	global right_dist
	global forward_dist
	global flag
	flag = 0
	left_dist = data.ranges[90]
	right_dist = data.ranges[270]
	forward_dist = data.ranges[0]

if __name__ == '__main__':
	c=0
	global etapa
	try:
		rospy.Subscriber("id", Float64MultiArray, callback_multi)
		rospy.Subscriber("scan", LaserScan, callback_scan)
		while True:
			rospy.init_node('send_goal')
			if etapa == 0:
				result = movebase_client(1)
				rospy.loginfo("Etapa 1 Reached!")
				etapa = 1
			if etapa == 1 and id == 25:
				result = movebase_client(0)
				rospy.loginfo("Etapa 2 Reached!")
				etapa = 2
			if etapa == 2:
				result = movebase_client(2)
				rospy.loginfo("First Goal Reached!")


			if result:
				rospy.loginfo("Goal execution done!")
			c=c+1
			print c
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation test finished.")
