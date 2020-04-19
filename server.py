import socket, threading
from room import Room

BUFFER_SIZE = 1024


class Server(object):
    """This class defines server instance"""

    def __init__(self):
        """
        The definition of server is to open port on local host and port 2510
        """
        self.ip = "127.0.0.1"
        self.rooms_list = []
        self.port = 2510
        self.server_socket = socket.socket()

    def open_server(self):
        """ This method opening the server side """
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        print("Server opened and listening on {} in port: {}".format(self.ip, self.port))
        self.rooms_list.append(str(self.port))

    def close_server(self):
        """ This method close the server """
        self.server_socket.close()
        self.rooms_list.remove(str(self.port))
        print("Server closed!")

    def create_room(self, port: int):
        """
        Creates new room
        @param port: the port that the room be connected to :int
        @return:
        """
        room_instance = Room(socket.socket(), port)
        room_socket = room_instance.room_socket
        room_socket.bind((self.ip, port))
        room_socket.listen()
        self.rooms_list.append(port)
        return room_instance

    def login_to_chat(self):
        """
        Login method - represents the login menu to the client
        @return:
        """
        connection, address = self.server_socket.accept()
        user_name = connection.recv(BUFFER_SIZE).decode()
        connection.send(bytes(
            'Hello {},\nTo view all opened rooms press 1, to create room press 2.'.format(user_name).encode()))
        action = connection.recv(BUFFER_SIZE).decode()
        try:
            if action == "1":
                connection.send(bytes(self.rooms_list))
            elif action == "2":
                connection.send(bytes("Choose port to open room".encode()))
                chosen_port = connection.recv(BUFFER_SIZE).decode()
                room_instance = self.create_room(int(chosen_port))
                connection.send(bytes("You opened room in port {}".format(chosen_port).encode()))
                #login_client_to_room_method_thread=threading.Thread(target=room_instance.login_client_to_room())


        except IOError:
            connection.send(bytes("Wrong action".encode()))
