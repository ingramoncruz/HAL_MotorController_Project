""" This is a module that holds some useful functions in both controllers. Feel free to add more
functions if needed.
"""
import configparser

def read_ip_address(root_path, ini_path):
    """Function to read the IP Address at the Config.ini file"""
    inifile_path = root_path + ini_path
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['General']['IP Address']

def read_motor_names(root_path, ini_path):
    """Function to read which motor (according to the name convention of each controller) is
    to every generic motor define at the Config.ini file"""
    inifile_path = root_path + ini_path
    config = configparser.ConfigParser()
    config.read(inifile_path)
    return config['Motors Name']['Motor 1'], config['Motors Name']['Motor 2']
