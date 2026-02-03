#1 When a function reaches a return statement, it stops executing and sends the result back:
def get_greeting():
    return "Hellom from a function"

message = get_greeting()
print(message)

#2  You can use the returned value directly:
def get_greeting():
    return "Hello from a function"

print(get_greeting())

#3 Function definitions cannot be empty. If you need to create a function placeholder without any code
def my_function():
    pass