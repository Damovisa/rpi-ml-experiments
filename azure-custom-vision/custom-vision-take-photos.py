from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep

hat = SenseHat()
cam = PiCamera()

# sense images
G = [0,200,0]
Y = [200,200,0]
O = [0,0,0]
black =  [O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,O]

tick =   [O,O,O,O,O,O,O,O,
          O,O,O,O,O,O,O,G,
          O,O,O,O,O,O,G,O,
          O,O,O,O,O,G,O,O,
          G,O,O,O,G,O,O,O,
          O,G,O,G,O,O,O,O,
          O,O,G,O,O,O,O,O,
          O,O,O,O,O,O,O,O]

wait =   [O,O,O,Y,Y,O,O,O,
          O,O,Y,O,O,Y,O,O,
          O,Y,O,O,O,O,Y,O,
          Y,O,Y,Y,Y,Y,O,Y,
          Y,O,Y,Y,Y,Y,O,Y,
          O,Y,O,O,O,O,Y,O,
          O,O,Y,O,O,Y,O,O,
          O,O,O,Y,Y,O,O,O]

cam.resolution = [227,227]
cam.preview_alpha = 128
cam.start_preview()
hat.set_pixels(wait)
sleep(2)
hat.clear()

i=0
running = True
while running:
    event = hat.stick.wait_for_event()
    if event.action == "pressed":
        if event.direction == "up":
            cam.capture('./images/u-' + str(i) + '.jpg')
            hat.set_pixels(tick)
            sleep(1)
            i = i+1
        if event.direction == "down":
            cam.capture('./images/d-' + str(i) + '.jpg')
            hat.set_pixels(tick)
            sleep(1)
            i = i+1
        if event.direction == "right":
            cam.capture('./images/r-' + str(i) + '.jpg')
            hat.set_pixels(tick)
            sleep(1)
            i = i+1
        if event.direction == "left":
            cam.capture('./images/l-' + str(i) + '.jpg')
            hat.set_pixels(tick)
            sleep(1)
            i = i+1
        if event.direction == "middle":
            running = False
        hat.clear()
    sleep(0.1)
    
cam.stop_preview()
