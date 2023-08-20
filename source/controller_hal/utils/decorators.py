""" Here you can find some general decorators used by both controllers. You can add more ones and
and call them in the specific controller you need them."""
import logging


logging.basicConfig(
    level = logging.INFO,
    format = '%(threadName)s-%(levelname)s-%(message)s')


def error_handler(method):
    """General decorator function to check if the method is runnable."""
    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except:
            logging.error(f"Error in {method.__qualname__}")
    return wrapper


def check_connection(method):
    """Decorator to check if the controller is connected, if so, it runs the method"""
    def wrapper(*args):
        self = args[0]
        if self.connection:
            return method(*args)
        else:
            logging.info(f"Action in {method.__qualname__} not done, because you are not connected.")
    return wrapper
