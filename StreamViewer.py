import argparse

import cv2
import numpy as np
import zmq
import threading
# import ClientChat

from constants import PORT, SERVER_ADDRESS
from utils import string_to_image
from ClientChat import *


class StreamViewer:

    def __init__(self, server_address=SERVER_ADDRESS, port=PORT):
        """
        Binds the computer to a ip address and starts listening for incoming streams.

        :param port: Port which is used for streaming
        """
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.connect('tcp://' + server_address + ':' + port)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        self.current_frame = None
        self.keep_running = True

    def receive_stream(self, display=True):
        """
        Displays displayed stream in a window if no arguments are passed.
        Keeps updating the 'current_frame' attribute with the most recent frame, this can be accessed using 'self.current_frame'
        :param display: boolean, If False no stream output will be displayed.
        :return: None
        """
        
        print("Connecting to stream")

        self.keep_running = True
        while self.footage_socket and self.keep_running:
            try:
                frame = self.footage_socket.recv_string()
                self.current_frame = string_to_image(frame)

                if display:
                    cv2.imshow("Stream", self.current_frame)
                    cv2.waitKey(1)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
        print("Streaming Stopped!")

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False

def main():
    port = PORT
    server_address = SERVER_ADDRESS

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        help='IP Address of the server which you want to connect to, default'
                             ' is ' + SERVER_ADDRESS,
                        required=True)
    parser.add_argument('-p', '--port',
                        help='The port which you want the Streaming Server to use, default'
                             ' is ' + PORT, required=False)

    args = parser.parse_args()

    if args.port:
        port = args.port
    if args.server:
        server_address = args.server

    stream_viewer = StreamViewer(server_address, port)
    streamClient = threading.Thread(target=stream_viewer.receive_stream)
    streamClient.start()
    # streamClient.join()

    # chatClient = threading.Thread(target=ClientChat.main)
    chatClient = ClientChat("name")
    chatClient.start()
    # chatClient.join()
    # stream_viewer.receive_stream()


if __name__ == '__main__':
    main()
