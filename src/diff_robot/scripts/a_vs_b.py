#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
from tensorflow import keras

class image_converter:

  def __init__(self):
    self.loaded_model=tf.keras.models.load_model('model_name.h5')
    self.loaded_model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
    self.graph = tf.get_default_graph() 
    self.image_pub = rospy.Publisher("image_topic_2",Image)
    self.vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=5)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("diff_robot/camera/image_raw",Image,self.callback)
    self.vel=Twist()
    self.counter=0

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image,(400,400),300,(0,0,255))

    resized=cv2.resize(cv_image,dim)
    normalized=resized/255.0
    reshaped=np.reshape(normalized,(1,150,150,3)) 
    reshaped=np.vstack([reshaped])
    with self.graph.as_default(): 
      print(self.loaded_model.predict(reshaped)) 

    #plt.imshow(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    #plt.draw()
    #plt.show()
    #plt.pause(0.01)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(1)

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
