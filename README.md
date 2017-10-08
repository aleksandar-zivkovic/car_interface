# Teensy Sensor Hub #
This is a ROS node to interface with the Teensy sensor hub.

## Configuration parmeters

The node need to know the tty for the serial port, where the Teensy is conected.
Also needed is the communcations speed. The default is 115200b/s.

## ROS Topics
This code define 4 ROS topics

### Topic "teensy_pong"
This topic defines two timestamps. It is sent to Teensy with RPi time set in
`timestamp1`, and `timestamp2` set to zero.

The Teensy will return the message and set timestamp2 to it's local time, when responding.
When RPi received the response the difference between timestamp1 and time of reception,
indicates the round-trip delay.

Half of this can be used as an estimate of the latency from Teensy to RPi.
The timestamp2 value can be used to establish a mapping between Teensy time ( `millis()` ) and the time on RPi (ROS) side.

```
# ping sender fill in this (pong sender copies)
uint32 timestamp1
# ping sets to 0 (pong sender fill this)
uint32 timestamp2
```

### Topic "teensy_wheel"

Data for wheel motion is sent for both left and right wheel.

```
# Two records, one for left and one for right wheel
OneWheel left
OneWheel right
```
Each wheel has the following data defined.

```
# Pulses per second (lowest possible speed is 20 seconds for one wheel revolution)
uint16 speed
# Enumeration rotDirection is used
uint8 direction
# Timestamp for measurement
uint32 when
# Odometer when direction changed
uint32 dist
# Absolute distance travelled
uint32 dist_abs
```

### Topic "teensy_distance"


### Topic "teensy_error"

## Control
Currently the node accepts simple keypresses (from the relevant terminal) as a way to send controls to the Teensy software.

# Installation
Move to `./catkin_ws/src` and extract the repository there

This should end up with a path like `~/catkin_ws/src/teensy_sensor_hub`

Sunday, 08. October 2017 10:29AM

