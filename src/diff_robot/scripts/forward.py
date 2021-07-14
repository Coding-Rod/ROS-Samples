#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
import cv2
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import tensorflow as tf
   

class image_converter:
    def __init__(self):
        self.loaded_model = tf.keras.models.load_model('/home/rigu/imt342p2_ws/src/model.h5')
        #self.loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        self.loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])  
	self.graph = tf.get_default_graph()      
        self.image_pub = rospy.Publisher("image_topic_2", Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw", Image, self.callback)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.vel = Twist()
        self.counter = 0
        self.flag = True
        self.dim = (150, 150)
        self.acceptation = 0.8
        self.bookshelf = 0
        self.hydrant = 0

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # pre-procesi -----------
        resized = cv2.resize(cv_image, self.dim)
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, 150, 150, 3))
        reshaped = np.vstack([reshaped])
	with self.graph.as_default(): 
            prediction = self.loaded_model.predict(reshaped)
        print(prediction)
        # -----------------
        print('Bookshelf count: {}, Fire hydrant count: {}.'.format(self.bookshelf, self.hydrant))
        if self.flag:
            if prediction.item(0) > self.acceptation:
                self.bookshelf += 1
                self.flag = False
            if prediction.item(1) > self.acceptation:
                self.hydrant += 1
                self.flag = False
        if prediction.item(2)< self.acceptation:
            self.flag = True

        self.vel.linear.x = 0
        self.vel.angular.z = 0.1
        self.pub.publish(self.vel)
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
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
