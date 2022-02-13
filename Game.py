#importing required modules

import curses
import random
import time
from curses import wrapper

#The curses library supplies a terminal-independent screen-painting and keyboard-handling facility for text-based terminals

#The wrapper() function takes a callable object and initializes the terminal




def start_screen(stdscr):

    stdscr.clear()

    stdscr.addstr('WELCOME TO THE SPEED TYPING TEST!',curses.color_pair(3))        
    stdscr.addstr('\nPRESS ANY KEY TO PROCEED:')

    stdscr.refresh()                   #applies changes

    stdscr.getkey()                    #if not given the window closes instantaneously

#displays the statrt screen


def get_text():

    f=open('Text.txt','r') 
    lines=f.readlines()
    f.close()

    return random.choice(lines).strip()

#returns a random piece of text from the Text.txt


def display_text(stdscr,target,current,wpm=0):

    stdscr.addstr(target)
    
    stdscr.addstr(f'\nWPM: {wpm}')
    
    for i,char in enumerate(current):                 #enumerate(<sequence>) returns both index and element

        if target[i]==char:
            stdscr.addstr(0,i,char,curses.color_pair(1))
        else:
            stdscr.addstr(0,i,char,curses.color_pair(2))

#displays the typed text over the target text

def wpm_test(stdscr):

    target_text=get_text()
    current_text=[]
    wpm=0
    start_time=time.time()
    
    stdscr.nodelay(True)            #ensures that the wpm decreases if the typist stops in between typing

    while True:
        
        time_elapsed=max(time.time()-start_time,1)
        wpm=round(((len(current_text)/time_elapsed)*60)/5)          #characters per minute/5=words per minute

        stdscr.clear()

        display_text(stdscr,target_text,current_text,wpm)

        stdscr.refresh()

        if ''.join(current_text)==target_text:                      #break the loop when all text has been typed correctly
            stdscr.nodelay(False)
            break

        try:                                #nodelay throws an exception if there is any delay in typing
            key=stdscr.getkey()
        except:
            continue

        if ord(key)==27:                       #ASCII value of esc key is 27
            break

        if key in ('KEY_BACKSPACE','\b','\x7f'):    #ensures thst typed characters are removed 
            if len(current_text)>0:
                current_text.pop()
        elif len(target_text)>len(current_text):    #stops the text typed from exceeding the given text
            current_text.append(key)

#calculate wpm, get and check the key typed by the user


def main(stdscr):

    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)   #define a foreground-background pair and reference it to an integer
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:                         #run the game as long as esc key or some other key is pressed

        wpm_test(stdscr)

        stdscr.addstr(3,0,'You have completed this game. Press any key to play again:')
        stdscr.refresh() 

        try:
            key=stdscr.getkey()
            if ord(key)==27:
                    break
        except:
            break
            
#main callable function to start the game


wrapper(main)                 #initialize the terminal for the game
