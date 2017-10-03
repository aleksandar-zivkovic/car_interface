#!/usr/bin/env python
import rospy
from beginner_tutorials.msg import Wheels


def talker():
    pub = rospy.Publisher('custom_chatter', Wheels)
    rospy.init_node('custom_talker', anonymous=True)
    r = rospy.Rate(10) #10hz
    msg = Wheels()
    msg.left.speed = 17
    msg.left.direction = 0
    msg.left.dist = 0

    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        msg.left.dist += 1
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass

