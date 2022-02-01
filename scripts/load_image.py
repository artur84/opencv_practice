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
        img_1 = cv2.imread('/home/user/catkin_ws/src/opencv_for_robotics_images/Unit_2/Course_images/test_image_1.jpg')

        #Display the image in a window
        cv2.imshow('test_image_1',img_1)
        r = rospy.Rate(10) #10Hz 
        while not rospy.is_shutdown(): 
            cv2.waitKey(1)
            r.sleep() 
        cv2.destroyAllWindows()
        


    def camera_callback(self,data):
        try:
            # We select bgr8 because its the OpenCV encoding by default
            self.cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            #Save the image "img" in the current path 
        cv2.imwrite('robot_image.jpg', self.cv_image)


if __name__ == '__main__':
    rospy.init_node('load_image', anonymous=True)
    showing_image_object = ShowingImage()
