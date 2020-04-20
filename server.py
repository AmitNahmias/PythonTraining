import socket, threading, queue, select
from room import Room

BUFFER_SIZE = 1024


class Server(object):
    """This class defines server instance"""

    def __init__(self):
        """
        The definition of server is to open port on local host and port 2510.
        Any server contains rooms dict and socket server.
        """
        self.ip = "127.0.0.1"
        self.rooms_dict = {}
        self.port = 2510
        self.server_socket = socket.socket()
        self.inputs = [self.server_socket]

    def open_server(self):
        """ This method opening the server side """
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(True)
        print("Server opened and listening on {} in port: {}".format(self.ip, self.port))

    def close_server(self):
        """ This method close the server """
        self.server_socket.close()
        print("Server closed!")

    def create_room(self, room_id: int):
        """
        Creates new room with id that the client chosen
        @param room_id: the room id of the room :int
        @return: room instance
        """
        room_instance = Room(room_id)
        self.rooms_dict[room_id] = room_instance
        print("New room has been created with the id: {}".format(room_id))
        return room_instance

    def delete_room(self, room_instance: Room):
        """
        Checks if room is empty, if he is empty it's deleting the room from rooms_dict
        @param room_instance: the room we wanna check
        """
        if not bool(room_instance.client_dict):
            del self.rooms_dict[room_instance.room_id]
        else:
            pass

    def home_bar_menu(self):
        while self.inputs:
            new_connections, writable, exceptional = select.select(self.inputs, self.inputs, self.inputs)
            for srv in new_connections:
                if srv is self.server_socket:
                    connection, client_address = srv.accept()
                    #connection.setblocking(True)
                    client_name = connection.recv(BUFFER_SIZE).decode()
                    connection.send(
                        bytes("Hello, for create new room press 1, for enter existing room press 2: ".encode()))
                    client_choice = connection.recv(BUFFER_SIZE).decode()
                    if client_choice == "1":
                        connection.send(bytes("Please choose room ID:".encode()))
                        new_room_id = connection.recv(BUFFER_SIZE).decode()
                        new_room = self.create_room(new_room_id)
                        new_room.add_client_connection_to_dict(connection, client_name)
                    elif client_choice == "2":
                        connection.send(bytes(
                            "This is the room that are open: {}".format(list(self.rooms_dict.keys())).encode()))
                        client_chosen_room: str = connection.recv(BUFFER_SIZE).decode()
                        self.rooms_dict[client_chosen_room].add_client_connection_to_dict(connection, client_name)


def main():
    """
    main() -> NoneType
    Control the flow of the program
    """
    server_instance = Server()
    """using open server method to open and bind and listen"""
    server_instance.open_server()
    server_instance.home_bar_menu()


if __name__ == '__main__':
    main()
