# python-unix-shell

## Installation:
    git clone https://github.com/G-Gowtham/python-unix-shell.git
    cd pyshell
    pip3 install .

## Usage:
    python3 -m pyshell
## Shell features:
  * Up and down arrows can used to navigate across history of commands 
  * Tab can be used for file name auto-completion 
  * Supports redirection and pipes use space between commands for redirection and pipes<br><br>
  
    Example-1:<br>
        In valid syntax  => ls|wc<br>
        valid syntax => ls | wc <br><br>

    Example-2: <br>
        In valid syntax  => ls>wc <br>
        valid syntax => ls > wc <br><br>

    Example-3: <br>
        valid syntax => ls 2> wc <br>
        In valid syntax  => ls 2>wc <br><br>

    Example-4: <br> 
        In valid syntax  => wc<test.txt \
        valid syntax => wc < test.txt <br><br>

  * If you not redirecting or pipeing but still want to use "|", ">" operators with spaces escape it, this may leads to value error <br><br>
      Example-1:<br>
          In valid syntax  => echo "< html >"<br>
          valid => echo "< html />"<br><br>
      Example-2:<br>
          In valid syntax  => echo " | "<br>
          valid => echo " \| "

## Phases:
  ### System calls:
  * https://www.youtube.com/watch?v=lhToWeuWWfw
  * https://www.youtube.com/watch?v=EavqupVh8ls
  * https://www.youtube.com/watch?v=IFEFVXvjiHY => fork & exec
  * https://www.youtube.com/watch?v=IIiKVaxHCX0 => os and subprocess libray
  * https://www.youtube.com/watch?v=2Fp1N6dof0Y => subprocess libray

  ### References:
  * https://stackoverflow.com/questions/59627995/is-there-a-python-3-native-equivalent-to-invoking-the-script-with-rlwrap
  * https://stackoverflow.com/questions/6656819/filepath-autocompletion-using-users-input/6657975
  * https://stackoverflow.com/questions/39495024/persistent-history-in-python-cmd-module
  * https://stackoverflow.com/questions/57955127/run-bash-script-with-live-output-in-a-python-script
  * https://dzone.com/articles/interacting-with-a-long-running-child-process-in-p
  * https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
  * https://serverfault.com/questions/59262/bash-print-stderr-in-red-color
  * https://stackoverflow.com/questions/163542/how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument


# <i>mould</i> - A minimalistic templating engine for Python

This Python library helps to render HTML pages and plain text  with variable substitutions, if conditions and for loops.


## Templating syntax :

## To delcare variables enclose the variable name with '{{' and '}}'

    Hello {{ text }} -- 'text' is the variable here

You can use the same syntax to write variable expressions.

    This is line number {{ n+10 }}
