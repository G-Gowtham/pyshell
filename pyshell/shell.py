"""
Features:
    * Up and down arrows can used to navigate across history of commands 
    * Tab can be used for file name auto-completion 
    * Supports redirection and pipes use space between commands for redirection and pipes
        Example-1: 
            In valid syntax  => ls|wc
            valid syntax => ls | wc 
            

        Example-2: 
            In valid syntax  => ls>wc
            valid syntax => ls > wc 
            
        
        Example-3: 
            In valid syntax  => ls 2>wc
            valid syntax => ls 2> wc 
            
        Example-4: 
            In valid syntax  => wc<test.txt
            valid syntax => wc < test.txt
            

    * If you not redirecting or pipeing but still want to use "|", ">" operators with spaces escape it, this may leads to value error
        Example-1:
            In valid syntax  => echo "< html >"
            valid => echo "< html />"
        Example-2:
            In valid syntax  => echo " | "
            valid => echo " \| "
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

def execute(raw_cmd, cmd, stdin, stdout, stderr):
    
    try:
        p = subprocess.Popen(shlex.split(cmd), stdin = stdin, stdout = stdout, stderr = stderr)
        return p
    except (FileNotFoundError, ValueError, IndexError) as e:
        print(colored(f"Please check the command: {raw_cmd}\nERROR: {e}", "red"))

def redirect_out(symbol, location, p): # '>'

    if not p:
        return

    out = p.stdout
    mode = "w"
    location = expanduser(location)
    if symbol.endswith(">>"):
        mode = "a"

    if (len(symbol) == 2 or len(symbol) == 3) and ord(symbol[0]) == 50:
        if p.stderr:
            out = p.stderr
    try:
        with open(location, mode) as f:
            for line in iter(out.readline, b''):
                f.write(line.decode())
    except FileNotFoundError as e:
        print(colored(f"ERROR FileNotFoundError: {e}", "red"))

def redirect_in(cmd): # '<'
    if "<" not in cmd.split():
        return cmd

    
    command, file_name = cmd.rsplit('<',1)

    if cmd and file_name:
        file_name =  expanduser(file_name)
        return f"cat {file_name} | {command}"
    return cmd

def execute_redirection(symbol, location, cmd_output):
    if symbol.endswith(">"):
        redirect_out(symbol, location, cmd_output)

    return {"returncode": 0, 'stdout': "", 'stdin': ""}

def pre_loop(histfile):
    if readline:
            readline.read_history_file(histfile)

def post_loop(histfile, histfile_size):
    if readline:
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)
        
def custom_parser(cmd):
    cmd_list = []
    tmp = ""
    raw_execution = 1

    for i,word in enumerate(cmd.split()):
        if word == '|' or (word.endswith(">") and len(word)<4 and '\\' not in word):
            cmd_list.append(tmp)
            cmd_list.append(word)
            tmp = ""
            raw_execution = 0

        else:
            word = word.replace("\>",">")
            word = word.replace("\|","|")
            tmp = tmp + " " + word

    if tmp != "":
        cmd_list.append(tmp)

    return raw_execution, cmd_list

def shell():

    ps1 = get_ps1()
    #for history
    histfile = expanduser('~/.py_unix_shell_history')
    if not exists(histfile):
        with open(histfile, "w+") as f:
            pass
    histfile_size = 1000

    #for tab auto completion
    tab_auto_completion()

    while True:
        pre_loop(histfile)
        cmd = input(colored(ps1,"blue")).strip()
        
        if cmd == "exit":
                break
        
        if cmd.strip() == "":
            continue

        raw_cmd = cmd
        cmd = redirect_in(cmd)
        raw_execution, cmd_list = custom_parser(cmd)
        #print(cmd_list)

        if raw_execution:
            p = execute(raw_cmd, cmd_list[0], sys.stdin, sys.stdout, sys.stderr)
            if p:
                p.wait()
            continue

        pipe_check = 0
        redirect_check = 0
        redirect_symbol = ""
        p = None

        for i, line in enumerate(cmd_list):
            if line == "|":
                pipe_check = 1
                continue
            elif line.endswith(">") or line.endswith(">>"):
                redirect_symbol = line
                redirect_check = 1
                continue
            
            if pipe_check == 1:
                if not p:
                    break
                if i == len(cmd_list)-1:
                    p = execute(raw_cmd, line, p.stdout, sys.stdout, sys.stderr)
                else:
                    p = execute(raw_cmd, line, p.stdout, subprocess.PIPE, subprocess.PIPE)
                pipe_check = 0

            elif redirect_check == 1:
                redirect_out(redirect_symbol, line, p)
                redirect_check = 0
                redirect_symbol = ""
            else:
                p = execute(raw_cmd, line, None, subprocess.PIPE, subprocess.PIPE)

            if p:
                p.wait()

        post_loop(histfile, histfile_size)

def main():
    shell()

if __name__ == "__main__":
    main()
    