# python-unix-shell

## Shell features:
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