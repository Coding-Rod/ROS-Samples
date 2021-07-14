#!/usr/bin/env python
from __future__ import print_function #

import roslib 
#en caso de informacion adicional
import sys
import numpy as np
import rospy
import cv2
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    
    self.image_pub = rospy.Publisher("modified_image",Image, queue_size=1)#image t topic, image tipo de dato

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/rrbot/camera1/image_raw",Image,self.callback)#nuestro topic
    self.place_pub = rospy.Publisher("Place", Int32, queue_size=10)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")#lo estavirtiendo a bgr 8
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape#el tamano
    if cols > 60 and rows > 60 :
      #cv2.rectangle(cv_image,(0,0),(640,480),(0,255,0),10)	
      lower =(30, 75, 35) # lower bound for each channel
      upper = (120, 250, 115)
      mask = cv2.inRange(cv_image, lower, upper)#mask=0_1	

      up=mask[0:239,0:639]#[0:2,0:2]
      bot_left=mask[0:479,0:212]#[0:2,0:2]
      bot_mid=mask[0:479,213:425]#[0:2,0:2,:demas capas]
      bot_right=mask[0:479,426:639]#[0:2,0:2]
      mask_vector=np.array([np.sum(up),np.sum(bot_left),np.sum(bot_mid),np.sum(bot_right)])
      #print (np.where (mask_vector==np.max(mask_vector)))
      index=np.where (mask_vector==np.max(mask_vector))
      #print (index[0][0])
      if (index[0][0]==0):
	print ("0")
        self.place_pub.publish(index[0][0])
      if (index[0][0]==1):
	print ("1")
        self.place_pub.publish(index[0][0])
      if (index[0][0]==2):
	print ("2")
        self.place_pub.publish(index[0][0])
      if (index[0][0]==3):
	print ("3")
        self.place_pub.publish(index[0][0])

    #cv2.imshow("Image window", cv_image)#nos da delay
    cv2.imshow("Mask ", mask)

    cv2.waitKey(3)
    #print (cv_image.shape)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(mask, "mono8"))#pulica la imagen alreves
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
