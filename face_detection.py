from threading import Timer
import threading
import time

class DetectorTimer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 5
    def run(self):
        while self.count > 0 and not self.event.is_set():
            self.count -= 1
            self.event.wait(1)

    def stop(self):
        self.event.set()

class CameraDetection():
    def __init__(self, frame_width, frame_height):
        # We can extend the implemention to return true if face is detected for several frames for accuracy
        # Ex. store an array of 5 continous frames with face detected
        self._face_in_middle = False
        self._face_pos = (0,0,0,0)
        self._frame_width  = frame_width
        self._frame_height = frame_height
        self.warning = None
        self.timer = None
    def setDetection(self, x, y, w, h):
        self._face_pos = (x, y, w, h)
        print(self.warning)
        if  w > self._frame_width//2  and abs(w/2 - (self._frame_width/2 - x)) < 50 :
            self._face_in_middle = True
            if not self.timer:
                self.timer = DetectorTimer()
                self.timer.start()
            elif self.timer.count == 0:
                self.timer.stop()
                self.timer = None
                # TODO: do something when timer expired
            else:
                self.warning = f"Hold still! {self.timer.count} seconds left"
        elif w <= self._frame_width//2:
            self.warning = "Come closer"
            if self.timer:
                self.timer.stop()
                self.timer = None
        elif x + w/2 < self._frame_width//2 - 50:
            self.warning = "Move left"
            if self.timer:
                self.timer.stop()
                self.timer = None
        elif x + w/2 > self._frame_width//2 + 50:
            self.warning = "Move right"
            if self.timer:
                self.timer.stop()
                self.timer = None
        else:
            self.warning = "Please move your head a little bit"
    def setNoDetection(self):
        self._face_in_middle = False
        self._face_pos = (0,0,0,0)
        self.warning = None
    def getDetection(self):
        # return position if detected else False
        return self._face_pos if self._face_in_middle else False