from sys import argv
from os import rename
from os.path import curdir


def StartDeploy(file: str):
    print("Moving File..")
    osName = (
        "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\" + file
    )

    rename(
        file,
        osName,
    )
    print(
        "Moved to",
        osName,
    )


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage BasicStartupDeployer.py <FILE>")
    else:
        StartDeploy(argv[1])
