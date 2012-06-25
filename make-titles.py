'''
MakeTitles

Makes prtl files from your subtitles.txt file in Subs folder.
Just import them to premiere, drop them in your sequence and fix the timing.

subtitles.txt - should be subtitles text seperated by 2 newlines (\n\n)

TitleExample.prtl - this title file you can redesign as you like, only
					make sure it still contains the text TO_REPLACE ("FirstLineSecondLine")



No rights reserved on this code unless required by law.

btw Version 2.0 will be able to take srt files and make an importable sequence!

works on Python 2.7 and Python 3.2
'''
import re
import os

# this is useful for RTL languages like hebrew, turn this to False for english.
REVERSE_TEXT = True

TEMPLATE = open("TitleExample.prtl", "rb").read()
TEMPLATE = TEMPLATE.decode('utf-16')
# this file should be unix format (only \n, not \r\n, because I split on \n\n)
SUBS_TEXT = open("Subtitles.txt", "rb").read().decode('utf-8')[1:]
FIRST_LINE_TO_REPLACE = 'FirstLine'
SECOND_LINE_TO_REPLACE = 'SecondLine'
OUTPUT_DIR = 'Subs'

def MakePrtlFile(textlines, fname):
    # premiere does newlines in a very strange fashion... So i just remove theme
    lines = textlines.strip().split('\n')
    firstLine = lines[0]
    if len(lines) > 1:
        secondLine = lines[1]
    else:
        secondLine = ''
        
    if REVERSE_TEXT:
        secondLine = secondLine[::-1]
        firstLine = firstLine[::-1]
        
    print(fname)
    # complicated unicode escaping for when printing  to an ascii terminal
    print(firstLine.encode('unicode_escape').decode('ascii'))
    print(secondLine.encode('unicode_escape').decode('ascii'))

    # RunCount is the amount of characters + 1, needs to be replaced or else premiere crashes
    runcountLineOne = 'RunCount="%d"' % (len(firstLine) + 1)
    runcountLineOneA = 'RunCountA="%d"' % (len(firstLine) + 1)
    runcountLineTwo = 'RunCount="%d"' % (len(secondLine) + 1)
    runcountLineTwoB = 'RunCountB="%d"' % (len(secondLine) + 1)
    newt = TEMPLATE.replace('RunCount="10"', runcountLineOneA)
    newt = newt.replace('RunCount="11"', runcountLineTwoB)
    newt = newt.replace(runcountLineOneA, runcountLineOne)
    newt = newt.replace(runcountLineTwoB, runcountLineTwo)
    

    newt = newt.replace(FIRST_LINE_TO_REPLACE, firstLine)
    newt = newt.replace(SECOND_LINE_TO_REPLACE, secondLine)    

    f = open(fname, "wb")

    # if we don't make the file in the correct encoding, premiere crahes.
    f.write(newt.encode('utf-16'))
    f.close()
    
def ParseSubsFile():
	subs = [x for x in SUBS_TEXT.split('#') if len(x) > 0]
	
	print(len(subs))
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)
	
	for i, text in enumerate(subs):
		num_id = "%04d" % i
		fname = "Title%s%s" % (num_id, ".prtl")
		fname = os.path.join(OUTPUT_DIR, fname)
		MakePrtlFile(text, fname)

ParseSubsFile()

