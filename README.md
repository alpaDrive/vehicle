# vehicle
Software running on Pi, in the vehicle. Written entirely in Python, all the code is in a procedural format, easy for anyone to read and understand.

## Table Of Contents
* [What's this](#whats-this)
    * [Role in the UX](#role-in-the-ux)
    * [Tech Stack](#tech-stack)
* Setup Guide
    * Hardware prerequisites
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
2. **ELM321 Adapter**
    
    This is available all over the internet for direct purchase, at least in India. [Here](https://www.amazon.in/Robostore-India-Bluetooth-Diagnostic-Scanner/dp/B07DJC6KNV) is one from Amazon India. Don't worry if this is unavailable or out of stock. You can get this literally anywhere for cheap, but make sure you don't buy the Bluetooth version. Only the OBD-II USB interface is supported by this software as of now.
