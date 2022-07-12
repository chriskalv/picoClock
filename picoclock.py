##################################
###########  PICOCLOCK ###########
############## BY CK #############
##################################

# Libraries and global variables for...
# ...Pimoroni pico display
import picodisplay as display
from machine import Pin, I2C
I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21
ALARM_PIN = 3
# ...time
import utime
import binascii
# ...garbage collector
import gc
gc.enable()
# ...colors
white = 165
showseconds = 0
# ...display dimensions
width = display.get_width()
height = display.get_height()
# ...language
language = 0

# Initialize display
display.init(bytearray(width * height * 2))

# Function for checking Button X (brightness adjustment)
def check_for_buttonX():
    global white

    if display.is_pressed(display.BUTTON_X) and white == 125:
        white = 165
    elif display.is_pressed(display.BUTTON_X) and white == 165:
        white = 125
    return white

# Function for checking button A (toggle to show/hide seconds)
def check_for_buttonA():
    global showseconds

    if display.is_pressed(display.BUTTON_A) and showseconds == 0:
        showseconds = 1
    elif display.is_pressed(display.BUTTON_A) and showseconds == 1:
        showseconds = 0
    return showseconds

# Function for checking button Y (switch language)
def check_for_buttonY():
    global language

    if display.is_pressed(display.BUTTON_Y):
        language += 1
        if language >= 4:
            language = 0
    return language

# Function for all things time
class ds3231(object):
    
    # Example for hour zero: 13:45:00 Mon 24 May 2021
    # NowTime = sec \ min \ hour \ week \ day \ month \ year
    NowTime = b'\x00\x45\x13\x02\x24\x05\x21'
    address = 0x68
    start_reg = 0x00
    alarm1_reg = 0x07
    control_reg = 0x0e
    status_reg = 0x0f
    
    # Set locale for weekdays
    if language == 0:
        w  = ["Sonntag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag"]
    elif langauge == 1:
        w = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    elif language == 2:
        w = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"]
    elif language == 3:
        w = ["Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]

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
        #print("%02x.%02x.20%x %02x:%02x:%02x %s" %(t[4],t[5],t[6],t[2],t[1],t[0],self.w[t[3]-1]))
    
    # Form human-readable date
    def read_date(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        d = t[3]&0x07  #week
        e = t[4]&0x3F  #day
        f = t[5]&0x1F  #month
        g = t[6]&0x0F  #year
        current_date = ("%02x.%02x.20%x" %(t[4],t[5],t[6]))
        return current_date
        #print("%02x.%02x.20%x %02x:%02x:%02x %s" %(t[4],t[5],t[6],t[2],t[1],t[0],self.w[t[3]-1]))
    
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
    
    # Form human-readable day of the week (number starts with Sunday)
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
    
    # Form human-readable day of the week
    def day_name(self):
        t = self.bus.readfrom_mem(int(self.address),int(self.start_reg),7)
        # Implement a birthday wish
        if rtc.day() == 11 and rtc.month() == 5:
            dayname = "Happy B-Day"
        else:
            dayname = self.w[t[3]-1]
        return dayname
    
    # REDO THIS!
    # Define indents for the days of the week
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

###############################################################################################
# If the time has to be set again, uncomment the following line for one execution of the script
#rtc.set_time('17:26:00,Dienstag,2022-05-31')
###############################################################################################


while True:
    # Black out the display
    display.set_pen(0,0,0)
    display.clear()
    # Choose a whiteish color and draw the time
    display.set_pen(check_for_buttonX(), check_for_buttonX(), check_for_buttonX())
    # Show either hours:minutes or hours:minutes:seconds
    if check_for_buttonA() == 0:
        display.text(rtc.read_time(), 33,8,240, 8)
    else:
        display.text(rtc.read_time()+":"+str(rtc.sec()), 12,15,240, 6)
    # Choose an orange color and draw the day of the week and the date
    display.set_pen(255, 128, 0)
    display.text(rtc.day_name(), rtc.day_widthvalue(),75,240,3)
    display.text(rtc.read_date(), 31,100,240,4)
    # Update the display and wait one second before executing the script again
    display.update()
    utime.sleep(1)