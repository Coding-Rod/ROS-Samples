#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
from tf.transformations import quaternion_from_euler
import tf
import sys
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

id = 0
state = 0
dist = 0
left_dist = 0
right_dist = 0
front_dist = 0
color = 0
init_distances = [0,0,0]
ids = [17, 52, 59]
search_id = 0

def odom_callback(data):
    global x
    global y
    global yaw
    x=data.pose.pose.position.x
    y=data.pose.pose.position.y
    euler=tf.transformations.euler_from_quaternion((data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z,data.pose.pose.orientation.w))
    yaw=euler[2] 

def mask_callback(data):
    global color
    color = data.data

def id_callback(data):
    global id
    try:
        id=data.detections[0].results[0].id
    except:
        pass

def callback_scan(data):
    global left_dist
    global right_dist
    global front_dist
    left_dist=data.ranges[89]
    right_dist=data.ranges[269]
    front_dist=data.ranges[179]

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
    global dist
    global left_dist
    global right_dist
    global front_dist

    while True:
        rospy.init_node('amcl_goal_id', anonymous=True)
        rospy.Subscriber("objects", Detection2DArray, id_callback)
        rospy.Subscriber("odom", Odometry, odom_callback)
        rospy.Subscriber("scan", LaserScan, callback_scan)

        #TODO: search id based on color
        print(state)
        if state == 0:
            init_distances[0] = left_dist
            init_distances[1] = front_dist
            init_distances[2] = right_dist
            state = 1

        print(state)
        if state == 1:
            minim = init_distances.index(min(init_distances))
            if minim == 0:
                result = movebase_client( 2.975734, 1.244423, 1.57079633)
            if minim == 1:
                result = movebase_client( 2.975734, 1.244423, 1.57079633)
            if minim == 2:
                result = movebase_client( 2.975734, 1.244423, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            search_id = ids[color]
            print(search_id)
            state = 2

        # Positions
        print(state)
        if state == 2:
            result = movebase_client( 5.876358, 2.813194, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 3
            dist = left_dist + right_dist

        print(state)
        if state == 3:
            result = movebase_client( 0.039904, 2.909452, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 4
            print('total distance: ',dist)
        
        print(state)
        if state == 4:
            result = movebase_client( 5.876358, 2.813194, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 5
            dist = left_dist + right_dist

        print(state)
        if state == 5:
            result = movebase_client( 0.039904, 2.909452, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 6
            print('total distance: ',dist)
            
        print(state)
        if state == 6:
            result = movebase_client( 0.039904, 2.909452, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 7
            print('total distance: ',dist)

        #TODO: Rotate based on a counter
            


if __name__ == '__main__':
    main(sys.argv)
    
