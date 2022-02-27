# curses library supplies a terminal-independent screen-painting and keyboard-handling facility for text-based terminals
import curses

# wrapper() takes a callable object and initializes the terminal
from curses import wrapper

# random module works as a pseudo-random number generator
import random

# provides various time-related functionalities
import time

# function to display the starting screen of the game which waits for the user to enter any key to proceed to the typing test
def start_screen(stdscr):
    # clear the terminal
    stdscr.clear()
    # add text to the terminal
    stdscr.addstr('WELCOME TO THE SPEED TYPING TEST!',curses.color_pair(3))        
    stdscr.addstr('\nPRESS ANY KEY TO PROCEED:')
    # refresh the terminal so that the text above is added and displayed
    stdscr.refresh()
    # ensures that the terminal does not close immediately
    stdscr.getkey()

# function to randomly select any line for the player to type
def get_text():
    # open the text file containing lines for the player to type
    f=open('Text.txt','r') 
    # returns a list of all the lines as strings
    lines=f.readlines()
    # closes the text file
    f.close()
    # function returns a random string from the given list of lines with all trailing spaces removed
    return random.choice(lines).strip()

# function to display text in the terminal
def display_text(stdscr,target,current,wpm=0):
    # adds the test string to the terminal
    stdscr.addstr(target)
    # displays the wpm in the next line which gets updated at each instant
    stdscr.addstr(f'\nWPM: {wpm}')
    # to check each character typed by the player
    for i,char in enumerate(current):     
        # display player typed text in green if it matches the character in the test string at that index
        if target[i]==char:
            # character added on line 0(1st) at index i, overlapping on the test string
            stdscr.addstr(0,i,char,curses.color_pair(1))
        # display player typed text in red if it does not match the character in the test string at that index
        else:
            # character added on line 0(1st) at index i, overlapping on the test string
            stdscr.addstr(0,i,char,curses.color_pair(2))

# function that calculates the wpm of the player, ends the game, checks and supplies the text typed by the player which is displayed in the terminal
def wpm_test(stdscr):
    # target_text contains the string to be typed by the player
    target_text=get_text()
    # stores the text typed by the player
    current_text=[]
    # variable containing the wpm, initialized as 0
    wpm=0
    # start_time contains the time when the test is started
    start_time=time.time()
    # ensures that the wpm decreases if the player stops typing while the test is ongoing
    stdscr.nodelay(True)  
    # to update calculations and displayed text in each instant
    while True:
        # id max(...) is not given then just as the time starts (when time_elapsed is 0) wpm throws a ZeroDivisionError 
        time_elapsed=max(time.time()-start_time,1)
        # claculates wpm upto the nearest integer
        wpm=round(((len(current_text)/time_elapsed)*60)/5) 
        #removes the text displayed on the terminal in the start screen
        stdscr.clear()
        # display the test string and text typed by player in the appropriate color and wpm at that instant
        display_text(stdscr,target_text,current_text,wpm)
        # refresh the terminal to display the text typed and wpm as calculated
        stdscr.refresh()
        # stdscr.nodelay(True) throws an exception on any delay in the player typing
        try: 
            # catch the exception thrown by nodelay                              
            key=stdscr.getkey()
        except:
            # ensures that the player can type at their own pace without throwing exceptions and the wpm decreases with pauses
            continue
        # in case that the player presses the esc key (ASCII value is 27) the game is exited
        if ord(key)==27:
            break
        # in case esc key is not pressed
        if key in ('KEY_BACKSPACE','\b','\x7f'):
            # in case that the key pressed is backspace, check that the text typed by the player has at least 1 character, else skip
            if len(current_text)>0:
                current_text.pop()
        # in case the key pressed is not backspace and typed text does not exceed the test string
        elif len(target_text)>len(current_text):
            # key pressed is added to current_text which will be displayed on terminal in appropriate color
            current_text.append(key)
        # in case that typed text matches the test string exactly
        if ''.join(current_text)==target_text:  
            # ensures that the wpm does not decrease when the player stops typing
            stdscr.nodelay(False)
            # end the test
            break

# callable function which executes all the functions to play the game
def main(stdscr):
    # green text to denote that the text typed is correct
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    # red text to denote that the text typed is wrong
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    # white text for anything not typed by the player
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
    # function to display the start screen on the terminal
    start_screen(stdscr)
    # to run the game as long as esc key is not pressed to quit the game
    while True:  
        # function to calculate wpm and display the typed text in appropriate colors along with it
        wpm_test(stdscr)
        # if the test is completed, display text on line 3(4th) on index 0
        stdscr.addstr(3,0,'You have completed this game. Press any key to play again:')
        # refresh the terminal so that the text above is added and displayed
        stdscr.refresh() 
        # obtain a key pressed by the user after test has ended
        key=stdscr.getkey()
        # in case that esc key (ASCII value is 27) is pressed
        if ord(key)==27:
            # break the loop to quit the game
                break

# function that takes a callable object and initializes the terminal for it
wrapper(main)   
