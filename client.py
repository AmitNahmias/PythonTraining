import socket

BUFFER_SIZE = 1024
LOCAL_HOST = "127.0.0.1"
PORT_TO_SERVER = 2510


class Client(object):
    """This class defines client's methods and params"""

    def __init__(self, user_name: str):
        """
        This method initiate client object with those params:
        @param user_name: the user name of the client :str
        """
        self.user_name = user_name
        self.client_socket = socket.socket()

    def login(self):
        """
        Login to the main server and using in his menu
        @return:
        """
        self.client_socket.connect((LOCAL_HOST, PORT_TO_SERVER))
        self.client_socket.send(bytes(self.user_name.encode()))
        action = input(self.client_socket.recv(BUFFER_SIZE).decode())
        self.client_socket.send(bytes(action.encode()))
        try:
            if action == "1":
                print(self.client_socket.recv(BUFFER_SIZE).decode())
                chosen_room_port = input("To which room you wanna join?")
                self.enter_to_room(chosen_room_port)
            elif action == "2":
                chosen_port = input(self.client_socket.recv(BUFFER_SIZE).decode())
                self.client_socket.send(bytes(chosen_port.encode()))
                print(self.client_socket.recv(BUFFER_SIZE).decode())
                self.enter_to_room(chosen_port)
        except:
            print(self.client_socket.recv(BUFFER_SIZE).decode())

    def enter_to_room(self, port: str):
        """
        Joining the user to room.
        @param port: the port of the room that the user wanna join to :str
        """
        self.client_socket.close()
        self.client_socket = socket.socket()
        self.client_socket.connect((LOCAL_HOST, int(port)))
        self.client_socket.send(bytes(self.user_name.encode()))
        print("Dear {}, \nWelcome to room number {}".format(self.user_name, port))

    def receive_data_from_client(self):
        """ Getting from client message """
        data = self.client_socket.recv(BUFFER_SIZE)
        print(data.decode())

    def send_data_to_room(self):
        """
        The method sends message to the room from the client, after encoding and converting to bytes
        @param message_to_send: the message that we want to send :str
        """
        message_to_send = self.user_name + input()
        self.client_socket.send(bytes(message_to_send.encode()))

    # def leave_room(self):
    #     """ This method gives to the user the option to leave the room that he is connected to """
    #     verify = input("For disconnecting replay yes: ")
    #     if verify == "yes":
    #         self.client_socket.close()
    #     else:
    #         pass
