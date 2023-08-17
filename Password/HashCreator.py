from hashlib import md5

while 1:
    hs = md5("".join(input("Enter Password: ")).encode()).hexdigest()
    print("Hash:", hs)
