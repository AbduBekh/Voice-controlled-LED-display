import spidev
import time

# Define the pattern for the letter 'A'
A = [
    0xFF, 0x81, 0x81, 0x81, 
    0xFF, 0x81, 0x81, 0x81
]

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI speed (1 MHz is a common value)

def display_pattern(pattern, delay):
    for j in range(8):
        data = [0] * 4
        data[0] = ~pattern[j]
        data[1] = 0xFF
        data[2] = 0xFF
        data[3] = 0x01 << j
        spi.xfer2(data)
        time.sleep(delay)

# Main loop
try:
    while True:
        print("Displaying 'A'")  # Debug output
        display_pattern(A, 0.0)
        time.sleep(0)  # Adjust this for the update rate

except KeyboardInterrupt:
    pass

finally:
    spi.close()
    print("SPI connection closed")  # Debug output
