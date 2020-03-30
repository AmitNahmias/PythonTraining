import socket
from server import Server
from client import Client

BUFFER_SIZE = 1024


class Room(object):
    """The class defines a room"""

    def __init__(self, port_from_user: str, user: Client):
        """
        This method initiate room instance.
        :param port_from_user: getting port from user and open room in this port :str
        :param user: getting the user that opened the room: Client
        """
        self.port_from_user = port_from_user
        self.room_id = port_from_user
        self.client_dict = {}
        self.room = Server(int(self.port_from_user))
        self.user = user

    def login(self):
        """ This method getting user name from client and map it to client's dictionary according
        the connection socket """
        connection, address = self.room.server_socket.accept()
        connection.send(bytes("Hello, what is your name?".encode()))
        user_name = connection.recv(BUFFER_SIZE).decode()
        self.client_dict[connection] = user_name

    def logout(self, connection_that_left: socket):
        """
        The method removes client from the client dictionary.
        :param connection_that_left: the socket that connected to the leaving client.
        """
        self.client_dict.pop(connection_that_left)

    def recv_msg(self, connection: socket):
        """
        The method receives message from client.
        :param connection: the connected socket to the client :socket
        :return: the message and the connected socket.
        """
        data_to_send = connection.recv(BUFFER_SIZE)
        return data_to_send, connection

    def forward_msg_from_client_to_all_room(self, data_from_client: bytes,
                                            connection_to_user_that_send_the_msg: socket):
        """
        The method forwarding the message from one client to all the other clients in the room,
        if user has been disconnecting the method will remove him from the client dictionary.
        :param data_from_client: the message that the client sent :bytes
        :param connection_to_user_that_send_the_msg: the client who sent the message socket's
        """
        for conn in self.client_dict:
            if conn != connection_to_user_that_send_the_msg:
                try:
                    conn.send("{} said: {} ".format(self.client_dict[conn], data_from_client))
                except ConnectionAbortedError or ConnectionResetError:
                    self.client_dict.pop(conn)
            else:
                pass
