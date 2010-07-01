'''
MakeTitles

Makes prtl files from your subtitles.txt file in Subs folder.
Just import them to premiere, drop them in your sequence and fix the timing.

subtitles.txt - should be subtitles text seperated by 2 newlines (\n\n)

TitleExample.prtl - this title file you can redesign as you like, only
					make sure it still contains the text TO_REPLACE ("FirstLineSecondLine")



No rights reserved on this code unless required by law.

btw Version 2.0 will be able to take srt files and make an importable sequence!
'''
import re

TEMPLATE = open("TitleExample.prtl").read()
TEMPLATE = TEMPLATE.decode('utf-16')
# this file should be unix format (only \n, not \r\n, because I split on \n\n)
SUBS_TEXT = open("Subtitles.txt").read().decode('utf-8')[1:]
FIRST_LINE_TO_REPLACE = u'FirstLine'
SECOND_LINE_TO_REPLACE = u'SecondLine'

def MakePrtlFile(textlines, fname):
    # premiere does newlines in a very strange fashion... So i just remove theme
    lines = textlines.strip().split('\n')
    firstLine = lines[0][::-1]
    if len(lines) > 1:
        secondLine = lines[1][::-1]
    else:
        secondLine = u''
    print fname
    print repr(firstLine)
    print repr(secondLine)

##	textlines = "\n".join([line[::-1] for line in textlines.split('\n')])
##
##	parsedline = textlines.replace(u'\r\n', u' ')
##	parsedline = parsedline.replace(u'\n', u' ')
##	print repr(parsedline)
    
    
    # This is the amount of characters + 1, needs to be replaced or else premiere crashes
    runcountLineOne = u'RunCount="%d"' % (len(firstLine) + 1)
    runcountLineOneA = u'RunCountA="%d"' % (len(firstLine) + 1)
    runcountLineTwo = u'RunCount="%d"' % (len(secondLine) + 1)
    runcountLineTwoB = u'RunCountB="%d"' % (len(secondLine) + 1)
    newt = TEMPLATE.replace(u'RunCount="10"', runcountLineOneA)
    newt = newt.replace(u'RunCount="11"', runcountLineTwoB)
    newt = newt.replace(runcountLineOneA, runcountLineOne)
    newt = newt.replace(runcountLineTwoB, runcountLineTwo)
    

    newt = newt.replace(FIRST_LINE_TO_REPLACE, firstLine)
    newt = newt.replace(SECOND_LINE_TO_REPLACE, secondLine)    

    f = open(fname, "w")

    # if we don't make the file in the correct encoding, premiere crahes.
    f.write(newt.encode('utf-16'))
    f.close()
    
def ParseSubsFile():
	subs = [x for x in SUBS_TEXT.split('#') if len(x) > 0]
	
	print len(subs)
	for i, text in enumerate(subs):
		num_id = "%04d" % i
		fname = "Subs\\Title%s%s" % (num_id, ".prtl")
		MakePrtlFile(text, fname)

ParseSubsFile()

