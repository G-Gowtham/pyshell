
from getpass import getuser
from socket import gethostname
from os import getcwd
from termcolor import colored

def main():
    user_name = getuser()
    host_name = gethostname()
    directory = getcwd()
    while True:
        ps1 = f"{user_name}@{host_name} : {directory}$ "
        cmd = input(colored(ps1, 'green'))

if __name__ == "__main__":
    main()