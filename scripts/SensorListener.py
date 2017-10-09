#!/usr/bin/env python
import rospy
from car_interface.msg import Wheels

def callback(data):
    rospy.loginfo("Speed %d direction %d distance %d" % (data.left.speed, data.left.direction, data.left.dist))

def listener():
    rospy.init_node('custom_listener', anonymous=True)
    rospy.Subscriber("custom_chatter", Wheels, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

