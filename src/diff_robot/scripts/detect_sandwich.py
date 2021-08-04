#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from vision_msgs.msg import Detection2DArray
import sys

class object_detector:
    def __init__(self):
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        self.vel = Twist()
        self.detect_sub = rospy.Subscriber("objects", Detection2DArray, self.callback)

    def callback(self, data):
        try:
            self.id = data.detections[0].results[0].id
            self.x = data.detections[0].bbox.center.x
        except:
            self.id = 0
            pass
        if self.id == 11:
            print('ID detected', self.id)
            if self.x > 230 and self.x < 250:
                self.vel.angular.z = 0
            elif self.x > 250:
                self.vel.angular.z = 0.2
            else:
                self.vel.angular.z = -0.2
            self.id = 0
        else:
            self.vel.angular.z = 0.2
            print('No detections')
        self.pub.publish(self.vel)

def main(args):
    rospy.init_node('object_detector', anonymous=True)
    od = object_detector()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)