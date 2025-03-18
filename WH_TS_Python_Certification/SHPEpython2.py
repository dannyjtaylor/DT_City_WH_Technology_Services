# notes from python mtg

# classes and objects
# passing no arguments, uses no default values from constuctor function, (like no arg construct from C)
# "self" is a keyword only for the instance of a class, is a parameter thats a reference to the current instance of class, used to access variables that belong to the class
# "del" keyword can delete object properties/objects as a whole

# "instance method" means it can change an instance. so it accesses the object (instance of a class) and changes it

#print(dog1.sound)
#__name__ and __main__, __main__ is used for main module
#can change "self" but is generally not practiced this way


#encapsulation
# _credit
# __password

# using 1 underscore means its protected (instead of the actual keyword like C)
# using 2 means its private, 0 means its public

class Account:
    def __init__(self):
        username = "gyatt"
        credit = 200
        password = "SpicyPepper"

#protected is NOT truly private, can be accessed from outside. can be accessed and modified, but with get/set methods.

# need to overload operators like C
def __add__(self, other):
    return self.amount + other.amount

# class1 + class2 = __add__(class1, class2)


# 1. C
# 2. C
# 3. B



# inheritance

# can overload and overwrite, 
# need suoer().init(name, lname) to make sure only child class has it and does not take it from the the parent
# adding a method in child class with same name as afunction in the parent class, the inheritance of the parent method will be overridden
# using a parent method in child still works even if its not defined int he child one


# abstraction
# units inner workings are hidden from users and other units
# from abc import ABC, abstractmethod
# abc module provides tools to create abstract classes in Python.
# have to implement all the abstract methods in the children



# polymorphism
# methods in different classes to share name name but perform distinct tasks
# allows u to write more flexible and maintanable code by enaabling u to use a single interface to represent underlying forms


# modules and packages
# very common is math
# use dir() to list all funcition names or variable names in a module
# reads everything when u import

#area.py
def square(side):
    """Gets the area of a square."""
    return side**2
def rectangle(length, width):
    return length * width
def triangle(base, height):
    return base * height * 0.5


#calling help(module_name) in a shell is a convenient way to learn about it

#PIP
# package manager for pthon packages
# pip --version


# error handling
# professional to do, can run into edge cases
# prevents programs from carshing

#try, except, and finally keywords
# important for handling API calls, invalid user inputs, unpxpected runtime errors, file operations



#very good for PRODUCTION
# can use assert for flagging
# good for
import requests
try:
    response = requests.get("api.com/data")
    #look up what json means
    data = response.json()
except Exception as ex:
    #use fstring, TRUST SHRIRAJ 
    print(f"Error: {ex}")
finally:
    print("The 'try except' is finished")


# file handling

# file handling refers to process of perfomring operations on a file like creating, opening, reading, writing, and closing, thru a programmign interface
# open(): opens and returns a file
# two parameters: filename, and mode   (filename in directory)
# 'r' - read: default value, opens file for reading
# 'a' - Append: opens file for appending, makes file if it doesn't exist. (line below last line)
# 'w' - Write: opens file for writing, creating the file if it doesn't exist
# 'x' - Create: creates the specified file, errors if it exists already (not used typically)
read() # reads data
write() # writes data to a file
close() # closes file, releasing resources


# Open File
file = open("example.txt", "r")
print("File Opened Successfully")

#Write text into file
file.write("Hi everybody!")
print("Text written to file") 
#other stuff



# LEETCODE
# python is good for leetcode since it has built in data structures, no pointers, many built in fnuctions, quick debugging and testing, no need to compile code,
# widely used in backend due to ability of handling. apparently main language for AI/ML
# no need for memory allocation, python references for u
# sorted(), split(), min(), max(), sum(), set(), reserved()