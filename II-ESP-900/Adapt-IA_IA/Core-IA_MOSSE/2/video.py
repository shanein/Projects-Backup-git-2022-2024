import cv2

class Video :
    # def __init__(self, x=1920, y=1080, source=0):
    # def __init__(self, x=128, y=128, source=0):
    def __init__(self, x=3840, y=2160, source=0):
        self.camera_Xlength = x
        self.camera_Ylength = y
        self.camera_src = source
        self.cap = None
    def startCapture(self):
        self.cap = cv2.VideoCapture(self.camera_src)

