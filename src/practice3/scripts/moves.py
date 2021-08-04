#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
from tf.transformations import quaternion_from_euler
import sys
from sensor_msgs.msg import LaserScan

id = 0
state = 1
dist = 0
left_dist = 0
right_dist = 0



def id_callback(data):
    global id
    try:
        id=data.detections[0].results[0].id
    except:
        pass

def callback_scan(data):
    global left_dist
    global right_dist
    left_dist=data.ranges[89]
    right_dist=data.ranges[269]

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

    selector = bool(input('Type \n1.pizza \n0.kite\n'))
    while True:
        rospy.init_node('amcl_goal_id', anonymous=True)
        rospy.Subscriber("objects", Detection2DArray, id_callback)
        rospy.Subscriber("scan", LaserScan, callback_scan)

        if selector: # Pizza
            if state == 1:
                result = movebase_client( 2.975734, 1.244423, 1.57079633)
                rospy.loginfo(str(state)+" goal reached")
                state = 2
                if id == 59:
                    print('Pizza detected!')

            if state == 2:
                result = movebase_client( 5.876358, 2.813194, 1.57079633)
                rospy.loginfo(str(state)+" goal reached")
                state = 3
                dist = left_dist + right_dist

        else: # Kite
            if state == 1:
                result = movebase_client(-2.898362, 1.234176, 1.57079633)
                rospy.loginfo(str(state)+" goal reached")
                state = 2
                if id == 38:
                    print('Kite detected!')

            if state == 2:
                result = movebase_client(-5.753002, 2.794272, 1.57079633)
                rospy.loginfo(str(state)+" goal reached")
                state = 3
                dist = left_dist + right_dist

        if state == 3:
            result = movebase_client( 0.039904, 2.909452, 1.57079633)
            rospy.loginfo(str(state)+" goal reached")
            state = 0
            print('total distance: ',dist)
            


if __name__ == '__main__':
    main(sys.argv)
    
