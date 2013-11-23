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
    frequency = 40 # Frequency
    interval = 0.1
    

    color = [
		[0.5,0,0, 0,0,1, 0,0,1],
		[1,0,0, 1,0,0, 0,0,1],
		[1,0,0, 1,0,0, 1,0,0],
		[0,1,0, 1,0,0, 1,0,0],
		[0,1,0, 0,1,0, 1,0,0],
		[0,1,0, 0,1,0, 0,1,0],
		[0,0,1, 0,1,0, 0,1,0],
		[0,0,1, 0,0,1, 0,1,0],
		[0,0,1, 0,0,1, 0,0,1]
	    ]

    color2 = [
                [1.00,1.00,1.00, 0.25,0.25,0.25, 0.25,0.25,0.25],
                [0.25,0.25,0.25, 1.00,1.00,1.00, 0.25,0.25,0.25],
                [0.25,0.25,0.25, 0.25,0.25,0.25, 1.00,1.00,1.00],
                [0.25,0.25,0.25, 1.00,1.00,1.00, 0.25,0.25,0.25]
            ]
        

    try:
      opts, args = getopt.getopt(argv,"hr:g:b:f:i:",["red=","green=","blue=", "frequency=", "interval="])
    except getopt.GetoptError:
      print 'setrgb.py -r <red> -g <green> -b <blue>'
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print 'setrgb.py -r <red> -g <green> -b <blue>'
         sys.exit()
      elif opt in ("-f", "--frequency"):
           frequency = int(arg);
      elif opt in ("-i", "--interval"):
	   interval = float(arg)
      elif opt in ("-r", "--red"):
           color[0] = level(arg, minValue, maxValue)
      elif opt in ("-g", "--green"):
           color[2] = level(arg, minValue, maxValue)
      elif opt in ("-b", "--blue"):
           color[1] = level(arg, minValue, maxValue)

    pwm = PWM(0x41, debug=False)
    pwm.setPWMFreq(frequency)                        # Set frequency to 1000 Hz  

    y = -1
    while interval > 0:
        i = 0
        y = y + 1
	
	if y > (len(color)-1):
	    y = 0

        while i < 9:
            pwm.setPWM(i, 0, int(color[y][i] * 4095))
	    i = i + 1
	
	time.sleep(interval)

if __name__ == "__main__":
   main(sys.argv[1:])
