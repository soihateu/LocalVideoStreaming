import argparse

import cv2
import zmq
import pyautogui
import numpy as np
import msvcrt
import base64
import threading

from ServerChat import *

class Streamer:

    def __init__(self, port):
        #Establish PUBLISHER connection, binds to port 5555 by default.
        print("Connecting to port")
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.bind('tcp://*:' + port)

    def start(self):
        print("Streaming Started...")
        self.keep_running = True
        screenSize = (960, 540)
        pause = False

        while self.footage_socket:
            try:
                # Captures screenshot, resizes, fixes color and sends it over socket as np array
                ss = pyautogui.screenshot()
                frame = np.array(ss)
                frame = cv2.resize(frame, screenSize)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_as_string = self.imageToString(frame)
                self.footage_socket.send(image_as_string)
                
                # Pause if key "p" is pressed
                if msvcrt.kbhit() and ord(msvcrt.getch()) == 112:
                    pause = True
                    print("Stream paused")

                # Resume if key "p" is pressed
                while pause == True:
                    if msvcrt.kbhit() and ord(msvcrt.getch()) == 112:
                        pause = False
                        print("Streaming continued")
                        
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
            
        print("Streaming Stopped!")
        cv2.destroyAllWindows()
        
    def imageToString(self, image):
        encoded, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer)
    
def main():
    port = '5555'
    streamer = Streamer(port)

    streamServer = threading.Thread(target=streamer.start)
    streamServer.start()

    chatServer = ServerChat()
    chatServer.main()
    
    
if __name__ == '__main__':
    main()
