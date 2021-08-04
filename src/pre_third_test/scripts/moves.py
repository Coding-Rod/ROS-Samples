#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
from tf.transformations import quaternion_from_euler
import sys

state = 0 
ultimo_valor = 0 
boat = 0 
bicycle = 0
col = 0

def color(data):
    global col
    col = data.data

def id_callback(data):
    global id
    try:
        id=data.detections[0].results[0].id
    except:
        pass  

def movebase_client(x_post, y_post, yaw):

    global boat
    global bicycle
    global id
    global state

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    # convert yaw to quaternion
    q = quaternion_from_euler(0, 0, yaw)
    goal.target_pose.pose.position.x = x_post
    goal.target_pose.pose.position.y = y_post
    goal.target_pose.pose.orientation.x = q[0]
    goal.target_pose.pose.orientation.y = q[1]
    goal.target_pose.pose.orientation.z = q[2]
    goal.target_pose.pose.orientation.w = q[3]

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


def main(args):
    global state
    global boat
    global bicycle

    while True:
        rospy.init_node('amcl_goal_id', anonymous=True)
        rospy.Subscriber("objects", Detection2DArray, id_callback)

        if col == 1:
            print('Bicycles: ', bicycle)
        if col == 2:
            print('Boats: ', boat)
        if state == 0:
            result = movebase_client(-0.000940, 1.601694, 1.608927)
            state = 1
            rospy.loginfo(str(state)+" goal reached")
            rospy.Subscriber("mask",Int32, color)
            if col > 0:
                print('Green' if col == 1 else 'Blue')
            else:
                state = 0

        if state == 1:
            result = movebase_client(3.443970, 2.155374, 0.867013)
            state = 2
            rospy.loginfo(str(state)+" goal reached")
            if id== 9:
                boat +=1
                print('boat: ',boat)

        if state == 2:
            result = movebase_client(3.186482, 2.342973, 2.528817)
            state = 3
            rospy.loginfo(str(state)+" goal reached")
            if id == 2:
                bicycle +=1
                print('bicycle: ',bicycle)

        if state == 3:
            result = movebase_client(3.782781, 0.216311, -1.211908)
            state = 4
            rospy.loginfo(str(state)+" goal reached")
            if id== 9:
                boat +=1
                print('boat: ',boat)

        if state == 4:
            result = movebase_client(2.887589, 0.075320, -2.055787)
            state = 5
            rospy.loginfo(str(state)+" goal reached")
            if id== 9:
                boat +=1
                print('boat: ',boat)

        if state == 5:
            result = movebase_client(-3.846847, 2.200315, 2.310173)
            state = 6
            rospy.loginfo(str(state)+" goal reached")
            if id == 2:
                bicycle +=1
                print('bicycle: ',bicycle)
        if state == 6:
            result = movebase_client(-3.477884, 1.701835, -0.855203)
            state = 7
            rospy.loginfo(str(state)+" goal reached")
            if id== 9:
                boat +=1
                print('boat: ',boat)
        if state == 7:
            result = movebase_client(-3.947226, 0.106301, -2.247186)
            state = 8
            rospy.loginfo(str(state)+" goal reached")
            if id== 9:
                boat +=1
                print('boat: ',boat)
        if state == 8:
            result = movebase_client(-3.452947, 0.023464, -0.885019)
            state = 9
            rospy.loginfo(str(state)+" goal reached")
            if id == 2:
                bicycle +=1
                print('bicycle: ',bicycle)
        if state == 9:
            print('---------- [Complete] ----------')
            state = 10

if __name__ == '__main__':
    main(sys.argv)
    