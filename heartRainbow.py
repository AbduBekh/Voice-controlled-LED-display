import spidev  # SPI Python library
import time    # delay
from globals import stop_flag


# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0
spi.mode = 0
spi.max_speed_hz = 5000000

# Define the HEART pattern
HEART = [0b00000000, 0b01100110, 0b11111111, 0b11111111, 0b11111111, 0b01111110, 0b00111100, 0b00011000]
small = [
    0x00, 0x00, 0x24, 0x7E,
    0x7E, 0x3C, 0x18, 0x00
]
# Define multiple images with different color intensities
# [Pattern, Red Intensity, Green Intensity, Blue Intensity]
images = [
    [[HEART, 3], [HEART, 0], [HEART, 0]],  # All colors off
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 0], [HEART, 1]],  # Orange (High Red, Low Green, No Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 1], [HEART, 3], [HEART, 3]],  # Turquoise (Low Red, High Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 0], [HEART, 2]],  # Orange variant (High Red, Medium Green, No Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 2], [HEART, 3], [HEART, 3]],  # Turquoise variant (Medium Red, High Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 0], [HEART, 3]],  # Yellow (High Red, High Green, No Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 1], [HEART, 3], [HEART, 1]],  # Purple (Low Red, Low Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 3], [HEART, 0]],  # Pink (High Red, No Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 0], [HEART, 0]],  # Red (High Red, No Green, No Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 0], [HEART, 0], [HEART, 3]],  # Green (No Red, High Green, No Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 0], [HEART, 3], [HEART, 0]],  # Blue (No Red, No Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 3], [HEART, 3], [HEART, 3]],  # White (High Red, High Green, High Blue)
    [[small, 3], [small, 0], [small, 0]],
    [[HEART, 2], [HEART, 2], [HEART, 2]],  # Grey (Medium Red, Medium Green, Medium Blue)
    [[small, 0], [small, 0], [small, 0]],
    [[HEART, 1], [HEART, 1], [HEART, 1]],
    [[small, 3], [small, 0], [small, 0]],
# Dim White (Low Red, Low Green, Low Blue)
]

# Timing for Pulse Width Modulation (PWM)
pwm_t = 0.00001  # Slightly longer delay for better visibility
img_idx = 0
frame = 0

def heartColors():
    global img_idx, frame
    try:
        while not stop_flag.is_set():
        # Change image every 16 frames for longer display time
            if frame % 50 == 0:
                img_idx += 1
                if img_idx == len(images):
                    img_idx = 0

            image = images[img_idx]
            frame += 1

        # Update screen
            for row in range(8):
            # Select the current row
                cur_row = 0x01 << row

            # Initialize color counters
                color_counter = [0, 0, 0]
                for i in range(4):  # Multiplexing color windows for more intensity levels
                    if stop_flag.is_set():  # Check the stop flag before each multiplexing iteration
                        break
                    for color in range(3):
                        data = [0xFF, 0xFF, 0xFF, cur_row]

                        if color_counter[color] < image[color][1]:
                            data[color] = ~image[color][0][row]  # Set the pattern for the specific color
                            spi.xfer(data)

                        time.sleep(pwm_t)  # Short delay for PWM effect
                        data = [0xFF, 0xFF, 0xFF, cur_row]
                        spi.xfer(data)  # Turn off the current row
                        color_counter[color] += 1
                        
                    if stop_flag.is_set():  # Check the stop flag before the next row
                        break
                        

    except KeyboardInterrupt:
        print("\nGot tired... cleaning up and finishing!")
        data = [0x00, 0x00, 0x00, 0x00]  # Turn off the LED matrix
        spi.xfer(data)
    finally:
        # Clean up: Turn off the LED matrix
        data = [0x00, 0x00, 0x00, 0x00]
        spi.xfer(data)
        print("LED matrix turned off, function exiting.")
#heartColors()
