#!/usr/bin/python

__author__ = 'humsie'
import subprocess           # Import subprocess module
import serial
import RPi.GPIO as GPIO
import time

class Humsie_KAKU:

    @staticmethod
    def getIdentifier():
        return "kaku";

    def __init__(self, server):
        self.server = server;
        self.pin = 14;
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT);
        print "init Kaku"

    def receive(self, message):
        parts = message.split(":")
        on = False
        if (parts[2] == 'on'):
            on = True

        self.sendOldSignal(parts[0], int(parts[1]), on)

    def sendOldSignal(self, address, device, on):

        #Address (string)   : A-P
        #Device  (integer)  : 0-16
        #On      (boolean)  : True|False

        # send signal for kaku receivers not starting with A (address set by 2 codedials)
        self.send(self.encodeMessage(self.makeOldSignal(address, device, on), 375, 1))


    def send(self, message):
        # Send message

        periodusec = message >> 23;

        # seconds to microseconds
        periodusec = periodusec / 1000000.0;

        repeat = 5 << ((message >> 20) & 7)

        # truncate to 20 bit
        message = message & 0xfffff

        # Convert the base3-code to base4-code
        dataBase4 = 0;

        for i in range(0, 12):
            dataBase4 = dataBase4 << 2
            dataBase4 = dataBase4 | (message % 3)
            message = message / 3

        # Send signal "repeat" times
        for loop in range(0, repeat):

            sendData = dataBase4

            for i in range(0, 12):

                signal = sendData & 3

                if signal == 0:
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec * 3.0)
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec * 3.0)

                elif signal == 1:
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec * 3.0)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec)
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec * 3.0)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec)

                elif signal == 2:
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec * 3.0)
                   GPIO.output(self.pin, GPIO.HIGH)
                   time.sleep(periodusec * 3.0)
                   GPIO.output(self.pin, GPIO.LOW)
                   time.sleep(periodusec)

                sendData = sendData >> 2;

            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(periodusec)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(periodusec * 31.0)

            loop = loop + 1

    def encodeMessage(self, trits, periodusec, repeats):

        periodusec = periodusec << 23
        repeats = repeats << 20

        message = long(0)

        # Encode data
        for i in trits:
            #print "i: %i %i \n" % (i, trits[i])
            message = message * 3;
            message = message + i;

        # Encode period duration
        message = message | periodusec;

        # Encode repeats
        message = message | repeats ;

        return message

    def makeOldSignal(self, address, device, on):

        # Set base to 0
        trits = [0,0,0, 0,0,0, 0,0,0, 0,0,0]

        address = ord(address) - 65;

        device = device - 1;

        for i in range(0, 4):
            # bits 0-3 contain address (2^4 = 16 addresses)
            if ( address & 1 ) == 1:
                trits[i] = 2
            address = address >> 1;

        for i in range(4, 8):
            # bits 4-8 contain device (2^4 = 16 addresses)
            if ( device & 1 ) == 1:
               trits[i] = 2
            device = device >> 1

        # bits 8-10 seem to be fixed
        trits[8]=0
        trits[9]=2
        trits[10]=2

        # switch on or off
        if ( on == True ):
            trits[11] = 2

        return trits

    def test(self):

        addresses = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]
        devices = range(1, 17)

        for a in addresses:
            for d in devices:
                result = self.encodeMessage(self.makeOldSignal(a, d, True), 375, 3);

                output,error = subprocess.Popen(
                    [ '/home/humsie/pi-domotica-server/lights/kaku_encode', a, str(d), "on" ],
                    stdout = subprocess.PIPE,
                    stderr= subprocess.PIPE
                ).communicate()

                if str(result) == str(output):
                    test = "pass"
                else:
                    test = "fail"

                print "%s %s On: %s ( %s  %s )" % (a, d, test, result, output);

if __name__ == '__main__':
    print "Testing Humsie_KAKU"
    Humsie_KAKU = Humsie_KAKU("")
    Humsie_KAKU.test()
    Humsie_KAKU.sendOldSignal("A", 6, False);
    Humsie_KAKU.sendOldSignal("A", 6, True);