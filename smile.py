import spidev
import time
from globals import stop_flag


# Define SPI bus and device
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, device 0
spi.max_speed_hz = 500000
spi.mode = 0



smiley_face = [
    0x3C, 0x42, 0xA5, 0x81,
    0xA5, 0x99, 0x42, 0x3C
]


# Initialize data buffer
data = [0x00, 0x00, 0x00, 0x00]

# Function to display heart pattern
def display():
    x = 0.00  # Delay time
    for j in range(8):
        data[0] = ~smiley_face[j]
        data[1] = 0xFF
        data[2] = 0xFF
        data[3] = 0x01 << j
        spi.xfer2(data)
        time.sleep(x)


def smile():
    while not stop_flag.is_set():
        display()
    


