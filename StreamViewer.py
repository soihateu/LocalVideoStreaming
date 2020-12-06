import argparse

import cv2
import numpy as np
import zmq
import msvcrt
import time
import base64
import threading

from ClientChat import *

class StreamViewer:
    def __init__(self, server_address, port):
        # Establish SUBSCRIBER connection, connects to address and port specified
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.connect('tcp://' + server_address + ':' + port)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        self.current_frame = None

    # Recieves frame from the PUBLISHER and displays it
    def receive_stream(self, display = True):
        
        print("Connecting to stream...")
        print("Enter P to pause")

        pause = False
        
        while self.footage_socket:
            try:
                frame = self.footage_socket.recv_string()
                self.current_frame = self.string_to_image(frame)

                if display:
                    cv2.imshow("Stream", self.current_frame)
                    cv2.waitKey(1)

                # Pause if key "p" is pressed
                if msvcrt.kbhit() and ord(msvcrt.getch()) == 112:
                    pause = True
                    print("Stream paused")

                # Resume if key "p" is pressed
                while pause == True:
                    if msvcrt.kbhit() and ord(msvcrt.getch()) == 112:
                        pause = False
                        print("Resume watching")

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
            
        print("Stopped watching stream!")

    def string_to_image(self, string):
        img = base64.b64decode(string)
        npimg = np.frombuffer(img, dtype=np.uint8)
        return cv2.imdecode(npimg, 1)
    
def main(address, username):
    port = '5555'
    server_address = address
    stream_viewer = StreamViewer(server_address, port)
    
    streamClient = threading.Thread(target=stream_viewer.receive_stream)
    streamClient.start()

    chatClient = ClientChat(username)
    chatClient.start()

if __name__ == '__main__':
    main()
