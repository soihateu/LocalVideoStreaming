import argparse

import cv2
import zmq
import pyautogui
import numpy as np
import threading
# import ServerChat

from constants import PORT
from utils import image_to_string
from ServerChat import *


class Streamer:

    def __init__(self, port=PORT):
        """
        Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.

        :param server_address: Address of the computer on which the StreamViewer is running, default is `localhost`
        :param port: Port which will be used for sending the stream
        """

        print("Connecting to port")
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.bind('tcp://*:' + port)
        self.keep_running = True

    def start(self):
        """
        Starts sending the stream to the Viewer.
        Creates a camera, takes a image frame converts the frame to string and sends the string across the network
        :return: None
        """
        print("Streaming Started...")
##        camera = Camera()
##        camera.start_capture()
        
        self.keep_running = True
        screenSize = (960, 540)

        while self.footage_socket and self.keep_running:
            try:
##                frame = camera.current_frame.read()  # grab the current frame
##                image_as_string = image_to_string(frame)
##                self.footage_socket.send(image_as_string)

                ss = pyautogui.screenshot()
                frame = np.array(ss)
                frame = cv2.resize(frame, screenSize)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_as_string = image_to_string(frame)
                self.footage_socket.send(image_as_string)
                
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
        print("Streaming Stopped!")
        cv2.destroyAllWindows()

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    port = PORT

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Viewer to use, default'
                             ' is ' + PORT, required=False)

    args = parser.parse_args()
    if args.port:
        port = args.port
    streamer = Streamer(port)

    streamServer = threading.Thread(target=streamer.start)
    streamServer.start()
    # streamServer.join()

    # chatServer = threading.Thread(target=ServerChat.main)
    chatServer = ServerChat()
    chatServer.main()
    # chatServer.join()


if __name__ == '__main__':
    main()
