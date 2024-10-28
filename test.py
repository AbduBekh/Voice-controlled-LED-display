import time
import spidev

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 0

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 500000
spi.mode = 0

# setting delay durations
x = 0.5
# define message information
msg = [0x00, 0x66, 0xFF, 0xFF, 0xFF, 0x7E, 0x3C, 0x18]
# define method to clear screen. 
def clear():
    msg = [0x00, 0x00, 0x00]
    spi.xfer2(msg)
    time.sleep(x)
    
def scroll_text(text):
    for char in text: 
        char_pattern = get_char_pattern(char)
        for row in char_pattern:
            spi.xfer2([row, 0xFF, 0xFF])
            time.sleep(0.1)
            clear()

# loop 
while True:
    # define colors
    blue = [0x00, 0xff, 0xff]
    green = [0xff, 0x00, 0xff]
    red = [0xff, 0xff, 0xff]
    demo1 = [0xff, 0xAA, 0xff]
    demo2 = [0xff, 0x55, 0xff]

    spi.xfer2(red)
    time.sleep(x)
    spi.xfer2(green)
    time.sleep(x)
    spi.xfer2(blue)
    time.sleep(x)
    spi.xfer2(demo1)
    time.sleep(x)
    spi.xfer2(demo2)
    time.sleep(x)
    clear()
    time.sleep(x)
    clear()
