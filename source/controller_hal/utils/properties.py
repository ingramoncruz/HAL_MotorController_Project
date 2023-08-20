"""This file contains and defines properties used by both controllers api's."""

class PropertyDistance:
    """Property class to read the _distance value given by the input_distance controller in the
    user interface."""
    def __init__(self):
        self._distance = 0

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value


class PropertyPosition:
    """Property class to read the _position value given by the input_position controller in the
    user interface."""
    def __init__(self):
        self._position = 0

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value


class PropertyConnection:
    """Property class to read the _connected parameter which tells if the controller is connected
    or not."""
    def __init__(self):
        self._connected = False

    @property
    def connection(self):
        return self._connected

    @connection.setter
    def connection(self, value):
        self._connected = value
