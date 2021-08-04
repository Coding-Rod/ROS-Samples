#!/usr/bin/env python
import rospy
import actionlib
from vision_msgs.msg import Detection2DArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

detect = True
id = 0
x = 0

def callback(data):
    global id
    global detect
    global x
    
    if detect:
        try:
            id = data.detections[0].results[0].id
            if id == 51 or id == 59:
                x = 1
                detect = False
            if id == 52:
                x = 2
                detect = False
            print('banana' if id == 52 else 'pizza')
        except Exception as e:
            print(e)

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if x==1:
        goal.target_pose.pose.position.x = 6.0
        goal.target_pose.pose.position.y = -4.5
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
    elif x==2:
        goal.target_pose.pose.position.x = 1.0
        goal.target_pose.pose.position.y = 3.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0  

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def listener():
    rospy.init_node('amcl_goal')
    rospy.Subscriber("objects", Detection2DArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()