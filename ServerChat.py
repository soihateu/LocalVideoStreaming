from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class ServerChat:
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(('localhost', 8888))

    clients = {}
    addresses = {}

    def accept_connection(self):
        while True:
            client, client_address = self.SERVER.accept()
            client.send(bytes("Welcome to the server!", "utf8"))
            self.addresses[client] = client_address
            self.clients[client] = client
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            message = client.recv(1024)
            self.broadcast(message)

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def main(self):
        # SERVER = socket(AF_INET, SOCK_STREAM)
        # SERVER.bind(('localhost', 8888))

        self.SERVER.listen(5)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=self.accept_connection)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()
