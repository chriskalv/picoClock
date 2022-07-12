
picoClock
========================
Instructions to build a pico-based digital table clock showing the 
  + time
  + date and 
  + day of the week.

The code is entirely micropython-based and pulls time data from the RTC chip - an internet connection is not needed. Assembly of the device is really easy and even solder-free in case you have a pre-soldered Raspberry Pi Pico.
<br></br>
| Finished picoClock   |
| ------------- |
| [![](https://i.imgur.com/uGB1qjq.png?raw=true)](https://i.imgur.com/uGB1qjq.png)   |

## Functionality
+ Button A: Switch language of the displayed day of the week (German, English, Spanish and French).
+ Button B: Toggle blinking animation of the colon(s) in the time display.
+ Button X: Adjust brightness.
+ Button Y: Show/hide seconds in the time display.

## Hardware
+ [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
+ [Pimoroni Pico Display](https://www.waveshare.com/pico-oled-2.23.htm)
+ [Waveshare RTC Module DS3231](https://www.waveshare.com/pico-rtc-ds3231.htm)

## Setup
1. Flash the custom Pimoroni MicroPython build onto the board, which already includes the driver for the display. You can find it [here](https://github.com/pimoroni/pimoroni-pico/releases/latest/).
    - Download the MicroPython UF2 file.
    - Push and hold the BOOTSEL button while you plug your Pico into the USB port of your computer. Once plugged in, release the button.
    - The Pico will mount as a mass storage device called _RPI-RP2_.
    - Drag and drop the MicroPython UF2 file into the _RPI-RP2_ volume.
    
2. Download and install [Thonny](https://thonny.org/), open it, go to _Run_ --> _Select interpreter_ and choose _MicroPython (Raspberry Pi Pico)_. This will establish a shell connection to your device.
3. Copy file main.py
4. Edit global settings
5. Set time

## Case
I did not make a specific case for this build, but [this one](https://www.printables.com/de/model/237722-raspberry-pi-pico-rtc-display-case) from another build uses the same hardware and should fit fairly well.
