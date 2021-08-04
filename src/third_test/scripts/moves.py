#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
from tf.transformations import quaternion_from_euler
import sys

id = 0
state = 1
cats = 0
dogs = 0

def id_callback(data):
    global id
    try:
        id=data.detections[0].results[0].id
    except:
        pass


def movebase_client(x_post, y_post, yaw):
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
    global cats
    global dogs

    while True:
        rospy.init_node('moves', anonymous=True)
        rospy.Subscriber("objects", Detection2DArray, id_callback)

        if state == 1:
            result = movebase_client(1.408028, -0.493724, 0.017920)
            rospy.loginfo(str(state)+" goal reached")
            state = 2
            if id == 17:
                print('Cat detected!')
                cats += 1
            else:
                print('Dog detected!')
                dogs += 1

        if state == 2:
            result = movebase_client(0.296930, -0.839372, -1.586309)
            rospy.loginfo(str(state)+" goal reached")
            state = 3
            if id == 17:
                print('Cat detected!')
                cats += 1
            else:
                print('Dog detected!')
                dogs += 1

        if state == 3:
            result = movebase_client(-0.785485, -0.395630, -3.118760)
            rospy.loginfo(str(state)+" goal reached")
            state = 4
            if id == 17:
                print('Cat detected!')
                cats += 1
            else:
                print('Dog detected!')
                dogs += 1

        if state == 4:
            result = movebase_client(-0.003255, 0.900690, 1.564504)
            rospy.loginfo(str(state)+" goal reached")
            state = 5
            if id == 17:
                print('Cat detected!')
                cats += 1
            else:
                print('Dog detected!')
                dogs += 1

        if state == 5:
            if cats == dogs:
                result = movebase_client(3.709100, -2.707660, 1.564963)
            elif cats > dogs:
                result = movebase_client(3.371563, -0.101304, -0.001009)
            else:
                result = movebase_client(-2.642778, 0.689771, 1.564985)
            rospy.loginfo(str(state)+" goal reached")
            print('cats: ',cats)
            print('dogs: ',dogs)
            state = 0
            
if __name__ == '__main__':
    main(sys.argv)
    
