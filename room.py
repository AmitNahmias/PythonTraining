import socket
from server import Server


class Room(object):
    """The class defines a room"""

    def __init__(self, port_from_user: str):
        """
        This method initiate room instance
        :param port_from_user: getting port from user and open room in this port :str
        """
        self.port_from_user = port_from_user
        self.room_id = port_from_user
        self.client_list = []
        self.room = Server(int(self.port_from_user))
