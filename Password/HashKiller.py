from hashlib import md5
from string import ascii_lowercase, ascii_uppercase, digits
from itertools import combinations

# Custom alphabet with lowercase letters, uppercase letters, numbers, and some punctuation symbols
alphabet = list(ascii_lowercase + ascii_uppercase + digits + "!@#$%^&*().")

length = 1


def BruteForce(hash, pIteration):
    global length
    for combination in combinations(alphabet, length):
        hs = md5("".join(combination).encode()).hexdigest()
        if pIteration:
            print(hs, "->", "".join(combination), length)
        if hs == hash:
            return "".join(combination)
    length += 1
    return BruteForce(hash, pIteration)


def File(hash, file, pIteration):
    with open(file, "r") as f:
        comb = file.read().splitlines()
    for i in comb:
        hs = md5("".join(i).encode()).hexdigest()
        if pIteration:
            print(hs, "->", "".join(i), length)
        if hs == hash:
            return "".join(i)
    return False


while 1:
    Hash = input("Enter Hash: ")
    Mode = input("Brute Force or File? ")
    Print = "y" in input("Print every iteration? ").lower()
    StartLength = input("Starting Lenght: ")

    if "b" in Mode.lower():
        # Brute Force It
        length = int(StartLength)
        password = BruteForce(Hash, Print)
        input("Password Cracked: " + password)
    elif "f" in Mode.lower():
        file = input("File: ")
        password = File(Hash, file, Print)
        if password:
            input("Password Cracked: " + password)
        else:
            input("Password Not Cracked.")
    else:
        input("Sorry", Mode, "is not a mode.")
