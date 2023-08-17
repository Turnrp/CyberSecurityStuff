from random import randint
from time import sleep

characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
characterslist = []
for i in characters:
    characterslist.append(i)

filename = input(f"Input File Name:\n")
print("This will be put in the directory of the .py file.")
replaces = ""
while 1:
    choice = input(f"Input Character Blacklists: (no to exit)\n")
    if choice == "no":
        break
    elif len(choice) == 1 and choice not in replaces:
        replaces += choice
    else:
        print("try again")

for i in replaces:
    characterslist.remove(i)

while 1:
    try:
        filelength = int(input(f"Input Password Lenght:\n"))
        break
    except :
        print("Invalid Response (USE A INTEGER)")

with open(filename, "w") as file:
    for i in range(0, filelength):
        file.write(characterslist[randint(0, len(characterslist) - 1)])
print("Password Created.")
sleep(1)