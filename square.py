import spidev # SPI Python library
import time # delay
from globals import stop_flag


spi = spidev.SpiDev()
spi.open(0,0) # SPI0
spi.mode = 0
spi.max_speed_hz = 500000 

# Define the patterns for a spinning square
square_1 = [0xf0, 0xf0, 0xf0, 0xf0, 0x00, 0x00, 0x00, 0x00]
square_4 = [0x00, 0x00, 0x00, 0x00, 0xf0, 0xf0, 0xf0, 0xf0]
square_2 = [0xf , 0xf, 0xf, 0xf, 0x00, 0x00, 0x00, 0x00 ]
square_3 = [0x00, 0x00, 0x00, 0x00, 0xf, 0xf, 0xf, 0xf]

# Sequence of frames for the spinning animation
images = [
 
    [[square_1, 0], [square_1, 1], [square_1, 3]],
    [[square_2, 0], [square_2, 1], [square_2, 3]],
    [[square_3, 0], [square_3, 1], [square_3, 3]],
    [[square_4, 0], [square_4, 1], [square_4, 3]]


    
]

pwm_t = 0.00000000001  # Adjusted timing for better visibility
img_idx = 0
frame = 0
def square():
    global frame, img_idx, pwm_t
    try:
        while not stop_flag.is_set():
        # Update frame every few iterations
            if frame % 5 == 0:
                img_idx += 1
                if img_idx == len(images):
                    img_idx = 0

            image = images[img_idx]
            frame += 1
        
        # Update screen
            for row in range(0, 8):
                if stop_flag.is_set():
                    break
            # Update row
                cur_row = 0x01 << row

                color_counter = [0, 0, 0]
                for i in range(0, 2):  # Multiplexing color windows
                    if stop_flag.is_set():
                        break
                    for color in range(0, 3):
                        data = [0xFF, 0xFF, 0xFF, cur_row]

                        if color_counter[color] < image[color][1]:
                            data[color] = ~image[color][0][row]
                            spi.xfer(data)

                        time.sleep(pwm_t)
                        data = [0xFF, 0xFF, 0xFF, cur_row]
                        spi.xfer(data)
                        color_counter[color] += 1
                    if stop_flag.is_set():
                        break
                if stop_flag.is_set():
                    break

    except KeyboardInterrupt:
        print("\nGot tired... cleaning up and finishing!")

    finally:
        data = [0x00, 0x00, 0x00, 0x00]  # Turning off the LED matrix
        spi.xfer(data)
        print("\nTurning off")
        
