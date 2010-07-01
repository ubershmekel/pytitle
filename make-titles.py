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


TEMPLATE = open("TitleExample.prtl").read()
TEMPLATE = TEMPLATE.decode('utf-16')
# this file should be unix format (only \n, not \r\n, because I split on \n\n)
SUBS_TEXT = open("Subtitles.txt").read()
TO_REPLACE = u'FirstLineSecondLine'

def MakePrtlFile(textlines, fname):
	# premiere does newlines in a very strange fashion... So i just remove theme
	parsedline = textlines.replace(u'\r\n', u' ')
	parsedline = parsedline.replace(u'\n', u' ')
	
	newt = TEMPLATE.replace(TO_REPLACE, parsedline)
	
	# This is the amount of characters + 1, needs to be replaced or else premiere crashes
	runcount = u'RunCount="%d"' % (len(parsedline) + 1)
	newt = newt.replace(u'RunCount="20"', runcount)
	
	f = open(fname, "w")
	
	# if we don't make the file in the correct encoding, premiere crahes.
	f.write(newt.encode('utf-16'))
	f.close()

def ParseSubsFile():
	subs = []
	current_lines = []
	subs = SUBS_TEXT.split('\n\n')
	
	print len(subs)
	for i, text in enumerate(subs):
		num_id = "%04d" % i
		fname = "Subs\\Title%s%s" % (num_id, ".prtl")
		MakePrtlFile(text, fname)

ParseSubsFile()

