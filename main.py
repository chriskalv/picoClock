##################################
###########  PICOCLOCK ###########
############## BY CK #############
##################################

# --------------------------------
# --------Global settings---------
# Birthday Wish:
birthday_wish_enabled = 1
birthday_month = 12
birthday_day = 5
# --------------------------------

# Libraries for...
# ...Pimoroni Pico display
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import Button
# ...Pimoroni Pico led
from pimoroni import RGBLED
# ...Waveshare RTC module / time
from machine import Pin, I2C
import binascii
import time
# ...garbage collector
import gc
gc.enable()

# Set up hardware/global variables
# Pimoroni Pico display
brightness = 0.6
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
width, height = display.get_bounds()
display.set_backlight(brightness)
# Pimoroni Pico led
led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)
# Waveshare RTC module
I2C_PORT = 1
I2C_SDA = 6
I2C_SCL = 7
'''
I2C_PORT = 0   # Another version of the Waveshare RTC module might need this I2C configuration instead
I2C_SDA = 20
I2C_SCL = 21
'''
# Language
language = 0
# Display formatting
showseconds = 0
# Colors
black = display.create_pen(0, 0, 0)
white = display.create_pen(255, 255, 255)
orange = display.create_pen(255, 128, 0)
# Buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Clear the screen once
display.set_pen(black)
display.clear()
display.update()

# Function for checking button B (switch language)
def buttoncheck_b():
    if button_b.read():
        global language
        language += 1
        if language >= 4:
            language = 0
        return language

# Function for checking button A (brightness adjustment down)
def buttoncheck_a():
    if button_a.read():
        global brightness
        brightness -= 0.1
        if brightness <= 0.2:
            brightness = 0.2
        return brightness

# Function for checking Button X (brightness adjustment up)
def buttoncheck_x():
    if button_x.read():
        global brightness
        brightness += 0.1
        if brightness >= 0.8:
            brightness = 0.8
        return brightness

# Function for checking button Y (show/hide seconds)
def buttoncheck_y():
    if button_y.read():
        global showseconds
        showseconds += 1
        if showseconds >= 2:
            showseconds = 0
        return showseconds

# Function for all things time
class ds3231(object):
    
    # NowTime = sec \ min \ hour \ week \ day \ month \ year
    NowTime = b'\x00\x45\x13\x02\x24\x05\x21'
    address = 0x68
    start_reg = 0x00
    alarm1_reg = 0x07
    control_reg = 0x0e
    status_reg = 0x0f

    # Initialize I2C board functionality
    def __init__(self,i2c_port,i2c_scl,i2c_sda):
        self.bus = I2C(i2c_port,scl=Pin(i2c_scl),sda=Pin(i2c_sda))
    
    # Derive time
    def set_time(self,new_time):
        hour = new_time[0] + new_time[1]
        minute = new_time[3] + new_time[4]
        second = new_time[6] + new_time[7]
        week = "0" + str(self.w.index(new_time.split(",",2)[1])+1)
        year = new_time.split(",",2)[2][2] + new_time.split(",",2)[2][3]
        month = new_time.split(",",2)[2][5] + new_time.split(",",2)[2][6]
        day = new_time.split(",",2)[2][8] + new_time.split(",",2)[2][9]
        now_time = binascii.unhexlify((second + " " + minute + " " + hour + " " + week + " " + day + " " + month + " " + year).replace(' ',''))
        self.bus.writeto_mem(int(self.address),int(self.start_reg),now_time)
    
    # Form human-readable time format
    def read_time(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        a = t[0]&0x7F  #second
        b = t[1]&0x7F  #minute
        c = t[2]&0x3F  #hour
        current_time = ("%02x:%02x" %(t[2],t[1]))
        return current_time
        # print("%02x.%02x.20%x %02x:%02x:%02x %s" %(t[4],t[5],t[6],t[2],t[1],t[0],self.w[t[3]-1]))
    
    # Form human-readable date
    def read_date(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        d = t[3]&0x07  #week
        e = t[4]&0x3F  #day
        f = t[5]&0x1F  #month
        g = t[6]&0x0F  #year 
        current_date = ("%02x.%02x.20%x" %(t[4],t[5],t[6]))
        return current_date
        # print("%02x.%02x.20%x %02x:%02x:%02x %s" %(t[4],t[5],t[6],t[2],t[1],t[0],self.w[t[3]-1]))
    
    # Form human-readable year
    def year(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[6]&0x70)/16) * 10
        lo = t[6]&0x0F
        return hi + lo
    
    # Form human-readable second
    def sec(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[0]&0x70)/16) * 10
        lo = t[0]&0x0F
        hilo = hi + lo
        if (hilo) < 10:
            hilo = "0"+str(hilo)
        return hilo
    
    # Form human-readable minute
    def minute(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[1]&0x70)/16) * 10
        lo = t[1]&0x0F
        return hi + lo
    
    # Form human-readable hour
    def hour(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[2]&0x30)/16) * 10
        lo = t[2]&0x0F
        return hi + lo
    
    # Form human-readable day of the week (number)
    def week(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        lo = t[3]&0x07
        return lo
    
    # Form human-readable day
    def day(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[4]&0x30)/16) * 10
        lo = t[4]&0x0F
        
        return hi + lo
    
    # Forme human-readable month
    def month(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        hi = int((t[5]&0x10)/16) * 10
        lo = t[5]&0x0F
        return hi + lo
    
    # Form human-readable day of the week (text)
    def day_name(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        
        # Set locale for weekdays
        if language == 0:
            w  = ["sonntag","montag","dienstag","mittwoch","donnerstag","freitag","samstag"]
        elif language == 1:
            w = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
        elif language == 2:
            w = ["domingo","lunes","martes","miércoles","jueves","viernes","sábado"]
        elif language == 3:
            w = ["dimanche","lundi","mardi","mercredi","jeudi","vendredi","samedi"]
            
        # Implement a birthday wish
        if birthday_wish_enabled == 1 and rtc.day() == birthday_day and rtc.month() == birthday_month:
            dayname = "happy b-day"
        else:
            dayname = w[t[3]-1]
        return dayname
   
    # Define correct indents in order to be able to center weekday text
    def day_widthvalue(self):
        weekday = rtc.day_name()
        if weekday == "Montag" or weekday == "Freitag" or weekday == "Samtag":
            widthvalue = 65
        elif weekday == "Dienstag" or weekday == "Mittwoch":
            widthvalue = 55
        elif weekday == "Sonntag":
            widthvalue = 60
        else:
            widthvalue = 35
        return widthvalue

# RTC functionality
rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)

#########################################################################################
# If the time has to be set again, uncomment the rtc.set_time line below, enter the     #
# current time, execute the script once and comment the line again after that.          #
#                                                                                       #
# rtc.set_time('17:31:30,Mittwoch,2022-07-13')                                          #
#########################################################################################


while True:
    # Check all the buttons!
    buttoncheck_a()
    buttoncheck_b()
    buttoncheck_x()
    buttoncheck_y()
    
    # Set display brightness
    display.set_backlight(brightness)

    # Clear the display
    display.set_pen(black)
    display.clear()
    
    # Give integer variables for time a leading zero
    disphours = "%02d" % (int(rtc.hour()),)
    dispminutes = "%02d" % (int(rtc.minute()),)
    dispseconds = "%02d" % (int(rtc.sec()),)
    
    # Define some counting variables    
    if showseconds == 0:
        disptime = disphours + ":" + dispminutes
        disptime_width = 3   # (two spaces and a colon)
    else:
        disptime = disphours + ":" + dispminutes + ":" + dispseconds
        disptime_width = 6   # (four spaces and two colons)
    date_width = 6    # (four spaces and two periods)
    dispweekday_width = 0
    
    # Count pixel width of pimoroni font numbers and multiply by actual display pixels per pimoroni pixel per font size
    for i in disptime:
        if i == "1":
            disptime_width += 2
        if i == "2" or i == "3" or i == "5":
            disptime_width += 4
        if i == "0" or i == "4" or i == "6" or i == "7" or i == "8" or i == "9":
            disptime_width += 5
    
    for i in rtc.read_date():
        if i == "1":
            date_width += 2
        if i == "2" or i == "3" or i == "5":
            date_width += 4
        if i == "0" or i == "4" or i == "6" or i == "7" or i == "8" or i == "9":
            date_width += 5
            
    # Count pixel width of pimoroni font letters and multiply by actual display pixels per pimoroni font pixel per font size
    for i in rtc.day_name():
        if i == "i" or i == "-":
            dispweekday_width += 3
        if i == "c" or i == "e" or i == "f" or i == "h" or i == "j" or i =="k" or i == "l" or i == "s" or i == "x" or i == "y" or i == "z":
            dispweekday_width += 4
        if i == "a" or i == "b" or i == "d" or i == "g" or i == "m" or i == "n" or i == "o" or i == "p" or i == "q" or i == "r" or i == "t" or i == "u" or i == "v" or i == "w":
            dispweekday_width += 5
            
    # Set starting point on x-achsis of the display to center text for different font sizes
    x_start8 = round((width / 2) - ((disptime_width * 9.1) / 2))
    x_start6 = round((width / 2) - ((disptime_width * 6.7) / 2))
    x_start_date = round((width / 2) - ((date_width * 4.5) / 2))
    x_start_weekday = round((width / 2) - ((dispweekday_width * 3.6) / 2))
    
    # Choose a white color and draw the time
    display.set_pen(white)
    if showseconds == 0:
        display.text(disptime, x_start8, 8, 240, 8)
    else:
        display.text(disptime, x_start6, 15, 240, 6)
        
    # Choose an orange color and draw the day of the week and the date
    display.set_pen(orange)
    display.text(rtc.day_name(), x_start_weekday, 75, 240, 3)
    display.text(rtc.read_date(), x_start_date, 100, 240, 4)
    
    # Update the display and wait one second before executing the script again
    display.update()
    time.sleep(1)
