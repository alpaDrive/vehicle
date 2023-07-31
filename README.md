<img src="https://github.com/alpaDrive/vehicle/assets/50231856/37f2801a-b467-4d9b-93d3-deda828b457e" alt="alpaDrive Logo" width="250" align="right" >

# `vehicle` 🚗
> Software running on Pi, in the vehicle. Written entirely in Python, all the code is in a procedural format, easy for anyone to read and understand. But beware, you might mess up your car if you change it... Just kidding, welcome aboard & happy hacking! 🎉

## Table Of Contents
* [What's this](#whats-this)
    * [Role in the UX](#role-in-the-ux)
    * [Tech Stack](#tech-stack)
* [Setup Guide](#setup-guide)
    * [Hardware prerequisites](#hardware-prerequisites)
    * [Connection & Circuits](#connection--circuits)
    * [Installation Instructions](#installation-instructions)

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

6. **Some networking equipment**
    The Raspberry Pi has to always be connected to a network. We advise you get some hardware that can achieve this. The hardware has to plug in to the RPi, and provide a consistent network connection, even while the car is moving. The best solution is to get some sort of USB SIM card adapter, get a SIM card, purchase a carrier plan & leave it plugged into the RPi.

7. **A power source**
    Looking for a photo here as well? If you don't even know that a power source refers to a phone charger or powerbank, we'd advise you to stop right here because we're sure this isn't your thing 😆 Sorry for that demotivation, let's continue...

### Connection & Circuits
Refer to the circuit diagram to make connections. If you need further clarification for the Raspberry Pi's pin layout, refer [pinout](https://pinout.xyz).

<img src="https://github.com/alpaDrive/vehicle/assets/50231856/ff701fab-205d-4973-8deb-bb7dfc7d3584" alt="Circuit Diagram" width="800" align="center" >

| GPS Module  | Raspberry Pi |
| ------------- | ------------- |
| VCC  | PIN 4 (5V)  |
| RX  | PIN 8 (UART TX)  |
| TX  | PIN 10 (UART RX) |
| GND | PIN 6 (GND) |

If you're using the pushbutton, here are the connections
  
| Pushbutton  | Raspberry Pi |
| ----------- | ------------ |
|    PIN 1    |    PIN 40    |
|    PIN 2    |    PIN 39    |

Connect the Pi to a power source after flashing an OS into the SD card
### Installation Instructions
If you've got this far, then this might just be a walk in the park. Just follow these instructions step by step to set up your device.

#### Setting up the software
The first thing that you have to do is to set up and test run the software to see whether it's working or not. Make sure your Raspberry Pi is connected to the network.

1. Enable serial in the Raspberry Pi by running `sudo raspi-config` on a terminal and enabling the serial interface from the menu

2. Clone this repository into the Pi and change the working directory

    ```bash
    $ git clone https://github.com/alpaDrive/vehicle.git
    $ cd vehicle/
    ```
3. Install all the required modules

    ```bash
    $ sudo pip3 install -r requirements.txt # make sure to run it as root
    ```
    
    Now, test whether all the imports are working fine.

    ```bash
    $ sudo __tests__/check.py # again run as root
    ```

4. Run the script as root from the command line itself after connecting the OBD adapter to a car.

    ```bash
    $ sudo python3 main.py
    ```

5. Once this is run, you will get a QR code on your terminal. Scan it from the app after signing up to pair this vehicle to your user account. Make sure you do this once and scan the QR before proceeding to enable auto start on boot. This is because if you accidentally enable auto start on boot, then you'll have to repeat the steps all over again.

If it works, voila! You've set up your Raspberry Pi and are ready to go. If it doesn't, make sure it's an issue with the code before opening an issue but don't feel hesitant to do so. We welcome any issues about the software and will respond immediately.

Before you jump to that, try to debug by using the scripts available in the `__tests__/` directory as well. Also, in order for the script to run smoothly, the OBD adapter must be connected before starting the script.

#### Enabling auto start on boot
In a nutshell, you're going to create a systemd service for this software and run it on boot. One factor to consider here is that the Raspberry Pi should be on some network all the time. The easiest way to do this is to get some USB SIM card adapter & leave it plugged in. Here is what you have to do once you have a consistent networking solution:

1. Copy over the service unit file from this repository to the `/etc/systemd/system/` directory, the execution script to `/usr/bin/` directory & grant permissions to the script.

    ```bash
    $ sudo cp alpadrive.service /etc/systemd/system/alpadrive.service
    $ sudo cp alpadrive.sh /usr/bin/alpadrive.sh && sudo chmod +x /usr/bin/alpadrive.sh
    ```

2. Reload the systemd daemon for changes to take effect

    ```bash
    $ sudo systemctl daemon-reload
    ```

3. Enable the service to run at boot

    ```bash
    $ sudo systemctl enable alpadrive.service
    ```

4. Start the service and check whether it runs without crashing. This should print an `active(running)` status onto the console.

    ```bash
    $ sudo systemctl start alpadrive.service
    $ sudo systemctl status alpadrive.service
    ```

5. Once this is done, you're almost ready to go! Connect the OBD adapter to the car and reboot the Pi...

    ```
    $ sudo reboot
    ```

6. Once it boots up, log back in again and check the status of the service

    ```bash
    $ sudo systemctl status alpadrive.service
    ```

    If it's running successfully, then congrats! You can now open your mobile app, pair using the QR code and view the status of your car! You can now disonnect SSH/display & leave the device in your car. Just make sure the power source is stable & doesn't go out. As long as the device stays powered, all features will be available to you. Happy alpaDriving!
