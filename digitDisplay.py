import spidev
import time
import datetime
from globals import stop_flag


# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI0
spi.mode = 0
spi.max_speed_hz = 500000

# Predefined digit patterns for a 4x4 grid
digits = {
    '0': [0b0110, 0b1001, 0b1001, 0b0110],
    '1': [0b0100, 0b0100, 0b0100, 0b0100],
    '2': [0b1110, 0b0100, 0b0010, 0b1110],
    '3': [0b1111, 0b0010, 0b0100, 0b1111],
    '4': [0b1001, 0b1001, 0b1111, 0b0001],
    '5': [0b1111, 0b0001, 0b0110, 0b0111],
    '6': [0b1110, 0b0010, 0b1110, 0b1110],
    '7': [0b1111, 0b1000, 0b0100, 0b0100],
    '8': [0b1110, 0b1010, 0b1110, 0b1110],
    '9': [0b1110, 0b1010, 0b1110, 0b1000]
}

# Function to display a digit in one quadrant of the matrix
def display_digit(pattern, row_offset, col_offset, color):
    for row in range(4):  # 4x4 grid for each digit
        data = [0xFF, 0xFF, 0xFF, 0x01 << (row + row_offset)]
        row_data = pattern[row]  
        
        for col in range(4):
            if row_data & (0x08 >> col):  
                if color == 'cyan':
                    data[1] &= ~(0x80 >> (col + col_offset))
                    data[2] &= ~(0x80 >> (col + col_offset))
                elif color == 'red':
                    data[0] &= ~(0x80 >> (col + col_offset))  
                elif color == 'green':
                    data[2] &= ~(0x80 >> (col + col_offset))  
                
                    
        spi.xfer(data)  
        time.sleep(0.00002)  

def test_display():
    while True:
	    display_digit(digits['0'], 0, 0, 'red')
	    display_digit(digits['2'], 0, 4, 'red')
	    display_digit(digits['5'], 4, 0, 'red')
	    display_digit(digits['3'], 4, 4, 'red')

	
	
def display_time(hours, minutes):
	h1, h2 = str(hours).zfill(2)
	m1, m2 = str(minutes).zfill(2)
	
	display_digit(digits[h2], 0, 0, 'red')
	display_digit(digits[h1], 0, 4, 'red')
	display_digit(digits[m2], 4, 0, 'cyan')
	display_digit(digits[m1], 4, 4, 'cyan')
	
def display_date(day, month):
    d1, d2 = str(day).zfill(2)
    m1, m2 = str(month).zfill(2)
    
    display_digit(digits[d2], 0, 0, 'red')
    display_digit(digits[d1], 0, 4, 'red')
    display_digit(digits[m2], 4, 0, 'cyan')
    display_digit(digits[m1], 4, 4, 'cyan')
    
def dateDisplay():
	global stop_flag
	while not stop_flag.is_set():
	    day = datetime.datetime.now().day
	    month = datetime.datetime.now().month
	    display_date(day, month)


def timeDisplay():
	global stop_flag
	while not stop_flag.is_set():
	    current_time = time.strftime("%H:%M")
	    hours, minutes = map(int, current_time.split(":"))
	    display_time(hours, minutes)
	    
def countdown(minutes, seconds):
    global stop_flag
    total_seconds = minutes * 60 + seconds
    start_time = time.time()
    while total_seconds >=0 and not stop_flag.is_set():
	    mins = total_seconds // 60
	    secs = total_seconds % 60
	
	    tens_min = mins //10
	    ones_min = mins % 10
	    tens_sec = secs //10
	    ones_sec = secs % 10
	    for _ in range(50):
		    display_digit(digits[chr(ones_min+48)], 0, 0, 'red')
		    display_digit(digits[chr(tens_min+48)], 0, 4, 'red')
		    display_digit(digits[chr(tens_sec+48)], 4, 4, 'cyan')
		    display_digit(digits[chr(ones_sec+48)], 4, 0, 'cyan')
		    time.sleep(0.0002)
	    current_time = time.time()
	    elapsed_time = current_time - start_time
	    if elapsed_time >= 1:
		    total_seconds -=1
		    start_time = current_time
	    
def parse_timer(words):
    minutes, seconds = 0,0
    words = words.split()
    if "minute" in words or "minutes" in words: 
	    if "minute" in words:
		    minute_index = words.index("minute")
	    else:
		    minute_index = words.index("minutes")
		
	    try:
		    minutes = int(words[minute_index -1])
	    except(ValueError, IndexError):
		    print("error")
    if "second" in words or "seconds" in words: 
	    if "second" in words:
		    second_index = words.index("second")
	    else:
		    second_index = words.index("seconds")
		
	    try:
		    seconds = int(words[second_index -1])
	    except(ValueError, IndexError):
		    print("error")
    return minutes, seconds
#countdown(10,10)
#timeDisplay()
#dateDisplay()
