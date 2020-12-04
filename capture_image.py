import os
import ephem
from subprocess import call
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep

# Output Directory
outputDir = '/home/pi/send2web/'

# Get today's date at midnight
now = datetime.now()
today=datetime.combine(now.today(), datetime.min.time())

# Configure ephem observer
o = ephem.Observer()  
o.lat, o.long, o.date = '42.42', '-76.92', today

# Get sunrise and sunset times
sunrise = ephem.localtime(o.next_rising(ephem.Sun()))
sunset = ephem.localtime(o.next_setting(ephem.Sun()))

# Check if image to be captured
captureImage = False
if now >= sunrise-timedelta(hours=1) and now <= sunset+timedelta(hours=1):
    captureImage = True
elif now.minute == 0:
    captureImage = True

if captureImage:
    # Camera Setup
    camera = PiCamera()
    camera.rotation = 0
    camera.resolution = (3280, 2464)
    camera.brightness = 51 # Default 50 (0 to 100)
    camera.contrast = 0 # Default 0 (0 to 100)
    camera.saturation =  12 # Default 0 (-100 to 100)

    # Capture Image
    camera.start_preview()
    sleep(5)
    camera.capture(f'{outputDir}/{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg')
    camera.stop_preview()