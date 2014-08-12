# pyselection

Python program to read a text file and be able to select lines (the output is a text file with your selection)

  - INPUT : input text file
  - OUTPUT : your selected lines (output text file)

![Screenshot 1](http://github.com/sgaudart/pyselection/pyselection.png)

## Requirement

use the curses modules (please type help() and after modules to check)<BR>
use the xterm type console if case of linux environment.

## Usage

```erb
(python) pyselection.py file.txt
```

## Usefull Keys
  - UP/DOWN : navigate
  - SPACE : select/unselect the line
  - OTHER KEY : you can make a dynamic text filter
  - BACKSPACE : you delete one chr of the text filter
  - ENTER : save and exit
  - ESC : no save and exit
