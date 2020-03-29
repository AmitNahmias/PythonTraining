import socket

BUFFER_SIZE = 1024
LOCAL_HOST = "127.0.0.1"


class Client(object):
    """This class defines client's methods and params"""

    def __init__(self, port_to_connect: str, address_to_connect: str, user_name: str):
        """
        This method initiate client object with those params:
        :param port_to_connect: the port that the client want to connect to :str
        :param address_to_connect: the address that the client want to connect to :str
        :param user_name: the user name of the client :str
        """
        self.port_to_connect = port_to_connect
        self.address_to_connect = address_to_connect
        self.user_name = user_name
        self.client_socket = socket.socket()

    def recive_data_from_client(self):
        """
        Getting from client message
        """
        data = self.client_socket.recv(BUFFER_SIZE)
        print(data.decode())

    def send_data_to_room(self, message_to_send: str):
        """
        The method sends message to the room from the client, after encoding and converting to bytes
        :param message_to_send: the message that we want to send :str
        """
        message_to_send_after_encode = message_to_send.encode()
        self.client_socket.send(bytes(message_to_send_after_encode))

    def enter_to_room(self, room_id: str):
        """
        The method joining the user to existing room
        :param room_id: the id of the room that the user wanna join to :str
        """
        self.client_socket.connect((LOCAL_HOST, int(room_id)))
        print("Dear {}, \nWelcome to room number {}".format(self.user_name, room_id))

    def leave_room(self):
        """
        This method gives to the user the option to leave the room that he is connected to
        """
        verify = input("For disconnecting write yes: ")
        if verify == "yes":
            self.client_socket.close()
        else:
            pass
