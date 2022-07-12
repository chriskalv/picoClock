
picoClock
========================
Instructions to build a pico-based digital clock showing the 
  + time, 
  + date and 
  + day of the week.

The code is entirely micropython-based. The build is not only easy, but also solder-free in case you have a pre-soldered Raspberry Pi Pico.
<br></br>
| Finished clock (front)   | Finished clock (back)   |
| ------------- | -------------|
| [![](https://i.imgur.com/J0NngF4.png?raw=true)](https://i.imgur.com/J0NngF4.png.jpg)   |   [![](https://i.imgur.com/hw6ClAO.png?raw=true)](https://i.imgur.com/hw6ClAO.png)   |

## Hardware
+ [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
+ [Pimoroni Pico Display](https://www.waveshare.com/pico-oled-2.23.htm)
+ [Waveshare RTC Module DS3231](https://www.waveshare.com/pico-rtc-ds3231.htm)


## Setup
1. Flash the custom Pimoroni MicroPython build onto the board, which already includes the driver for the display. You can find it [here](https://github.com/pimoroni/pimoroni-pico/releases/latest/).
    - Download the MicroPython UF2 file.
    - Push and hold the BOOTSEL button and plug your Pico into the USB port of your computer. Release the BOOTSEL button after your Pico is connected.
    - The Pico will mount as a Mass Storage Device called RPI-RP2.
    - Drag and drop the MicroPython UF2 file into the RPI-RP2 volume.
    
2. Download [Thonny](https://thonny.org/), install and open it, go to _Run_ --> _Select interpreter_ and choose _MicroPython (Raspberry Pi Pico)_. This will establish a shell connection to your device.
3. Copy file main.py
4. Edit global settings
5. Set time

## Case
I did not make a specific case for this build, but [this one](https://www.printables.com/de/model/237722-raspberry-pi-pico-rtc-display-case) from another build uses the same hardware and should fit fairly well.
