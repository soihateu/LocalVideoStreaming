import tkinter

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from functools import partial


class ClientChat:

    def __init__(self, name):
        self.name = name

    def get_message(self, sock, msg_lst):
        while True:
            try:
                message = sock.recv(1024).decode("utf8")
                msg_lst.insert(tkinter.END, message)
            except OSError:
                break

    def send_message(self, msg, sock, tp, event=None):
        message = msg.get()
        msg.set("")
        sock.send(bytes("<" + self.name + "> " + message, "utf8"))

        if message == "quit":
            sock.close()
            tp.quit()

    def on_close(self, msg, sock, tp, event=None):
        msg.set("quit")
        self.send_message(msg, sock, tp)

    def start(self, event=None):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(('localhost', 8888))

        top = tkinter.Tk()
        top.title("Chatter")

        messages_frame = tkinter.Frame(top)
        my_message = tkinter.StringVar()  # For the messages to be sent.
        # my_message.set("Type your messages here.")
        scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
        # Following will contain the messages.
        message_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        message_list.pack()
        messages_frame.pack()

        entry_field = tkinter.Entry(top, textvariable=my_message)
        entry_field.bind("<Return>", self.send_message)
        entry_field.pack()
        send_message_partial = partial(self.send_message, my_message, client_socket, top)
        send_button = tkinter.Button(top, text="Send", command=send_message_partial)
        send_button.pack()

        on_close_partial = partial(self.on_close, my_message, client_socket, top)
        top.protocol("WM_DELETE_WINDOW", on_close_partial)

        get_message_partial = partial(self.get_message, client_socket, message_list)
        receive_thread = Thread(target=get_message_partial)
        receive_thread.start()
        tkinter.mainloop()
