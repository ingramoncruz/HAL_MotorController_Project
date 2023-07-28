
class Example:
    def __init__(self):
        print('Example')

class Controller:
    def __init__(self):
        self._Motor_Name = 'Default'

    @property
    def Motor_Name(self):
        print(self._Motor_Name)
        return self._Motor_Name

    @Motor_Name.setter
    def Motor_Name(self, value):
        self._Motor_Name = value

    @Motor_Name.deleter
    def Motor_Name(self):
        print('Deleting variable')
        del self._Motor_Name


if __name__ == '__main__':
    a = Controller()
    a.Motor_Name
    a.Motor_Name = 'Newport'
    a.Motor_Name
    del a.Motor_Name
    a.Motor_Name = 'PI'
    a.Motor_Name
