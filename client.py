""" This module is the client side """

# imports are here:
import socket, _thread

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

    def send_msg(self):
        data_to_send = input()
        while data_to_send != "~exit~":
            self.client_socket.send(bytes(data_to_send.encode()))
            data_to_send = input()

    def recv_msg(self):
        while True:
            self.client_socket.recv(BUFFER_SIZE).decode()

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
            response_from_server = self.client_socket.recv(BUFFER_SIZE).decode()
            print(response_from_server)
            if response_from_server == "Room  {} is already exist".format(
                    room_id):
                exit()
        elif client_choice == "2":
            print(self.client_socket.recv(BUFFER_SIZE).decode())
            room_id = input("To which room you want to join?")
            self.client_socket.send(bytes(room_id.encode()))
        else:
            print("Value error! {} isn't in the options".format(client_choice))
            exit()
        _thread.start_new_thread(function=self.send_msg())
        _thread.start_new_thread(function=self.recv_msg())


def main():
    client_name = input("Enter name:")
    client_instance = Client(client_name)
    client_instance.connect_to_server()


if __name__ == '__main__':
    main()
