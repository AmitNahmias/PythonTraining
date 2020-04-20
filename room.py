import socket

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

    def remove_client_connection_from_dict(self, client_socket: socket):
        """
        Removes client from room's dict
        @param client_socket: the connection to the client we wanna remove
        """
        del self.client_dict[client_socket]

# def forward_msg_from_client_to_all_room(self, data_from_client: bytes,
#                                         connection_to_user_that_send_the_msg: socket):
#     """
#     The method forwarding the message from one client to all the other clients in the room,
#     if user has been disconnecting the method will remove him from the client dictionary.
#     @param data_from_client: the message that the client sent :bytes
#     @param connection_to_user_that_send_the_msg: the client who sent the message socket's
#     """
#     for conn in self.client_dict:
#         if conn != connection_to_user_that_send_the_msg:
#             try:
#                 conn.send("{} said: {} ".format(self.client_dict[conn], data_from_client))
#             except ConnectionAbortedError or ConnectionResetError:
#                 self.client_dict.pop(conn)
#         else:
#             pass

# def login_client_to_room(self):
#     # TODO: run in thread from the server script inside login_to_chat method
#     """
#     Accepting client to room and announces to all the room users
#     @return:
#     """
#     connection, address = self.room_socket.accept()
#     user_name = connection.recv(BUFFER_SIZE)
#     for conn in self.client_dict:
#         try:
#             conn.send(bytes("{} joined to the room".format(user_name)))
#         except ConnectionResetError or ConnectionAbortedError:
#             self.client_dict.pop(conn)
#     self.client_dict[connection] = user_name
#     self.forward_msg_from_client_to_all_room(user_name, connection)
