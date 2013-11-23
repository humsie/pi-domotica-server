__author__ = 'humsie'

from Adafruit.Adafruit_PWM import Adafruit_PWM

class Humsie_RGB:

    minValue = 0  # Min pulse length out of 4096
    maxValue = 4095  # Max pulse length out of 4096
    frequency = 1200 # Set frequency between 40 and 1600 Hz


    @staticmethod
    def getIdentifier():
        return "rgb"

    def __init__(self, server):

        self.rgbchannels = server.config.get('Humsie_RGB', 'channels')
        self.pwm = Adafruit_PWM(int(server.config.get('Humsie_RGB', 'address'), 16), debug=False)
        self.pwm.setPWMFreq(Humsie_RGB.frequency)

        mapping = server.config.get('Humsie_RGB', 'channelmapping')

        print mapping[0]

        self.server = server
        print "init RGB"

    def receive(self, message):
        print "message_received: %s" % (message)
        parts = message.split(":")

        offset = int(parts[0])
        end = len(parts) -1

        i = 0
        while i < end:
            self.pwm.setPWM(i+offset, 0, self.hex2level(float(parts[i+1])))
            i = i + 1

    def hex2level(self, value):
        steps = 255
        delta = float(Humsie_RGB.maxValue - Humsie_RGB.minValue)
        value = int(value)

        if value > steps:
            value = steps
        if value < 0:
            value = 0
        return int(Humsie_RGB.minValue + ((delta / 255) * value))