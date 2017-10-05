#!/usr/bin/env python
from __future__ import print_function

import rospy
from beginner_tutorials.msg import Wheels
from beginner_tutorials.msg import Distance
import serial
import select
import sys
import termios
import atexit
import sensorhub

pub = rospy.Publisher('custom_chatter', Wheels)

wheelPublisher = Wheels()
distancePublisher = Distance()

def publishPing(ping):
	return
	
def publishPong(ping):
	return
	
def publishWheels(left, right):
	global pub
	global wheelPublisher

	wheelPublisher.left.when = left.when
	wheelPublisher.right.when = right.when

	wheelPublisher.left.speed = left.speed
	wheelPublisher.right.speed = right.speed
	
	wheelPublisher.left.direction = left.direction
	wheelPublisher.right.direction = right.direction
	
	wheelPublisher.left.dist = left.turn
	wheelPublisher.right.dist = right.turn
	
	wheelPublisher.left.dist_abs = right_dist
	wheelPublisher.right.dist_abs = right.dist

    rospy.loginfo(wheelPublisher)
    pub.publish(wheelPublisher)
	
	return
	
def publishDist(dist):
	
	return

def publishError(error):
	return


def talker():
	global pub
    rospy.init_node('custom_talker', anonymous=True)
    r = rospy.Rate(10) #10hz
    
    sh = sensorhub.Sensorhub()
    sh.setOutputHandlers(publishPing, publishPong, publishWheels, publishDist, publishError)
    
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

