import spidev
import time
import python_weather
import asyncio
import os
from globals import stop_flag

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 5000000
spi.mode = 0


async def getweather():
	async with python_weather.Client() as client :
		weather = await client.get('debrecen')
		print(weather.temperature)
		return weather.temperature
		#for daily in weather.daily_forecasts:
			#print(daily)
			#for hourly in daily.hourly_forecasts:
				#print(f'-->{hourly!r}')


digits = {
    0: [0b0110, 0b1001, 0b1001, 0b1001, 0b1001, 0b0110],  
    1: [0b0100, 0b0110, 0b0100, 0b0100, 0b0100, 0b1110],  
    2: [0b1111, 0b1001, 0b0100, 0b0010, 0b0001, 0b1111],  
    3: [0b0110, 0b1001, 0b0100, 0b0100, 0b1001, 0b0110],  
    4: [0b1000, 0b1100, 0b1010, 0b1111, 0b1000, 0b1000],  
    5: [0b1111, 0b0001, 0b0111, 0b1000, 0b1001, 0b0110],  
    6: [0b0110, 0b0001, 0b0111, 0b1001, 0b1001, 0b0110],  
    7: [0b1111, 0b1000, 0b0100, 0b0010, 0b0001, 0b0001],  
    8: [0b0110, 0b1001, 0b0110, 0b1001, 0b1001, 0b0110],  
    9: [0b0110, 0b1001, 0b1110, 0b1000, 0b1001, 0b0110]   
}

minus_sign = [0b0000,0b0011, 0b0000, 0b0000]


# Display function
def display_digit(pattern, row_offset, col_offset, color):
    for row in range(6):  
     
        data = [0xFF, 0xFF, 0xFF, 0x01 << (row+ row_offset)]
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
        #time.sleep(0.2)  
   

def display_temperature(temp):

	if temp < 0:
		temp = abs(temp)
		tens = temp // 10
		ones = temp % 10
		for row in range (1):
			data = [0xff, 0xff,0xff,0x01 << row]
			data[1] &= ~(0x03)
			spi.xfer(data)
		
		display_digit(digits[ones], 2,0, 'cyan')
		display_digit(digits[tens], 2,4, 'cyan')
	else:
		tens = temp // 10
		ones = temp % 10
		display_digit(digits[ones], 2,0, 'red')
		display_digit(digits[tens], 2,4, 'red')

def tempDisplay():
	global stop_flag
	temp=asyncio.run(getweather())
	while not stop_flag.is_set():
				display_temperature(temp)  

#tempDisplay()
