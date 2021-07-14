#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2 as cv
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

path = "/home/rigu/imt342p2_ws/src/diff_robot/scripts/raw_data/"


class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2", Image)
        self.vel_pub = rospy.Publisher("cmd_vel", Twist, queue_size=5)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw", Image, self.callback)
        self.vel = Twist()
        self.counter = 0
        self.flag = True

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        if self.counter < 150:
            self.vel.linear.x = 0.1
            self.vel.angular.z = 0
        if 150 <= self.counter < 450:
            self.vel.linear.x = -0.1
            self.vel.angular.z = 0
        if 450 <= self.counter < 600:
            self.vel.linear.x = 0.1
            self.vel.angular.z = 0
        if 600 <= self.counter < 650:
            self.vel.linear.x = 0
            self.vel.angular.z = 0.1
        if 650 <= self.counter < 750:
            self.vel.linear.x = 0
            self.vel.angular.z = -0.1
        if self.counter > 750:
            self.vel.linear.x = 0
            self.vel.angular.z = 0
            self.flag = False
        self.counter += 1
        self.vel_pub.publish(self.vel)
        print(self.counter)
        if self.flag:
            cv.imwrite(path + "fire-" + str(self.counter) + ".jpg", cv_image)
            if self.counter >= 1000:
                return
        cv.imshow("Image window", cv_image)
        cv.waitKey(1)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)


def main(args):
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
