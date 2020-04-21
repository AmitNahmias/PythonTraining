import socket, select

BUFFER_SIZE = 1024


class Room(object):
    """The class defines a room"""

    def __init__(self, room_id: int):
        """
        This method initiate room instance.
        @param room_id: represents the room id :int
        """
        self.room_id = room_id
        self.client_dict = {}

    def add_client_connection_to_dict(self, client_socket: socket, client_user_name: str):
        """
        Adding client to room's dict
        @param client_socket: the connection to the client we wanna add
        @param client_user_name: the user name of the client
        """
        self.client_dict[client_socket] = client_user_name

    def login_new_client_to_room(self, new_client_in_room: socket):
        """
        Announces that client joined to room
        @param new_client_in_room: the new client's connection :socket
        """
        for client in self.client_dict:
            if client != new_client_in_room:
                try:
                    client.send(bytes("{} joined to the room".format(self.client_dict[new_client_in_room].encode())))
                except ConnectionResetError or ConnectionAbortedError:
                    self.logout_client_from_room(client)

    def logout_client_from_room(self, connection_to_client_that_left: socket):
        """
        Announces that client left the room
        @param connection_to_client_that_left: the connection to the client that left :socket
        """
        for client in self.client_dict:
            if client != connection_to_client_that_left:
                client.send(
                    bytes("{} has left the room".format(self.client_dict[connection_to_client_that_left].encode())))
        del self.client_dict[connection_to_client_that_left]

    def recv_data_from_client(self, client_socket: socket):
        """
        Receiving data from client
        @param client_socket: the connection to the client who sent the message :socket
        @return: data -> message
        """
        return client_socket.recv(BUFFER_SIZE).decode()

    def forward_msg_from_client_to_all_room(self, data_from_client: bytes,
                                            connection_to_user_that_send_the_msg: socket):
        """
        The method forwarding the message from one client to all the other clients in the room,
        if user has been disconnecting the method will remove him from the client dictionary.
        @param data_from_client: the message that the client sent :bytes
        @param connection_to_user_that_send_the_msg: the client who sent the message socket's :socket
        """
        while len(self.client_dict) > 1:
            for conn in self.client_dict:
                if conn != connection_to_user_that_send_the_msg:
                    try:
                        conn.send("{} said: {} ".format(self.client_dict[conn], data_from_client))
                    except ConnectionAbortedError or ConnectionResetError:
                        self.logout_client_from_room(conn)
                else:
                    pass
