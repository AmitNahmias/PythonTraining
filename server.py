import socket

BUFFER_SIZE = 1024


class Server(object):
    """This class defines server instance"""

    def __init__(self, port: int):
        """
        The definition of server is to open port on local host
        :param port: the port to open the server :str
        """
        self.ip = "127.0.0.1"
        self.rooms_list = []
        self.port = port
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


    def open_rooms(self):
        """
        Show's the open room according to client's request
        @return: rooms list : list
        """
        return self.rooms_list
