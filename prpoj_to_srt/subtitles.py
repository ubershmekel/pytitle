'''
subtitles.py

This module can generate subtitle files from a list of titles and intervals.

usage:
    import subtitles
    titles = [(0, 3, 'hi'), (6, 7, 'GET DOWN!'), (10, 13.5, 'I need a vacation')]
    subformat = subtitles.SubRip()
    subs = subformat.render([titles])
    open('whatever' + subformat.extension, 'w').write(subs)
'''

import os
import datetime

def time_format(seconds, msec_sep='.'):
    '''
    Converts an amount of seconds into
        Hours:Minutes:Seconds.milliseconds
    and the milliseconds can have whatever separator you like. You crazy you.
    '''
    delta = datetime.timedelta(seconds=seconds)
    milliseconds = int(delta.microseconds / 1000)
    minutes, seconds = divmod(delta.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    text = "%s:%s:%s%s%s" % (hours, minutes, seconds, msec_sep, milliseconds)
    return text

class SubtitleFormat:
    extension = ''
    def prefix(self):
        return ''
    def title(self, time_in, time_out, text):
        raise NotImplementedError
    def render(self, titles_list):
        text_list = [self.prefix()]
        
        for time_in, time_out, title_text in titles_list:
            text_list.append(self.title(time_in, time_out, title_text))
        
        return ''.join(text_list)
    

class SubRip(SubtitleFormat):
    extension = '.srt'
    def title(self, time_in, time_out, text):
        return '%s --> %s\n%s\n\n' % (time_format(time_in, msec_sep=','), time_format(time_out, msec_sep=','), text)
        
        

class SubViewer(SubtitleFormat):
    extension = '.sub'
    def prefix(self):
        return '''[INFORMATION]
[TITLE]
[AUTHOR]
[SOURCE]
[PRG]
[FILEPATH]
[DELAY]0
[CD TRACK]0
[COMMENT]
[END INFORMATION]
[SUBTITLE]
[COLF]
'''
    def title(self, time_in, time_out, text):
        return '%s,%s\n%s\n\n' % (time_format(time_in), time_format(time_out), text)

class Youtube(SubtitleFormat):
    extension = '.sbv'
    def title(self, time_in, time_out, text):
        return '%s,%s\n%s\n\n' % (time_format(time_in), time_format(time_out), text)


FORMATS = [Youtube, SubViewer, SubRip]
EXTENSIONS = {fmt.extension: fmt for fmt in FORMATS}

def subs_from_fname(fname):
    extension = os.path.splitext(fname)[1]
    # get rid of the dot
    return EXTENSIONS[extension]()
            