# vehicle
Software running on Pi, in the vehicle. Written entirely in Python, all the code is in a procedural format, easy for anyone to read and understand.

## Table Of Contents
* [What's this](#whats-this)
    * [Role in the UX](#role-in-the-ux)
    * [Tech Stack](#tech-stack)
* Setup Guide
    * Hardware prerequisites
    * Circuit & Connections
    * Installation Instructions

## What's this?
alpaDrive requires some kind of computing platform running in the vehicle to be able to connect with it and monitor it. This platform should ideally work across multiple vehicles as well.
### Role in the UX
This device aims to provide a plug and play experience for end users to join the alpaDrive family. It would just plug into your existing car's OBD-II port, hook up to the internet, and seamlessly pair with the [app](https://github.com/alpaDrive/app) to make the car connected, just like that!
### Tech Stack
The device is essentially based off of a Raspberry Pi, with a NEO-6M GPS module. You can see more about the hardware in the [Hardware Prerequisites]() section. The software running on the Pi is written entirely in Python, and is a wrapper for the [python-OBD](https://github.com/brendan-w/python-OBD) library, with [systemd](https://systemd.io/) to manage the process.

## Setup Guide
This setup guide assumes you have the necessary hardware components ready to go. The software may not work correctly if you have some hardware setup the wrong way.
### Hardware Prerequisites
Obtain all the following components, test them out individually and confirm they're working
1. **Raspberry Pi 3 or 4**
   
   ![rpi](https://github.com/alpaDrive/vehicle/assets/50231856/33df13dc-abde-41a1-8e51-f8197699f0af)
   
   You can get one [here](https://www.raspberrypi.com/products/) on the official Raspberry Foundation shop
2. **ELM327 Adapter**

    ![obd](https://github.com/alpaDrive/vehicle/assets/50231856/314d843f-6952-4693-b8e8-f36e88fb49db)

    This is available all over the internet for direct purchase, at least in India. [Here](https://www.amazon.in/Robostore-India-Bluetooth-Diagnostic-Scanner/dp/B07DJC6KNV) is one from Amazon India. Don't worry if this is unavailable or out of stock. You can get this literally anywhere for cheap, but make sure you don't buy the Bluetooth version. Only the OBD-II USB interface is supported by this software as of now.

3. **NEO-6M GPS Module** (with Berg connector)
    
    ![gps](https://github.com/alpaDrive/vehicle/assets/50231856/16b74781-cb59-472c-b65c-334c14c1d2ba)     ![berg](https://github.com/alpaDrive/vehicle/assets/50231856/0d85e19c-14b1-45dd-bc9b-297b35e90712)
    
    This GPS module is just like the adapter, and can be found in plenty of online stores. [Here](https://robu.in/product/ublox-neo-6m-gps-module/) is a link to an online listing. The Berg connector, although optional, is highly reccommended. This might not come as a surprise if you're an electronics or hardware pro, but for total noobs or even most software guys, this is something to keep in mind. Once they both arrive, you gotta get the connector soldered on to the pins of the module. If you're a beginner, you might be tempted to immediately grab some male to female jumpers and solder them onto the board. Don't do it, you'll risk damaging the module itself and even if you manage to solder it on, the data transfer might not be proper at all. If you're unfamiliar to soldering, go to some soldering professional and get it done.

4. **Push Button** (optional)
    
    ![button](https://github.com/alpaDrive/vehicle/assets/50231856/9418cc7c-6b16-49dc-b687-7fc8ca402dcf)

    This is an optional accessory to enable quick shutdown of the device and serves no other meaningful purpose. You can get one [here](https://www.electronicscomp.com/push-button-spst-on-off-switch) or simply use any similar switch. Don't let the image fool you. If you don't plan on getting it, make sure you log into the Pi via SSH and run `sudo shutdown` before disconnecting the power each time.

5. **Jumper Wires**
    
    ![jumpers](https://github.com/alpaDrive/vehicle/assets/50231856/a3fae4f2-348c-481e-af24-e830d425b14c)

    You can get them in pretty much any electronics store you want these days. If you do want an online link, just click [here](https://robu.in/product/20cm-dupont-wire-color-jumper-cable-2-54mm-1p-1p-female-female-40pcs). Get some male to female & female to female ones, as you'll need them for the push button and GPS module.

6. **A power source**
    Looking for a photo here as well? If you don't even know that a power source refers to a phone charger or powerbank, we'd advise you to stop right here because we're sure this isn't your thing 😆 Sorry for that demotivation, let's continue...

### Connection & Circuits
A proper circuit diagram is in the works and will be uploaded soon. Meanwhile, you can use these instructions to connect.
* Connect the ELM327 adapter to one of the USB ports on the Pi
* Take 4 jumper wires, and make the following connections from the GPS module to the Pi. If you're stuck with the pin numbering scheme on the Pi, just go to [pinout](https://pinout.xyz).
    
    | GPS Module  | Raspberry Pi |
    | ------------- | ------------- |
    | VCC  | PIN 4 (5V)  |
    | RX  | PIN 8 (UART TX)  |
    | TX  | PIN 10 (UART RX) |
    | GND | PIN 6 (GND) |
 * If you're using the pushbutton, take 2 jumpers, and make the following connections
  
    | Pushbutton  | Raspberry Pi |
    | ----------- | ------------ |
    |    PIN 1    |    PIN 40    |
    |    PIN 2    |    PIN 39    |
 * Connect the Pi to a power source after flashing an OS into the SD card
### Installation Instructions
If you've got this far, then this might just be a walk in the park. Just follow these instructions step by step to set up your device.
