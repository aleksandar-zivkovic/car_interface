#!/usr/bin/env python
import rospy
from car_control import CarControl
from car_interface.msg import Movement
from car_interface.msg import Distance

MOVEMENT_TOPIC_NAME = 'movement_talker'
DISTANCE_TOPIC_NAME = 'teensy_distance'

cc = CarControl()

def movement_callback(movement_msg):
	global block_forward_movement
	global block_reverse_movement
	rospy.loginfo("Movement command received: %s" % (movement_msg.command))
	if movement_msg.command == 'forward':
    	# forward
		if block_forward_movement == False:
			cc.more_gas()
			rospy.loginfo("Foward block set to: %s" % (block_forward_movement))
		else:
			rospy.loginfo("Cannot move forward. Foward block set to: %s" % (block_forward_movement))
	elif movement_msg.command == 'reverse':
        # reverse
		if block_reverse_movement == False:
			cc.reverse()
			rospy.loginfo("Reverse block set to: %s" % (block_reverse_movement))
		else:
			rospy.loginfo("Cannot move reverse. Reverse block set to: %s" % (block_reverse_movement))
	elif movement_msg.command == 'left':
		# turn left
		cc.steer_left()
	elif movement_msg.command == 'right':
        # turn right
		cc.steer_right()
	elif movement_msg.command == 'brake':
        # active braking
		cc.active_braking()
	elif movement_msg.command == 'reset':
        # reset steering
		cc.reset_steering()
	else:
        # stop and reset
		cc.stop_and_reset()
        
def distance_callback(distance_msg):
	global block_forward_movement
	global block_reverse_movement
	
	#if distance_msg.distance < 100:
	#	rospy.loginfo("Sensor number %d: Distance: %s" % (distance_msg.sensor, distance_msg.distance))
	
	rospy.loginfo("Distance message received from sensor number %d. Distance: %s" % (distance_msg.sensor, distance_msg.distance))
	if distance_msg.sensor == 0 or distance_msg.sensor == 1 or distance_msg.sensor == 2:
		if distance_msg.distance < 100:
			# front sensors detected an obsticle
			cc.active_braking()
			block_forward_movement = True
			rospy.loginfo("Obsticle detected infront of the car. Braking and turning ON forward block!")
			rospy.sleep(3.)
		else:
			block_forward_movement = False
			rospy.loginfo("No obsticles detected infront of the car. Turning OFF forward block!")
	elif distance_msg.sensor == 3 or distance_msg.sensor == 4 or distance_msg.sensor == 5:
		if distance_msg.distance < 100:
			# reverse sensors detected an obsticle
			cc.active_braking()
			block_reverse_movement = True
			rospy.loginfo("Obsticle detected behind the car. Braking and turning ON reverse block!")
			rospy.sleep(3.)
		else:
			block_reverse_movement = False
			rospy.loginfo("No obsticles detected behind the car. Turning OFF reverse block!")
            
def movement_listener():
	global block_forward_movement
	global block_reverse_movement
	
	block_forward_movement = False
	block_reverse_movement = False
	
	rospy.init_node('movement_listener_node', anonymous=True)
	rospy.Subscriber(MOVEMENT_TOPIC_NAME, Movement, movement_callback)
	rospy.Subscriber(DISTANCE_TOPIC_NAME, Distance, distance_callback)

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
	try:
		movement_listener()
	except rospy.ROSInterruptException:
		pass

