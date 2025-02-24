# for unix/MACos this line instructs the OS how to execute the contents of the file
#!/usr/bin/env python3


#doc string that should briefly explain the purpose and contents of the module
""" module.py - an example of a Python module """

__counter = 0


def suml(the_list):
    global __counter
    __counter += 1
    the_sum = 0
    for element in the_list:
        the_sum += element
    return the_sum


def prodl(the_list):
    global __counter    
    __counter += 1
    prod = 1
    for element in the_list:
        prod *= element
    return prod


if __name__ == "__main__":
    print("I prefer to be a module, but I can do some tests for you.")
    my_list = [i+1 for i in range(5)]
    print(suml(my_list) == 15)
    print(prodl(my_list) == 120)







"""counter = 0


print("I like to be a module.")
print(__name__)

if __name__ == "__main__":
    print("I prefer to be a module")
elif __name__ == "module":
    print("I like to be a module2e3")
else:
    print("HOLY GYATT")


# convention to let users know that they shouldn't modify, only read
# add 1 or 2 underscores before varaible name
# __hidden = 5"""