# imports are here:
import socket

# constants are here:
BUFFER_SIZE = 1024


class Room(object):
    def __init__(self, room_id: int):
        """
        defines room methods
        """
        self.client_dict = {}
        self.room_id = room_id

    def login_to_room(self, client_socket: socket, client_user_name: str):
        """
        append client from room
        :param client_socket: the socket of the client : socket
        :param client_user_name: client's user name :str
        :return:
        """
        self.client_dict[client_socket] = client_user_name

    def logout_from_room(self, client_socket: socket):
        """
        removes client from room
        :param client_socket: the socket of the client : socket
        :return:
        """
        self.client_dict.pop(client_socket)

    def send_all(self, my_connection: socket, msg_to_send: str):
        """
        send to all room clients the message
        :param my_connection: the connection who sent the message : socket
        :param msg_to_send: the message that the server forwards
        :return:
        """
        for connection in self.client_dict.keys():
            if connection != my_connection:
                try:
                    connection.send(msg_to_send.encode())
                except ConnectionAbortedError or ConnectionResetError:
                    self.logout_from_room(connection)

    def recv_all(self):
        """
        receive messages from all users
        :return:
        """
        for connection in self.client_dict.keys():
            connection.recv(BUFFER_SIZE).decode()

    def room_handler(self):
        """
        handle in the conversation in the room
        :return:
        """
        while self.client_dict:
            for client in self.client_dict.keys():
                self.send_all(my_connection=client,
                              msg_to_send=client.recv(BUFFER_SIZE).decode())
