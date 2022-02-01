#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2


class ShowingImage(object):

    def __init__(self):
    
        self.image_sub = rospy.Subscriber("/two_wheels_robot/camera1/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()

        #Read the image file
        #img_1 = cv2.imread('/home/user/catkin_ws/src/opencv_for_robotics_images/Unit_2/Course_images/test_image_1.jpg')
        example_path = '/home/user/catkin_ws/src/opencv_practice/scripts/robot_image.jpg'    
        img = cv2.imread(example_path)
        cv2.imshow('robot_image',img)
        #Display the image in a window
        self.img_received = 0 #Flag to make sure we received an image before showing it.
        r = rospy.Rate(10) #10Hz 
        while not rospy.is_shutdown(): 
            if self.img_received:
                cv2.imshow('image',self.cv_image)
            cv2.waitKey(1)
            r.sleep() 
        cv2.destroyAllWindows()
        


    def camera_callback(self,data):
        try:
            # We select bgr8 because its the OpenCV encoding by default
            self.cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        self.img_received=1
        


if __name__ == '__main__':
    rospy.init_node('load_image_2', anonymous=True)
    showing_image_object = ShowingImage()
