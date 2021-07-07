#!/usr/bin/env python 
import rospy #ros python packages
from sensor_msgs.msg import JointState
import std_msgs.msg

def comparator(a, b, step):
    if a < b:
        a += step
    elif a > b:
        a -= step
    return round(a,2)

def two_move(ax1,ax2,ax1_expect,ax2_expect,move,next_move,step):
    change = True
    change = not ((ax1 == ax1_expect) and (ax2 == ax2_expect))

    ax1 = comparator(ax1, ax1_expect,step)
    ax2 = comparator(ax2, ax2_expect,step)

    if change:
        return ax1,ax2,move
    else:
        return ax1,ax2,next_move

def one_move(ax,ax_expect,move,next_move,step):
    change = True
    change = not(ax == ax_expect)

    ax = comparator(ax, ax_expect,step)

    if change:
        return ax,move
    else:
        return ax,next_move

 
def point_publisher():
    pub = rospy.Publisher('joint_states', JointState, queue_size=20) #position -> Topic, Point -> Message type, queue_size
    rospy.init_node('joint_states_publisher', anonymous=True) #point_publisher -> node name, anonymous=True -> no id
    rate = rospy.Rate(5) # 5Hz -> delay(Hz)
    msg = JointState() # Point topic object
    h = std_msgs.msg.Header()
    angles = [0,-1.2,2.2,0,0,0]
    msg.name = ['joint_a1', 'joint_a2', 'joint_a3', 'joint_a4', 'joint_a5', 'joint_a6']
    move = 'p1'
    step = 0.1
    initial = True
    while not rospy.is_shutdown(): #while ros is running
        h.stamp = rospy.Time.now()
        h.seq +=1
        msg.header = h
        if initial:
            angles = [0,-1.2,2.2,0,0,0]
            initial = False
        else:
            # Position 1 (initial)
            if move == 'p1':
                angles[1],angles[2],move = two_move(angles[1],angles[2],-0.7,2.2,'p1','p2',step)
            # Position 2 (hang)
            if move == 'p2':
                angles[5],move = one_move(angles[5],0.5,'p2','p3',0.1)
            # Position 3 (up)
            if move == 'p3':
                angles[1],angles[2],move = two_move(angles[1],angles[2],-1.2,2.7,'p3','p4',step)
            # Position 4 (right)
            if move == 'p4':
                angles[0],move = one_move(angles[0],-1.5,'p4','p5',step)
                
            # Position 5 (down)
            if move == 'p5':
                angles[1],angles[2],move = two_move(angles[1],angles[2],-0.7,2.2,'p5','p6',step)
            # Position 6 (drop)
            if move == 'p6':
                angles[5],move = one_move(angles[5],0,'p6','p7',step)
            # Position 7 (up)
            if move == 'p7':
                angles[1],angles[2],move = two_move(angles[1],angles[2],-1.2,2.7,'p7','p8',step)
            # Position 8 (left)
            if move == 'p8':
                angles[0],move = one_move(angles[0],0,'p8','p1',step)
        
        msg.position = angles
        rospy.loginfo(move)
        pub.publish(msg) #Publish a message
        rate.sleep() #transforms rate(Hz) in seconds

if __name__ == '__main__':
    try:
        point_publisher()
    except rospy.ROSInterruptException:
        pass