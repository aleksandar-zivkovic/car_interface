#!/usr/bin/python
import sys
import time
from Adafruit_PWM_Servo_Driver import PWM

class servo_control:
    def __init__(self, freq=50):
        self._pwm = PWM(0x40, debug=False)    # I2C address 
        self.freq = freq
        self._pwm.setPWMFreq(self.freq)
        self.pulse_len = 1500
        return

    def set_pulse_len(self, pulse_len):
        """pulse_len is between 1000us and 2000us"""
        self.pulse_len = pulse_len
        self.calcPWM()
        return

    def set_freq(self, freq):
        """frequency between 40 and 200Hz"""
        self.freq = freq
        self._pwm.setPWMFreq(self.freq)
        self.calcPWM()
        return

    def calcPWM(self):
        unit_cycle_time = (1.0/self.freq) / 4096  # duration of one count, assuming 12bit (4096) intervals
        self.pwm_count = int(self.pulse_len / 1000000.0 / unit_cycle_time)
        self._pwm.setPWM(1, 0, self.pwm_count)
        print("pulse:{:10} freq:{:10} count:{:10} unit:{:20.9f}".format(self.pulse_len, self.freq, self.pwm_count, unit_cycle_time))
        return 

def main():
    servo = servo_control()
    time.sleep(0.5)
    #for pos in range(1000,2000):
    pos = 1520
    servo.set_pulse_len(pos)
    for f in range(50,600,10):
        servo.set_freq(f)
        time.sleep(0.5)
    servo.set_freq(400)
    while True:
        for pos in range(1000,2000,10):
            servo.set_pulse_len(pos)
            time.sleep(0.1)
        for pos in range(2000,1000,-10):
            servo.set_pulse_len(pos)
            time.sleep(0.1)
    return

if __name__ == '__main__':
    main()
