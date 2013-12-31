pi-domotica-server
==================

Raspberry Pi Domotica Server

README is a work-in-(slow)-progress :D

Todo

* Usage
* Hardware wiring
* protocol
* Tests
* Modules
* Configuration

## Server

### Requirements

* Raspberry Pi computer running Raspbian
	- Python 2.7
	- Wiring Pi

* Python modules: 
	- Serial (python-serial)
	- RPi.GPIO (python-rpi.gpio)
	- SMBus (python-smbus)
	- sudo apt-get install python-serial python-rpi.gpio python-smbus

### Install

@todo: Clone from github	

### Configure

@todo: Look at server/DomoServer.cfg and client/client.cfg.

### Run

	$ python server/DomoServer.py &

This should run a server, on the port configured in DomoServer.cfg

## Client

### Configure

@todo: Look at client/client.cfg.


## Modules

#### Humsie_KAKU
Send KAKU on / off commands to old and new [Klik Aan Klik Uit (KAKU)](http://klikaanklikuit.nl) receivers.

##### Requirements

* RF 434 Mhz transmitter (i use: https://www.iprototype.nl/products/components/communications/rf-transmitter-434mhz)

Message: kaku:[house]:[device]:[state]

Possible values for: 

 - house: **A**,**B**,**C**,**D**,**E**,**F**,**G**,**H**,**I**,**J**,**K**,**L**,**M**,**N**,**O** or **P**
 - device: **1**,**2**,**3**,**4**,**5**,**6**,**7**,**8**,**9**,**10**,**11**,**12**,**13**,**14**,**15** or **16** 
 - state: **on** or **off**


#### Humsie_RGB

##### Requirements

- [Adafruit 16-Channel 12-bit PWM/Servo Driver - I2C interface - PCA9685](http://www.adafruit.com/products/815)
- electronic circuit to upgrade the 5v low-watts PWM to 12V high-watts 


Message: rgb:[channel]:[value](:[value]:[value])

Possible values for: 

- channel: 0 to 15
- value: 0 (off) to 255 (on)


## THNX

Thanx goto to Adafruit for having great products and even better learning system and open source code.