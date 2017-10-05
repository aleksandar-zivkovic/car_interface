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

publishWheels   = rospy.Publisher('custom_chatter', Wheels)
publishDistance = rospy.Publisher('custom_chatter', Distance)


def publishPing(ping):
    return

def publishPong(ping):
    return

def publishWheels(left, right):
    global pubWheels
    wheelsMsg = Wheels()

    wheelsMsg.left.when       = left.when
    wheelsMsg.right.when      = right.when
    wheelsMsg.left.speed      = left.speed
    wheelsMsg.right.speed     = right.speed
    wheelsMsg.left.direction  = left.direction
    wheelsMsg.right.direction = right.direction
    wheelsMsg.left.dist       = left.turn
    wheelsMsg.right.dist      = right.turn
    wheelsMsg.left.dist_abs   = right_dist # convert to meters
    wheelsMsg.right.dist_abs  = right.dist

    rospy.loginfo(wheelsMsg)
    pubWheels.publish(wheelsMsg)

    return

def publishDist(dist):
    global publishDistance
    distanceMsg = Distance()
    distanceMsg.sensor = dist.sensor
    distanceMsg.distance = dist.distance # convert from us to m
    distanceMsg.when = dist.when  # adjust time to RPi time
    return

def publishError(error):
    return


def talker():
    rospy.init_node('custom_talker', anonymous=True)
    r = rospy.Rate(10) #10hz

    sh = sensorhub.Sensorhub()
    sh.setOutputHandlers(publishPing, publishPong, publishWheels, publishDist, publishError)

    msg = Wheels()
    msg.left.speed = 17
    msg.left.direction = 0
    msg.left.dist = 0

    while not rospy.is_shutdown():
        if sh.txDataAvailable():
            txList = [ser]
        else:
            txList = []
        r, w, e = select.select([sys.stdin, ser], txList, [], 0.010)

        # data coming from keyboard?
        if sys.stdin in r:
            if not handleKeyPress(sh, sys.stdin.read(1)):
                break  # bail out

        # data coming from serial?
        if ser in r:
            data_str = ser.read(ser.inWaiting())
            for b in data_str:
                sh.rxRawByte(b)

        # Any data to transmit over serial?
        if ser in w:
            flagAndByte = sh.txGetByte()
            if flagAndByte[0]:
                ser.write(chr(flagAndByte[1]))
    return

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
