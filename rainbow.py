import spidev 
import time 
from globals import stop_flag


spi = spidev.SpiDev()
spi.open(0,0) 
spi.mode = 0
spi.max_speed_hz = 5000000

image = (
    (0xc04, 0x808, 0x40C, 0x00E, 0x04C, 0x088, 0x4c4, 0x880),
    (0xc04, 0x808, 0x40C, 0x00E, 0x04C, 0x088, 0x4C4, 0x880),
    (0xC04, 0x808, 0x40c, 0x00E, 0x04C, 0x088, 0x4C4, 0x880),
    (0xC04, 0x808, 0x40C, 0x00E, 0x04C, 0x088, 0x4C4, 0x880),
    (0xC04, 0x808, 0x40C, 0x00E, 0x04C, 0x088, 0x4C4, 0x880),
    (0xC04, 0x808, 0x40c, 0x00E, 0x04C, 0x088, 0x4C4, 0x880),
    (0xc04, 0x808, 0x40C, 0x00e, 0x04c, 0x088, 0x4C4, 0x880),
    (0xc04, 0x808, 0x40C, 0x00E, 0x04C, 0x088, 0x4c4, 0x880)
)



"""Returns a binary representation of the row pixels of a specific color to be activated"""
def get_color_row_slice(row, color, slice):
    row_val = 0
    for pix in range(0, 8):
        intensity = (row[pix]//(16**(2-color)))%16 
        if intensity > slice:
            row_val += 2**pix
                       
    return row_val 



pulse_width = 16
pulse_slice_count = 0

def rainbow():
    global pulse_slice_count, pulse_width    
    try:
        while  not stop_flag.is_set():
            for row in range(0, 8):
                if stop_flag.is_set():
                    break
                data = [0xFF, 0xFF, 0xFF, 0x01 << row] 
                for color in range(0,3): # 0: Red, 1:Blue, 2: Green # Only light one color at a time on each row
                    if stop_flag.is_set():
                        break
                    if  pulse_slice_count % 3 == color:
                        # Calculate the values of the row for the color corresponding to this PWM slice
                        # Leds get activated when low so we need to send the binary complement
                        data[color] = ~get_color_row_slice(image[row], color, pulse_slice_count)  
                        #print([f"0x{image[row][pix]:03x}" for pix in range(0,8)], f"{color} {pulse_slice_count}", f"{get_color_row_slice(image[row], color, pulse_slice_count):#010b}")
                        # We send data once per row
                        # Each time we send data the previous row gets erased
                if stop_flag.is_set():
                    break
                spi.xfer(data)
                # If we wait too much between frames we need to ensure the last row gets erased
                # other wise it will remain lit until the start of the next redraw
                """ data = [0xff, 0xff, 0xff, 0x00]
                spi.xfer(data)  """
                # After we have drawn a complete screen color we wait a small time
                # A complete PWM colored screen refresh will take 3 * 16 * sleep time
            if stop_flag.is_set():
                break
            #time.sleep(0.0000001)
            pulse_slice_count += 1
            if pulse_slice_count >= pulse_width : pulse_slice_count = 0
        #time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nGot tired... cleaning up and finishing!")
        data = [0x00, 0x00, 0x00, 0x00]  # turning off the LED matrix.
        spi.xfer(data)

#rainbow()
