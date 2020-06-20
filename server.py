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
        # if room_id in self.rooms:

        new_room_instance = room.Room(room_id)
        self.new_rooms[room_id] = new_room_instance
        return new_room_instance

    def move_room(self, room_id: int):
        """
        moving the room from the new one's dict to existing rooms dict
        :param room_id: room id :int
        :return:
        """
        self.rooms[room_id] = self.new_rooms[room_id]
        self.new_rooms.pop(room_id)

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
            if room_id not in self.new_rooms.keys() and room_id not in self.rooms.keys():
                room_instance = self.create_new_room(room_id=room_id)
                room_instance.login_to_room(client_socket=socket_to_client,
                                            client_user_name=user_name)
                socket_to_client.send(bytes(
                    "Room {} created successfully".format(room_id).encode()))
            else:
                socket_to_client.send(
                    bytes("Room  {} is already exist".format(room_id).encode()))
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
                function=self.client_handler(socket_to_client=client_socket))
            if self.new_rooms:
                for room_id in self.new_rooms:
                    self.move_room(room_id=room_id)
                    _thread.start_new_thread(self.rooms[room_id].room_handler,
                                             ())


def main():
    server_instance = Server()
    server_instance.server_handler()


if __name__ == '__main__':
    main()
