#!/usr/bin/env python
import rospy
import actionlib
from time import sleep
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
state = 0
id = 0
forward_dist = 0
animal=int(input("Ingrese el numero del objeto que busca (18->perro, 17->gato, 1->persona): "))
def movebase_client(x):
	global state
	global id
	global forward_dist
	global animal
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()
	print("State: ", state)
	print("Id object: ", id)

	if x == 1:
		goal.target_pose.pose.position.x = -2.06705944915
		goal.target_pose.pose.position.y = 0.241622111274
		goal.target_pose.pose.orientation.z = 0.916957998892
		goal.target_pose.pose.orientation.w = 0.398983744364
	elif x == 2:
		goal.target_pose.pose.position.x = -2.57276028425
		goal.target_pose.pose.position.y = -2.28588301603
		goal.target_pose.pose.orientation.z = 0.899966161393
		goal.target_pose.pose.orientation.w = 0.435959755421
	elif x == 3 :
		goal.target_pose.pose.position.x = -0.108970540988
		goal.target_pose.pose.position.y = -2.11538308649
		goal.target_pose.pose.orientation.z = 0.980982059506
		goal.target_pose.pose.orientation.w = 0.194098425877

	elif x == 4 :
		goal.target_pose.pose.position.x = 0.0
		goal.target_pose.pose.position.y = 0.0
		goal.target_pose.pose.orientation.z = 0.0
		goal.target_pose.pose.orientation.w = 1.0


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
	print("Id object: ", id)

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
	global state
	global animal
	global id
	try:
		rospy.Subscriber("id", Float64MultiArray, callback_multi)
		rospy.Subscriber("scan", LaserScan, callback_scan)
		while True:
			rospy.init_node('send_goal')
			if state == 0:
				result = movebase_client(1)
				sleep (3)
				rospy.loginfo("buscando!")
				if id == animal: 
				    result = movebase_client(4)
				else:
				    state = 1
			if state == 1:
				result = movebase_client(2)
				sleep (3)
				rospy.loginfo("buscando!")
				if id == animal:
				    result = movebase_client(4)
				else:
				    state = 2
			if state == 2:
				result = movebase_client(3)
				sleep (3)
				rospy.loginfo("Buscando!")
				if id == animal: 
				    result = movebase_client(4)
				else:
				    result = movebase_client(4)



			if result:
				rospy.loginfo("finish!")
			c=c+1
			print c
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation test finished.")
