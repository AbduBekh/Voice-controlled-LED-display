import spidev
import time
from globals import stop_flag


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000
spi.mode = 0

RED_DATA = 0
BLUE_DATA = 1
GREEN_DATA = 2

heart = [
    0x00, 0x66, 0xFF, 0xFF,
    0xFF, 0x7E, 0x3C, 0x18
]
data = [0x00, 0x00, 0x00, 0x00]

def display_heart_red(heart):
    x = 0.000  # Delay time
    for j in range(8):
        data[2] = ~heart[j]
        data[1] = 0xFF
        data[0] = 0xFF
        data[3] = 0x01 << j
        spi.xfer2(data)
        time.sleep(x)
        
def display_heart_blue(heart):
    x = 0.000  # Delay time
    for j in range(8):
        data[1] = ~heart[j]
        data[0] = 0xFF
        data[2] = 0xFF
        data[3] = 0x01 << j
        spi.xfer2(data)
        time.sleep(x)


def turn_off():
    x = 0.0  # Delay time
    for j in range(8):
        data[0] = 0xFF
        data[1] = 0xFF
        data[2] = 0xFF
        data[3] = 0x01 << j
        spi.xfer2(data)
        time.sleep(x)
        
def cyan():
  while  stop_flag.is_set():  # Check if the stop flag is set
        display_heart_blue(heart)
        if stop_flag.is_set():
            break
        turn_off()
        if stop_flag.is_set():
            break
        display_heart_red(heart)
        if stop_flag.is_set():
            break
        turn_off()


      
#cyan()
