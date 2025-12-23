def log_args_kwargs(func):
    def wrapper(*args, **kwargs):
        print(f"Positional arguments: {args}")
        print(f"Keyword arguments: {kwargs}")
        return func(*args, **kwargs)
    return wrapper



@log_args_kwargs
def my_function(x, y, **kwargs):
    return x + y

my_function(10, 20, debug=True, verbose=False)
# Вывод:
# Positional arguments: (10, 20)
# Keyword arguments: {'debug': True, 'verbose': False}