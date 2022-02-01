#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class ShowingImage(object):

    def __init__(self):
        self.image_sub = rospy.Subscriber("/two_wheels_robot/camera1/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()
        self.image_received = 0 #Flag to indicate that we have already received an image
        r = rospy.Rate(10) #10Hz 
        while not rospy.is_shutdown(): 
            if self.image_received:
                 cv2.imshow('image',self.cv_image)
            cv2.waitKey(1)
            r.sleep() 
        cv2.destroyAllWindows()

    def camera_callback(self,data):
        self.image_received=1
        try:
            # We select bgr8 because its the OpenCV encoding by default
            self.cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
       
        

if __name__ == '__main__':
    rospy.init_node('opencv_example1', anonymous=True)
    showing_image_object = ShowingImage()
