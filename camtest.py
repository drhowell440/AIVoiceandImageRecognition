import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.start_preview()
    camera.start_recording('my_video.h264')
    time.sleep(1)  
    camera.zoom=(1/100.,1/100.,1,1)
    time.sleep(10)
    camera.stop_recording()