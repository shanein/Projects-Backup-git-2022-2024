import cv2

class Video :
    def __init__(self, x=1920, y=1080, source=1):
        self.camera_Xlength = x
        self.camera_Ylength = y
        self.camera_src = source
        self.cap = None
    def startCapture(self):
        self.cap = cv2.VideoCapture(self.camera_src)