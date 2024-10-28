import spidev
from datetime import date
from globals import stop_flag, running
from time import sleep

spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 500000

def send_spi_data(data):
    spi.xfer2(data)
    
def display_pattern(pattern, color):
    for j in range(8):
        data = [~pattern[j], color[0], color[1], 0x01 << j]
        send_spi_data(data)
        sleep(0.002)


def clear_matrix():
    blank = [0x00] * 8
    display_pattern(blank, (0xFF, 0xFF))


def exit_program():
    global stop_flag, running
    stop_flag.set()  # Stop any running threads
    print("...")
    clear_matrix()
    sleep(1)
    print("...")
    sleep(1)
    print("...")
    sleep(1)
    running = False  # Set the flag to False to exit the loop
    print(f"Running flag set to {running}")


#clear_matrix()
