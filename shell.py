"""
Features:
    * Up and down arrows can used to navigate across history of commands 
    * Tab can be used for file auto-completion 
"""

from getpass import getuser
from socket import gethostname
from os import getcwd
from termcolor import colored
from os.path import expanduser, exists
import subprocess
import readline, glob
import argparse

def get_ps1():
    user_name = getuser()
    host_name = gethostname()
    directory = getcwd()
    ps1 = f"{user_name}@{host_name} : {directory}$ "  #ps1 => primary prompt variable
    return ps1

def interactive():
    ps1 = get_ps1()
    cmd = f"/bin/bash --init-file shell-init.sh"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell= True)

    for line in iter(p.stdout.readline, b''):
        print(line.decode(), end="")
    p.stdout.close()
    p.wait()



def complete_line(text, state):
    return (glob.glob(text+'*')+[None])[state]


def execute_cmd(cmd):
    cmd_output = subprocess.run(cmd, shell= True, capture_output= True, text= True)
    return cmd_output

def pre_loop(histfile):
    if readline and exists(histfile):
            readline.read_history_file(histfile)

def post_loop(histfile, histfile_size):
    if readline:
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)

def parse_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--non-interactive", help="Used to run commands in Non-Interative mode", action="store_true")
    args = parser.parse_args()
    return args

def non_interactive():

    ps1 = get_ps1()
    #for history
    histfile = expanduser('~/.py_unix_shell_history')
    histfile_size = 1000

    #for tab auto completion
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_line)

    while True:
        pre_loop(histfile)

        cmd = input(colored(ps1,"blue")).strip()
        if cmd == "exit":
            break

        cmd_output = execute_cmd(cmd)

        if cmd_output.returncode:
            print(colored(cmd_output.stderr,"red"), end="")
        else:
            print(cmd_output.stdout, end="")

        post_loop(histfile, histfile_size)

def main():
    args = parse_inputs()
    mode = args.non_interactive

    if mode:
        non_interactive()
    else:
        interactive()

if __name__ == "__main__":
    main()
    
