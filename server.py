""" This module is the server side """

# imports are here:
import socket, _thread
import client, room

# constants are here:
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2510
BUFFER_SIZE = 1024


class Server(object):
    def __init__(self):
        """ define the server methods """
        self.server_socket = socket.socket()
        self.new_rooms = {}
        self.rooms = {}

    def open_server(self):
        """ binding the server socket to ip and port and starting to listen """
        self.server_socket.bind((SERVER_IP, SERVER_PORT))
        self.server_socket.listen(20)
        print(
            "Server is opened and listening on {} in port {}".format(SERVER_IP,
                                                                     SERVER_PORT))

    def close_server(self):
        """ This method close the server """
        self.server_socket.close()
        print("Server is closed!")

    def create_new_room(self, room_id: int):
        """
        creates new room
        :param room_id: room id :int
        :return: room instance :room
        """
        new_room_instance = room.Room(room_id)
        self.new_rooms[room_id] = new_room_instance
        return new_room_instance

    def move_room(self, room_instance: room):
        pass

    def client_handler(self, socket_to_client: socket):
        """
        handle in the client side communication
        :param socket_to_client: the connection to the :client
        :return:
        """
        user_name = socket_to_client.recv(BUFFER_SIZE).decode()
        client_choice = socket_to_client.recv(BUFFER_SIZE).decode()
        if client_choice == "1":
            room_id = socket_to_client.recv(BUFFER_SIZE).decode()
            room_instance = self.create_new_room(room_id=room_id)
            room_instance.login_to_room(client_socket=socket_to_client,
                                        client_user_name=user_name)
        else:
            socket_to_client.send(bytes(
                "This is the opened room: {}".format(self.rooms).encode()))
            room_id = socket_to_client.recv(BUFFER_SIZE).decode()
            self.rooms[room_id].login_to_room(client_socket=socket_to_client,
                                              client_user_name=user_name)

    def server_handler(self):
        """ handle in the server side communication """
        while True:
            client_socket, client_address = self.server_socket.accept()
            _thread.start_new_thread(
                self.client_handler(socket_to_client=client_socket))
            if self.new_rooms:
                for room in self.new_rooms:
                    _thread.start_new_thread(room.room_handler)
                    self.move_room(room_instance=room)
