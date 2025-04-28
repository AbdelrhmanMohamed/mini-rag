import os

# file = open("test.txt")


# print(os.getcwd())

print(os.path.dirname(os.path.dirname(__file__)))


file = open(f'{os.getcwd()}/ab.txt', 'a')

print(file.writelines(["ahmed\n", "mohamed\n"]))
