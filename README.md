# pyselection

Python program to read a text file and be able to select lines (the output is a text file with your selection)

  - INPUT : text file
  - OUTPUT : text file with your selected lines

![Screenshot 1](https://raw.githubusercontent.com/sgaudart/pyselection/master/pyselection.png)

## Requirement

  - Python 2.7 (run perhaps for Python 3.X)
  - curses module (please type help() and after modules to check)
  - use the XTERM type console in case of linux environment

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
