import spidev
import time
import python_weather
import asyncio
import os
from globals import stop_flag


spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 250000
spi.mode = 0

weather_icons = {
    'snowy': [
        0b00100100,
        0b00011000,
        0b11111111,
        0b01111110,
        0b01111110,  
        0b11111111,  
        0b00011000,    
        0b00100100    
    ],
    'cloudy': [
        0b00000000,
        0b00000000,
        0b00001100,
        0b00011100,
        0b00111110,
        0b01111110,
        0b11111111,
        0b00000000
    ],
	'rainy': [
		0b00011000,
		0b00111100,
		0b01111110,
		0b10010001,      
		0b00010000,
		0b00010000,
		0b00011000,
		0b00011000
	],
	'sunny': [
		0b10000001,
		0b01011010,
		0b00111100,
		0b01100110,
		0b01100110,
		0b00111100,
		0b01011010,
		0b10000001          
],
	'thunder': [
		0b00000000,
		0b01000000,
		0b00100000,
		0b00011000,
		0b00001100,
		0b00000010,
		0b00000001,
		0b00000000
]
}

def display_weather_icon(icon_pattern, color):
    for row in range(8):
        data = [0xFF, 0xFF, 0xFF, 0x01 << row]
        row_data = icon_pattern[row]  
        
        for col in range(8):
            if row_data & (0x80 >> col):  
                if color == 'yellow':
                    data[2] &= ~(0x80 >> col)  
                    data[0] &= ~(0x80 >> col)
                elif color == 'cyan':
                    data[2] &= ~(0x80 >> col)  
                    data[1] &= ~(0x80 >> col)  
                elif color == 'blue':
                    data[1] &= ~(0x80 >> col)  
                
        spi.xfer(data) 
        time.sleep(0.0000002)  


def get_weather_forecast(weather_kind):
	if weather_kind in [113]:
		return 'sunny'
	elif weather_kind in [119,122,143,116]:
		return 'cloudy'
	elif weather_kind in [227, 230, 323, 335, 392]:
		return 'snowy'
	elif weather_kind in [176, 179,182, 266, 299, 302, 200,389]:
		return 'rainy'
	else:
		return 'unknown'

		
async def getweather():
	async with python_weather.Client() as client :
		weather = await client.get('debrecen')
		print(weather.kind)
		return weather.kind.value
		
def display_weather_forecast(forecast):
	if forecast == "sunny" :
		display_weather_icon(weather_icons['sunny'], 'yellow')
	elif forecast == "cloudy" :
		display_weather_icon(weather_icons['cloudy'], 'cyan')
	elif forecast == "rainy" :
		display_weather_icon(weather_icons['rainy'], 'blue')
	elif forecast == "snowy" :
		display_weather_icon(weather_icons['snowy'], 'cyan')




def displayForcast():
	global stop_flag
	forecast = get_weather_forecast(asyncio.run(getweather()))
	while not stop_flag.is_set():
		display_weather_forecast(forecast)
		

#displayForcast()
#display_weather_icon(weather_icons['cloudy'], 'cyan')
