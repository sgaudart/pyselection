#!/usr/bin/env python
# https://github.com/sgaudart/pyselection

import curses
import sys

window_height=25 # curses window's lines 25
window_larger=80 # curses window's rows 75

# reading the text file
f = open(sys.argv[1],'r')
text = f.readlines()
totalline = len(text)
f.close()

filtertext = []
prefix = [' '] * (totalline) # ' '=no selection '*'=selection

curses.initscr()
win = curses.newwin(window_height,window_larger,0,0) # line, row, coord X,Y
#curses.noecho() # impact ?
curses.curs_set(2) # show the cursor
curses.start_color()
win.border(0)
win.keypad(1) # you can use special keys like KEY_UP...
win.nodelay(1) # If yes is 1, getch() will be non-blocking
#curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_GREEN)

def ShowText(line) : # show the text file in the current curses windows
	if filterflag == 0 : # no filter
		for i in range(0,window_height-2) : # we can show more than window_height
			if i < len(text) : # small text
				win.addstr(i+1,1,"[" + prefix[line+i] + "] " + text[line+i][0:window_larger-8])
			else :
				win.addstr(i+1,1,"")
		
	else : # filter mode
		for i in range(0,window_height-2) : # we can show more than window_height
			if i < len(filtertext) : # small text
				win.addstr(i+1,1,"[" + prefix[filtertext[line+i]] + "] " + text[filtertext[line+i]][0:window_larger-8])
			else :
				win.addstr(i+1,1,"\n")

def ShowBorder() : # show the border
	win.border(0)
	win.addstr(0, 2, str(sys.argv[1])) # show the name of the file
	if filterflag == 0 : # no filter
		win.addstr(0, 33, "LINE="+str(fline+1).zfill(4)+"/"+str(totalline).zfill(4)) # show fline
	else : # filter mode
		win.addstr(0, 33, "LINE="+str(fline+1).zfill(4)+"/"+str(len(filtertext)).zfill(4)) # affichage de fline
	win.addstr(window_height-1, 2, "FILTER="+filterstring) # affichage de filterflag


def markLine(cline, line) : # mark the line with the chr "*"
	if filterflag == 0 : # no filter
		if prefix[line] == ' ':
			prefix[line]='*'
		else :
			prefix[line]=' '
		win.addstr(cline+1,2,prefix[line])

	else : # filter mode
		if prefix[filtertext[line]] == ' ':
			prefix[filtertext[line]]='*'
		else :
			prefix[filtertext[line]]=' '
		win.addstr(cline+1,2,prefix[filtertext[line]])


def WriteResultFile () :
	resultfile = open(sys.argv[1] + ".selection", "w")
	for i in range(0,totalline) :
		if prefix[i] == '*' :
			resultfile.write(text[i])
	resultfile.close()

def MoveCursor (offset) :
	global cline
	global fline
	
	cline=cline+offset
	fline=fline+offset
	
	# check if border exceeding ?
	if fline < 0 : # top of the file
		fline = 0
		cline = 0
	if cline < 0 : # top of the cursor + move the windows
		cline=0
		ShowText(fline)
		ShowBorder()
	
	if filterflag == 0 : # no filter
		if fline > len(text)-1 : # end of the file (no scroll)
			fline=len(text)-1
			cline=len(text)-1
		win.addstr(0, 33, "LINE="+str(fline+1).zfill(4)+"/"+str(totalline).zfill(4)) # affichage de fline
	else : # filter mode
		if fline > len(filtertext)-1 : # end of the file (no scroll)
			fline=len(filtertext)-1
			cline=len(filtertext)-1
		win.addstr(0, 33, "LINE="+str(fline+1).zfill(4)+"/"+str(len(filtertext)).zfill(4)) # affichage de fline
	if cline > window_height-3 : # bottom of the cursor
			cline=window_height-3
			ShowText(fline-window_height+3)
			ShowBorder()

	win.move(cline+1, 2)
	win.refresh() # on affiche tout

def CreateFilterTab(filter) :
	global filtertext 
	filtertext = [] # init filtertext
	for i in range(0,totalline) :
		if filter in text[i] :
			filtertext.append(i)
	

cline=0  # line number for the cursor (0= first line)
fline=0  # line number inside the text file (0= first line)
filterflag = 0 # flag for the filtering function
filterstring = "" # the filter string

ShowText(fline) # show text
ShowBorder() # show border
win.move(cline+1, 2)

while 1: # main loop	
	
	key = win.getch() # which key ?
	
	if key == 27: break # if ESC key => quit only (option : reset the filter ?)
	
	if key == 10: # if ENTER key => make the result file
		WriteResultFile()
		break 

	if key in range(33,126) : # set the filter function (ascii 33 => 126)
		fline=0 # init 
		cline=0 # init
		filterstring = filterstring + chr(key) # add the chr
		CreateFilterTab(filterstring)
		filterflag = len(filterstring)
		ShowText(fline)
		ShowBorder() # show border
		win.move(cline+1, 2)
		win.refresh() # on affiche tout
	
	if key == 8 : # BACKSPACE key
		fline=0 # init 
		cline=0 # init
		filterstring = filterstring[:-1] # drop the last chr
		CreateFilterTab(filterstring)
		filterflag = len(filterstring)
		ShowText(fline)
		ShowBorder() # show border
		win.move(cline+1, 2)
		win.refresh() # on affiche tout
		
	if key == 32: # SPACE key => mark the line
		markLine(cline,fline)
		MoveCursor(1) # after space, move down automatically
	
	if key == curses.KEY_UP : MoveCursor(-1)
	
	if key == curses.KEY_DOWN : MoveCursor(1)
	
	if key == curses.KEY_PPAGE : MoveCursor(-window_height+3) # PAGE UP key => move one page up
	
	if key == curses.KEY_NPAGE : MoveCursor(window_height-3) # PAGE DOWN key => move one page down
