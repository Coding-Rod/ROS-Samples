#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(x):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if x==1:
        goal.target_pose.pose.position.x = -4.0
        goal.target_pose.pose.position.y = 3.5
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0
    elif x==2:
        goal.target_pose.pose.position.x = -2.5
        goal.target_pose.pose.position.y = 3.5
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0  

    elif x==3:
        goal.target_pose.pose.position.x = 5.5
        goal.target_pose.pose.position.y = -4.5
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0 

    else:
        goal.target_pose.pose.position.x = 1.0
        goal.target_pose.pose.position.y = 2.0
        goal.target_pose.pose.orientation.z = 0.0
        goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    c=0
    try:
        while True:
            rospy.init_node('amcl_goal')
            result = movebase_client(1)
            rospy.loginfo("First goal reached")

            result = movebase_client(2)
            rospy.loginfo("Second goal reached")

            result = movebase_client(3)
            rospy.loginfo("Third goal reached")

            result = movebase_client(4)
            rospy.loginfo("Fourth goal reached")


            if result:
                rospy.loginfo("Goal execution done!")
            c=c+1
            print c
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
