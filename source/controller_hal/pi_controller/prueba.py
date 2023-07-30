class MyClass:
    @staticmethod
    def my_decorator(cls):
        def wrapper(*args, **kwargs):
            print("Decorator action before calling the method.")
            result = cls(*args, **kwargs)
            print("Decorator action after calling the method.")
            return result
        return wrapper

    @my_decorator   # Using the my_decorator method as a decorator for the method below
    def some_method(self, x, y):
        return x + y

# Creating an instance of the class
obj = MyClass()

# Calling the method that uses the decorator
result = obj.some_method(5, 3)

# Output:
# Decorator action before calling the method.
# Decorator action after calling the method.

print("Result:", result)  # Output: Result: 8
