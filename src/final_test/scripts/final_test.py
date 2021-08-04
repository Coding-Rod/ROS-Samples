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
front_dist = 0
vel = Twist()
prev_yaw = 0
x = 0
y = 0
yaw = 0
go = 0

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

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
    global front_dist
    front_dist=data.ranges[0]

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
    global prev_yaw
    global state
    global front_dist
    global yaw
    global x 
    global y
    global go

    while True:
        rospy.init_node('final_test', anonymous=True)
        rospy.Subscriber("objects", Detection2DArray, id_callback)
        rospy.Subscriber("odom", Odometry, odom_callback)
        rospy.Subscriber("scan", LaserScan, callback_scan)

        if state == 0:
            vel.angular.z = -1
            if front_dist > 4:
                prev_yaw = yaw
                state = 1

        if state == 1:
            vel.angular.z = -0.05
            if abs(prev_yaw - yaw) > 0.15:
                vel.angular.z = 0
                state = 2

        if state == 2:
            print(id)
            vel.linear.x = 0.5
            if id == 17:
                vel.linear.x = 0
                state = 3
                go = 17
            if id == 18:
                vel.linear.x = 0
                state = 3
                go = 18
            

        # Positions 
        if state == 3: # cat
            if not ((x<-3.5 or x>3.5) or (y<-3.5 and y>3.5)):
                print('go')
                vel.linear.x = 0.5
            else:
                if go == 17:
                    state = 4
                else:
                    state = 5
        
        if state == 4: # cat
            result = movebase_client( 3.798539, -4.055027, -1.600749)
            rospy.loginfo(str(state)+" goal reached")

        if state == : # dog
            result = movebase_client( -4.047993, 4.085038, 1.569714)
            rospy.loginfo(str(state)+" goal reached")
        pub.publish(vel)
        

if __name__ == '__main__':
    main(sys.argv)
    
