""" This module is the client side """

# imports are here:
import socket

# constants are here:
HOST = "127.0.0.1"
PORT = "2510"
BUFFER_SIZE = 1024


class Client(object):
    def __init__(self, name: str):
        """
        defines client instance
        :param name: client's name :str
        """
        self.client_name = name
        self.client_socket = socket.socket()

    def connect_to_server(self):
        """
        connecting the client to the server
        :return:
        """
        self.client_socket.connect((HOST, PORT))
        self.client_socket.send(bytes(self.client_name.encode()))
        client_choice = input(
            "To create room press 1, for joining room press 2:")
        self.client_socket.send(bytes(client_choice.encode()))
        if client_choice == "1":
            room_id = input("Choose room id:")
            self.client_socket.send(bytes(room_id.encode()))
        elif client_choice == "2":
            print(self.client_socket.recv(BUFFER_SIZE).decode())
            room_id = input("To which room you want to join?")
            self.client_socket.send(bytes(room_id.encode()))
        else:
            print("Value error! {} isn't in the options".format(client_choice))
            exit()
