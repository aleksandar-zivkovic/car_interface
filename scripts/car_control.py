#!/usr/bin/python

import sys
import time

#sys.path.append('Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
from Adafruit_PWM_Servo_Driver import PWM

servoMin = 220  # Min pulse length out of 4096
servoMax = 520  # Max pulse length out of 4096

steerLeft = 208
steerCenter = 312
steerRight = 417
currentSteeringAngle = steerCenter
STEERING_ANGLE_STEP = 5
gas_pedal = 0

STEERING_PWM_CHANNEL = 0
MOTOR_PWM_CHANNEL = 15
MOTOR_STOP_PWM_VALUE = 307
MOTOR_MIN_PWM_VALUE = 290
MOTOR_DEADBAND_START_VALUE = 299
MOTOR_DEADBAND_STOP_VALUE = 323
MOTOR_MAX_PWM_VALUE = 340


MOTOR_MAX_THROTTLE_PERCENTAGE = 50
MOTOR_MAX_REVERSE_PERCENTAGE = -50
MOTOR_STEP_SIZE_PERCENT = 5
MOTOR_BREAKING_FORCE = 5
MOTOR_BREAKING_DELAY = 0.3


class CarControl(object):
  def __init__(self):
    self._pwm = PWM(0x40)
    self._pwm.setPWMFreq(50)
    self.stop()
    self.reset_steering()
    self.throttle = 0

  def more_gas(self):
    global gas_pedal
    if gas_pedal <= MOTOR_MAX_THROTTLE_PERCENTAGE:
       gas_pedal += MOTOR_STEP_SIZE_PERCENT
    else:
       gas_pedal = MOTOR_MAX_THROTTLE_PERCENTAGE
    self.throttle = gas_pedal

  def reverse(self):
    global gas_pedal
    if gas_pedal >= MOTOR_MAX_REVERSE_PERCENTAGE:
       gas_pedal -= MOTOR_STEP_SIZE_PERCENT
    else:
       gas_pedal = MOTOR_MAX_REVERSE_PERCENTAGE
    self.throttle = gas_pedal


  def active_breaking(self):
    global gas_pedal
    # ACTIVE BREAK OPPOSITE DIRECTION
    if gas_pedal > 0:
       self.throttle = -MOTOR_BREAKING_FORCE
    elif gas_pedal < 0:
       self.throttle = MOTOR_BREAKING_FORCE
    time.sleep(MOTOR_BREAKING_DELAY)
    self.throttle = 0
    gas_pedal = 0

  def sensor_breaking(self):
    global gas_pedal
    # ACTIVE BREAK OPPOSITE DIRECTION
    self.throttle = -MOTOR_BREAKING_FORCE
    time.sleep(MOTOR_BREAKING_DELAY)
    self.throttle = 0
    gas_pedal = 0

  def _get_motor_pwm_value(self):
    if self.throttle == 0:
      return MOTOR_STOP_PWM_VALUE
    elif self.throttle < 0:
      coeff = -self.throttle / 100.0
      min_value = MOTOR_DEADBAND_START_VALUE
      max_value = MOTOR_MIN_PWM_VALUE
    else:
      coeff = self.throttle / 100.0
      min_value = MOTOR_DEADBAND_STOP_VALUE
      max_value = MOTOR_MAX_PWM_VALUE
    assert 0.0 <= coeff <= 1.0
    diff = max_value - min_value
    # Interpolate between the min and max values
    return int(round(min_value + coeff * diff, 0))

  @property
  def throttle(self):
    return self._throttle

  @throttle.setter
  def throttle(self, value):
    assert -100 <= value <= 100
    self._throttle = value
    pwm_value = self._get_motor_pwm_value()
    print('Setting motor PWM to', pwm_value)
    self._pwm.setPWM(MOTOR_PWM_CHANNEL, 0, pwm_value)

  def stop(self):
    global currentSteeringAngle
    self.throttle = 0
    currentSteeringAngle = steerCenter

  def stop_and_reset(self):
    self.throttle = 0
    self.active_breaking()
    self.stop()
    self.reset_steering()

  def reset_steering(self):
    global currentSteeringAngle
    self._pwm.setPWM(STEERING_PWM_CHANNEL, 0, steerCenter)
    currentSteeringAngle = steerCenter

  def steer_right(self):
    global currentSteeringAngle
    if currentSteeringAngle <= (steerRight-STEERING_ANGLE_STEP):
        currentSteeringAngle += STEERING_ANGLE_STEP
    else:
        currentSteeringAngle = steerRight
    self._pwm.setPWM(STEERING_PWM_CHANNEL, 0, currentSteeringAngle)

  def steer_left(self):
    global currentSteeringAngle
    if currentSteeringAngle >= (steerLeft+STEERING_ANGLE_STEP):
        currentSteeringAngle -= STEERING_ANGLE_STEP
    else:
        currentSteeringAngle = steerLeft
    self._pwm.setPWM(STEERING_PWM_CHANNEL, 0, currentSteeringAngle)



cc = CarControl()

for throttle, seconds in zip(sys.argv[1::2], sys.argv[2::2]):
  cc.throttle = int(throttle)
  seconds = float(seconds)
  print('Sleeping for', seconds)
  time.sleep(seconds)
cc.stop()
#cc.throttle = -100
# def setServoPulse(channel, pulse):
#   pulseLength = 1000000                   # 1,000,000 us per second
#   pulseLength /= 60                       # 60 Hz
#   print "%d us per period" % pulseLength
#   pulseLength /= 4096                     # 12 bits of resolution
#   print "%d us per bit" % pulseLength
#   pulse *= 1000
#   pulse /= pulseLength
#   pwm.setPWM(channel, 0, pulse)


# pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
# pwm.setPWM(15, 0, 310)
# for value in range(330, 350):
#   print(value)
#   pwm.setPWM(15, 0, value)
#   time.sleep(.2)
# for value in range(300, 250, -1):
#   print(value)
#   pwm.setPWM(15, 0, value)
#   time.sleep(.2)
# pwm.setPWM(15, 0, 323) # = 192
# time.sleep(5)
# pwm.setPWM(15, 0, 310)
# time.sleep(1)
# pwm.setPWM(15, 0, 0)
