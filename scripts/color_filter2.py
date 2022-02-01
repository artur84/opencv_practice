#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class ShowingImage(object):

    def __init__(self):
        self.image_sub = rospy.Subscriber("two_wheels_robot/camera1/image_raw",Image,self.camera_callback)
        self.bridge_object = CvBridge()

        self.img_received = 0 #Flag to make sure we received an image before showing it.
        r = rospy.Rate(10) #10Hz 
        while not rospy.is_shutdown(): 
            if self.img_received:
                #I resized the image so it can be easier to work with
                
                image = cv2.resize(self.cv_image,(300,300))

                #Once we read the image we need to change the color space to HSV
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                #Hsv limits are defined
                #here is where you define the range of the color you´re looking for
                #each value of the vector corresponds to the H,S & V values respectively
                min_green = np.array([40,50,50])
                max_green = np.array([60,255,255])

                min_red = np.array([0,45,142])
                max_red = np.array([10,255,255])

                min_blue = np.array([100,50,50])
                max_blue = np.array([120,255,255])


                #This is the actual color detection 
                #Here we will create a mask that contains only the colors defined in your limits
                #This mask has only one dimention, so its black and white }
                mask_g = cv2.inRange(hsv, min_green, max_green)
                mask_r = cv2.inRange(hsv, min_red, max_red)
                mask_b = cv2.inRange(hsv, min_blue, max_blue)

                #We use the mask with the original image to get the colored post-processed image
                res_b = cv2.bitwise_and(image, image, mask= mask_b)
                res_g = cv2.bitwise_and(image,image, mask= mask_g)
                res_r = cv2.bitwise_and(image,image, mask= mask_r)

                cv2.imshow('Image',image)
                cv2.imshow('Green',res_g)
                cv2.imshow('Red',res_r)
                cv2.imshow('Blue',res_b)
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
    rospy.init_node('color_filter2', anonymous=True)
    showing_image_object = ShowingImage()
