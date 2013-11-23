#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import getopt

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)

def level(value, min, max):
    steps = 255;
    delta = float(max - min)
    value = int(value)

    if value > steps:
        value = steps;
    if value < 0:
        value = 0;
    return int(min + ((delta / 255) * value));

def main(argv):

    minValue = 0  # Min pulse length out of 4096
    maxValue = 4095  # Max pulse length out of 4096
    frequency = 1200 # Frequency
    

    color = [0,0,0, 0,0,0, 0,0,0];
    
    try:
      opts, args = getopt.getopt(argv,"hr:g:b:f:a:b:c:",["red=","green=","blue=", "frequency="])
    except getopt.GetoptError:
      print 'setrgb.py -r <red> -g <green> -b <blue>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'setrgb.py -r <red> -g <green> -b <blue>'
         sys.exit()

      elif opt in ("-f", "--frequency"):
           frequency = int(arg);

      elif opt in ("-a", "--channela"):
	   color[0] = level(int(arg[:2], 16), minValue, maxValue)
	   color[2] = level(int(arg[2:4], 16), minValue, maxValue)
	   color[1] = level(int(arg[4:6], 16), minValue, maxValue)

      elif opt in ("-b", "--channelb"):
	   color[3] = level(int(arg[:2], 16), minValue, maxValue)
	   color[5] = level(int(arg[2:4], 16), minValue, maxValue)
	   color[4] = level(int(arg[4:6], 16), minValue, maxValue)

      elif opt in ("-c", "--channelc"):
	   color[6] = level(int(arg[:2], 16), minValue, maxValue)
	   color[8] = level(int(arg[2:4], 16), minValue, maxValue)
	   color[7] = level(int(arg[4:6], 16), minValue, maxValue)

      elif opt in ("-r", "--red"):
           color[0] = level(arg, minValue, maxValue)
           color[3] = level(arg, minValue, maxValue)
           color[6] = level(arg, minValue, maxValue)

      elif opt in ("-g", "--green"):
           color[2] = level(arg, minValue, maxValue)
           color[5] = level(arg, minValue, maxValue)
           color[8] = level(arg, minValue, maxValue)

      elif opt in ("-b", "--blue"):
           color[1] = level(arg, minValue, maxValue)
           color[4] = level(arg, minValue, maxValue)
           color[7] = level(arg, minValue, maxValue)

    pwm = PWM(0x41, debug=False)
    pwm.setPWMFreq(frequency)                        # Set frequency to 1000 Hz  

    i = 0;
    while i < 9:
	print "Setting channel %i to value %i" % (i, color[i]); 
	pwm.setPWM(i, 0, color[i])
	i = i + 1;

if __name__ == "__main__":
   main(sys.argv[1:])
