from module import suml, prodl
from sys import path

path.append('..\\modules') #use \\ to escape backslash

#absolute path
path.append('C:\\Users\\18639\\anaconda3\\Test_Folder\\Test')

zeroes = [0 for i in range(5)]
ones = [1 for i in range(5)]
print(suml(zeroes))
print(prodl(ones))