#! /usr/bin/env python
from __future__ import print_function
import rospy
import tty, sys
import termios

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the motor action, including the goal message
import car_interface.msg

def motor_action_client():
    # Creates the SimpleActionClient, passing the type of the action (MotorAction) to the constructor.
    client = actionlib.SimpleActionClient('motor_action', car_interface.msg.MotorAction)

    # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

def getin():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
       tty.setraw(sys.stdin.fileno())
       ch = sys.stdin.read(1)
    finally:
       termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main_loop():
#    print "Enter your command (i=forward, o=steer right, u=steer left, k=reverse, r=reset steering, 0=Stop!):"
#    print "Enter 'q' to quit!"

    print(',---------------------------------------------')
    print('| Enter command:                              |')
    print('| i = throttle forward / k = throttle reverse |')
    print('| u = steer left / o = steer right            |')
    print('| b = break                                   |' )
    print('| r / l / j = center steering                 |')
    print('| any other key = kill switch, STOP!          |')
    print('| q = STOP and quit script                    |')
    print(' ---------------------------------------------')

    while True: 
      ch = getin()
      if ch == 'i' or ch == 'I':
        goal = car_interface.msg.MotorAction(direction=1)
        client.send_goal(goal)
      elif ch == 'k' or ch == 'K':
        goal = car_interface.msg.FibonacciAction(direction=0)
        client.send_goal(goal)

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS.
        rospy.init_node('motor_action_client_py')
        main_loop()
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)
