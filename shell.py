"""
Features:
    * Up and down arrows can used to navigate across history of commands 
    * Tab can be used for file name auto-completion 
    * Supports redirection and pipes use space between commands for redirection and pipes
        Example-1: 
            valid syntax => ls | wc 
            In valid syntax  => ls|wc

        Example-2: 
            valid syntax => ls > wc 
            In valid syntax  => ls>wc
        
        Example-3: 
            valid syntax => ls 2> wc 
            In valid syntax  => ls 2>wc
        
        Example-4: 
            valid syntax => wc < test.txt
            In valid syntax  => wc<test.txt
        
"""

from getpass import getuser
from socket import gethostname
from os import getcwd
from termcolor import colored
from os.path import expanduser, exists
import subprocess
import readline, glob
import argparse
import shlex
import sys

def tab_auto_completion():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete_line)

def get_ps1():
    user_name = getuser()
    host_name = gethostname()
    directory = getcwd()
    ps1 = f"{user_name}@{host_name} : {directory}$ "  #ps1 => primary prompt variable
    return ps1

def complete_line(text, state):
    return (glob.glob(text+'*')+[None])[state]

def execute(cmd, stdin, stdout, stderr):
    
    try:
        p = subprocess.Popen(shlex.split(cmd), stdin = stdin, stdout = stdout, stderr = stderr)
        return p
    except FileNotFoundError as e:
        print(colored(f"Please check the command: {cmd}", "red"))

def redirect_out(symbol, location, p): # '>'
    out = p.stdout
    mode = "w"
    location = expanduser(location)
    if symbol.endswith(">>"):
        mode = "a"

    if (len(symbol) == 2 or len(symbol) == 3) and ord(symbol[0]) == 50:
        if p.stderr:
            out = p.stderr

    with open(location, mode) as f:
        for line in iter(out.readline, b''):
            f.write(line.decode())

def redirect_in(cmd): # '<'
    if "<" not in cmd.split():
        return cmd

    command, file_name = cmd.rsplit('<',1)
    file_name =  expanduser(file_name)
    
    return f"cat {file_name} | {command}"

def execute_redirection(symbol, location, cmd_output):
    if symbol.endswith(">"):
        redirect_out(symbol, location, cmd_output)

    return {"returncode": 0, 'stdout': "", 'stdin': ""}

def pre_loop(histfile):
    if readline and exists(histfile):
            readline.read_history_file(histfile)

def post_loop(histfile, histfile_size):
    if readline:
        readline.write_history_file(histfile)
        
def custom_parser(cmd):
    cmd_list = []
    tmp = ""
    raw_execution = 1

    for word in cmd.split():
        if word == '|' or word.endswith(">") or  word.endswith("<"):
            cmd_list.append(tmp)
            cmd_list.append(word)
            tmp = ""
            raw_execution = 0

        else:
            tmp = tmp + " " + word

    if tmp != "":
        cmd_list.append(tmp)

    return raw_execution, cmd_list

def shell():

    ps1 = get_ps1()
    #for history
    histfile = expanduser('~/.py_unix_shell_history')
    histfile_size = 1000

    #for tab auto completion
    tab_auto_completion()

    while True:
        pre_loop(histfile)
        cmd = input(colored(ps1,"blue")).strip()
        
        if cmd == "exit":
                break
        
        cmd = redirect_in(cmd)
        raw_execution, cmd_list = custom_parser(cmd)

        if raw_execution:
            p = execute(cmd, sys.stdin, sys.stdout, sys.stderr)
            if p:
                p.wait()
            continue

        pipe_check = 0
        redirect_check = 0
        redirect_symbol = ""

        for i, word in enumerate(cmd_list):
            if word == "|":
                pipe_check = 1
                continue
            elif word.endswith(">") or word.endswith(">>"):
                redirect_symbol = word
                redirect_check = 1
                continue
            
            if pipe_check == 1:
                if i == len(cmd_list)-1:
                    p = execute(word, p.stdout, sys.stdout, sys.stderr)
                else:
                    p = execute(word, p.stdout, subprocess.PIPE, subprocess.PIPE)
                pipe_check = 0

            elif redirect_check == 1:
                redirect_out(redirect_symbol, word, p)
                redirect_check = 0
                redirect_symbol = ""
            else:
                p = execute(word, None, subprocess.PIPE, subprocess.PIPE)

            if p:
                p.wait()

        post_loop(histfile, histfile_size)

def main():
    shell()

if __name__ == "__main__":
    main()
    
