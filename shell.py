
from getpass import getuser

def main():
    user = getuser()

    while True:
        cmd = input(f"{user}@ >>>")

if __name__ == "__main__":
    main()