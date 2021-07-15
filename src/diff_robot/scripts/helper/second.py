#!/usr/bin/env python
from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Int32
import cv2
import rospy
import sys
import numpy as np
from geometry_msgs.msg import Twist
pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
import roslib
#roslib.load_manifest('computer_vision')

rvel=0.6
gvel=0.4
angic=-0.4
angdc=0.4
angil=-0.5
angdl=0.5
vel=Twist()
class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2", Image, queue_size=10)
        self.dir_pub = rospy.Publisher("direction", Int32, queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rrbot/camera1/image_raw", Image, self.callback)
        

    def callback(self, data):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv,(25,52,72),(102,255,255))
        target = cv2.bitwise_and(cv_image, cv_image, mask=mask1)

        l1=mask1[50:479, 128:203]
        l2=mask1[50:479, 204:279]
        cc=mask1[50:479, 280:360]
        r2=mask1[50:479, 361:436]
        r1=mask1[50:479, 437:512]

        scores = np.array([np.sum(l1), np.sum(l2), np.sum(cc),np.sum(r2),np.sum(r1)])
        indexes = np.where(scores == np.max(scores))
        index = indexes[0][0]
        print(index)
        if(np.max(scores>5)):
            if (index==2):
                vel.linear.x=rvel
                vel.angular.z=0.0
            elif(index==0):
                vel.linear.x=gvel
                vel.angular.z=angil
            elif(index==1):
                vel.linear.x=gvel
                vel.angular.z=angic
            elif(index==3):
                vel.linear.x=gvel
                vel.angular.z=angdc
            elif(index==4):
                vel.linear.x=gvel
                vel.angular.z=angdl
        else:
            vel.linear.x=0.0
            vel.angular.z=0.0   
        pub.publish(vel)

        cv2.imshow("Image window", target)
        cv2.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

def main(args):

    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
