import socket, select, queue

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
        self.outputs = []
        self.msg_queues = {}

    def add_client_connection_to_dict(self, client_socket: socket, client_user_name: str):
        """
        Adding client to room's dict
        @param client_socket: the connection to the client we wanna add
        @param client_user_name: the user name of the client
        """
        self.client_dict[client_socket] = client_user_name
        self.msg_queues[client_socket] = queue.Queue()

    def login_new_client_to_room(self, client_name: str):
        """
        Announces that client joined to room
        @param client_name: the new client's name :str
        """
        for client in self.client_dict:
            try:
                client.send(bytes("{} joined to the room".format(client_name).encode()))
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
                    bytes("{} has left the room".format(self.client_dict[connection_to_client_that_left]).encode()))
        del self.msg_queues[connection_to_client_that_left]
        del self.client_dict[connection_to_client_that_left]

    def forward_msg_from_client_to_all_room(self, data_from_client,
                                            connection_to_user_that_send_the_msg: socket):
        """
        Forwarding the message from one client to all the other clients in the room,
        if user has been disconnecting the method will remove him from the client dictionary.
        @param data_from_client: the message that the client sent :bytes
        @param connection_to_user_that_send_the_msg: the client who sent the message socket's :socket
        """
        for conn in self.client_dict:
            if conn != connection_to_user_that_send_the_msg:
                try:
                    conn.send(bytes(data_from_client.encode()))
                except ConnectionAbortedError or ConnectionResetError:
                    self.logout_client_from_room(conn)
            else:
                pass

    def forwarder(self):
        """ Hopefully will do the magic in chat """
        while len(self.client_dict) > 1:
            # readable, writable, exceptional = select.select(self.client_dict, self.outputs, self.client_dict)
            print(self.msg_queues)
            for client_connection in self.client_dict:
                data = client_connection.recv(BUFFER_SIZE).decode()
                if data:
                    self.msg_queues[client_connection].put(data)
                    if client_connection not in self.outputs:
                        self.outputs.append(client_connection)
                elif data == "Exit":
                    self.logout_client_from_room(client_connection)
                    self.outputs.remove(client_connection)
                else:
                    pass
            for client_connection in self.outputs:
                try:
                    next_msg = self.msg_queues[client_connection].get_nowait()
                except queue.Empty:
                    self.outputs.remove(client_connection)
                else:
                    self.forward_msg_from_client_to_all_room(next_msg, client_connection)
