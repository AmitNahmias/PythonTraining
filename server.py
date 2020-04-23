import select, time, socket, _thread
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
        print("Server opened and listening on {} in port {}".format(self.ip, self.port))

    def close_server(self):
        """ This method close the server """
        self.server_socket.close()
        print("Server closed!")

    def delete_room(self, room_instance: Room):
        """
        Checks if room is empty, if he is empty it's deleting the room from rooms_dict
        @param room_instance: the room we wanna check
        """
        while True:
            if not bool(room_instance.client_dict):
                del self.rooms_dict[room_instance.room_id]
                break
            else:
                time.sleep(7)

    def create_room(self, room_id, client_sock: socket, name_of_client: str):
        """
        Creates new room with id that the client chosen and adding the room creator to the room's client dict
        @param room_id: the room id of the room :int
        @param client_sock: the socket of the connection to the room creator :socket
        @param name_of_client: the name of the room creator
        @return: room instance
        """
        room_instance = Room(room_id)
        self.rooms_dict[room_id] = room_instance
        print("New room has been created with the id: {}".format(room_id))
        room_instance.add_client_connection_to_dict(client_sock, name_of_client)
        # check_for_closing_room_thread = threading.Thread(target=self.delete_room(room_instance))
        # check_for_closing_room_thread.start()
        # while room_id in self.rooms_dict:
        # _thread.start_new_thread(room_instance.forwarder, ())
        room_instance.forwarder()
        return room_instance

    def home_bar_menu(self):

        """ Login the client to room or give him the option to create one """
        while self.inputs:
            new_connections, writable, exceptional = select.select(self.inputs, self.inputs, self.inputs)
            for new_con in new_connections:
                if new_con is self.server_socket:
                    connection, client_address = new_con.accept()
                    client_name = connection.recv(BUFFER_SIZE).decode()
                    connection.send(
                        bytes("Hello {},\nFor create new room press 1, for enter existing room press 2: ".format(
                            client_name).encode()))
                    client_choice = connection.recv(BUFFER_SIZE).decode()
                    if client_choice == "1":
                        connection.send(bytes("Please choose room ID: ".encode()))
                        new_room_id = connection.recv(BUFFER_SIZE).decode()
                        if new_room_id in self.rooms_dict.keys():
                            connection.send(bytes("The room is already exist, try again later!".encode()))
                        else:
                            new_room = self.create_room(new_room_id, connection, client_name)
                            connection.send(bytes("Room number {} has been opened!".format(new_room_id).encode()))
                            """Running the forwarder method, no need to run in client choice 2 because the room already 
                            exists and the method is running """
                    elif client_choice == "2":
                        connection.send(bytes(
                            "This is the room that are open: {}".format(list(self.rooms_dict.keys())).encode()))
                        client_chosen_room: str = connection.recv(BUFFER_SIZE).decode()
                        self.rooms_dict[client_chosen_room].login_new_client_to_room(client_name)
                        self.rooms_dict[client_chosen_room].add_client_connection_to_dict(connection, client_name)
                        connection.send(bytes("Welcome to room number {}".format(client_chosen_room).encode()))


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
