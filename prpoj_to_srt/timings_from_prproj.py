#coding: utf-8
'''
timings_from_prproj.py takes a prproj file that has one sequence full of titles
and outputs the in and out times of each title.

This can be useful if you made subtitles using adobe premiere and
want to convert the subtitles to srt or sub files.

usage examples:
    python prproj2subs.py mymovie.prproj subsfname.srt
    python prproj2subs.py mymovie.prproj subsfname.sbv
    python prproj2subs.py mymovie.prproj subsfname.sub


written for python 3
'''

from __future__ import division
from __future__ import unicode_literals
import sys
import string
import re
import pprint
import base64
import zlib
import subtitles

SEQUENCE_FRAMERATE = 25
OFFSET = 22.5
HEBREW = True

def get_framerate(prproj):
    rate_match = next(re.finditer(r'<FrameRate>(\d+)</FrameRate>', prproj))
    number_str = rate_match.groups()[0]
    return int(number_str) * SEQUENCE_FRAMERATE

#<ClipTrackItem
#<SubClip ObjectRef="472"/>
####<Name>Title0006</Name>
#<MasterClip ObjectURef="3f2accc0-0b7d-47cf-9573-c0eec351abb1"/>

#<VideoClip ObjectID="331"

#<SubClip ObjectRef="472"/>
#<Clip ObjectRef="473"/>
#<Source ObjectRef="333"/>
#<VideoMediaSource ObjectID="333"
#<Media ObjectURef="b1614fd9-0069-4d30-b4fb-f3dfc160032f"/>
#<Media ObjectUID="b1614fd9-0069-4d30-b4fb-f3dfc160032f"
#<ImporterPrefs Encoding="base64" Checksum="36924910">AQAA...

#<ImporterPrefs
#</ImporterPrefs>

#<ClipTrackItem Version="4">.*?</ClipTrackItem>

TITLES = {}

def get_info(cliptrack, prproj):
    #import pdb;pdb.set_trace()
    times_str = re.findall(r'<End>(\d+)</End>\s+<Start>(\d+)</Start>', cliptrack)
    out_time, in_time = times_str[0]
    #if '0' == in_time:
    #    continue
    start, end = int(in_time), int(out_time)
    
    obj_ref = re.search(r'<SubClip ObjectRef="(\d+)"/>', cliptrack).groups()[0]
    
    subclip_re = r'<SubClip ObjectID="%s"(.*?)</SubClip>' % obj_ref
    subclip = re.search(subclip_re, prproj, re.DOTALL).groups()[0]

    #title_name = re.findall(r'<Name>(\w+)</Name>', subclip)[0]
    #title_lines = TITLES[title_name]
    
    clip_id = re.search(r'<Clip ObjectRef="(\d+)"/>', subclip).groups()[0]
    
    video_clip = re.search(r'<VideoClip ObjectID="%s"(.*?)</VideoClip>' % clip_id, prproj, re.DOTALL).groups()[0]
    
    object_id = re.search(r'<Source ObjectRef="(\d+)"/>', video_clip).groups()[0]
    
    media_source = re.search(r'<VideoMediaSource ObjectID="%s"(.*?)</VideoMediaSource>' % object_id, prproj, re.DOTALL).groups()[0]
    
    media_uref = re.search(r'<Media ObjectURef="([^"]+)"/>', media_source).groups()[0]
    
    title_lines = TITLES[media_uref]
    #import pdb;pdb.set_trace()
    return start, end, title_lines
    
    

def parse_titles(prproj):
    media_re = r'<Media ObjectUID="([^"]+)".*?<ImporterPrefs[^>]+>(.*?)</ImporterPrefs>.*?<Title>(\w+)</Title>.*?</Media>'
    for match in re.finditer(media_re, prproj, re.DOTALL):
        uid, data, title_name = match.groups()
        binary = base64.decodestring(data.encode('ascii'))
        
        header, compressed = binary[:32], binary[32:]
        prtl_xml = zlib.decompress(compressed)
        prtl_xml = prtl_xml.decode('utf-16')

        text_list = re.findall('<TRString[^>]*?>(.*?)</TRString>', prtl_xml)
        #print(matches)
        #import pdb;pdb.set_trace()
        TITLES[uid] = text_list
    text = pprint.pformat(TITLES)
    open('detected_titles.txt', 'wb').write(text.encode('utf-8'))

def fix_hebrew(line):
    start = 0
    i = 0
    new_line_parts = []
    is_hebrew_part = False
    for i, c in enumerate(line):
        if c in 'אבגדהוזחטיכלמנסעפצקרשתםףץןך':
            if is_hebrew_part:
                continue
            else:
                is_hebrew_part = True
                new_line_parts.append(line[start:i])
                start = i
            continue
        elif c in string.ascii_letters:
            if is_hebrew_part:
                new_line_parts.append(line[start:i][::-1])
                start = i
            else:
                continue
    i += 1
    if is_hebrew_part:
        new_line_parts.append(line[start:i][::-1])
    else:
        new_line_parts.append(line[start:i])
    
    return ''.join(new_line_parts)

def fix_hebrew_c(line):
    words_list = []
    for word in re.split(r'([א-ת ,.:?!]+)', line):
        if len(word) == 0:
            continue
        
        if word[0] in 'אבגדהוזחטיכלמנסעפצקרשתםףץןך ,.:?!':
            words_list.append(word[::-1])
        else:
            words_list.append(word)
            
    line = ''.join(words_list)
    
    # fix punctuation from the outer edges (bring from the end to the start)
    puncs = r''',."'?!: '''
    ending_puncs = re.findall(r'([%s]+)$' % re.escape(puncs), line)
    if len(ending_puncs) > 0:
        line = ending_puncs[0] + line.rstrip(ending_puncs[0])
    
    return line

def fix_hebrew_b(line):
    original_line = line
    
    # reverse everything
    line = line[::-1]
    
    # make english stuff better again
    words_list = []
    for word in re.split(r'([a-zA-Z]+)', line):
    #for word in re.split(ur'[א-ת]+', line):
        if len(word) == 0:
            continue
        
        if word[0] in string.ascii_letters:
            words_list.append(word[::-1])
        else:
            words_list.append(word)
            
    line = ''.join(words_list)
    
    # fix punctuation from the outer edges (bring from the end to the start)
    puncs = r''',."'?!:'''
    ending_puncs = re.findall(r'([a-zA-Z%s]+)$' % re.escape(puncs), line)
    if len(ending_puncs) > 0:
        line = ending_puncs[0] + line.rstrip(ending_puncs[0])
    
    if len(original_line) != len(line):
        #import pdb;pdb.set_trace()
        raise Exception("A bug in fixing hebrew")
    
    return line

def get_intervals(prproj):
    parse_titles(prproj)
    intervals = []
    framerate = get_framerate(prproj)
    for match in re.finditer(r'<ClipTrackItem Version="4">(.*?)</ClipTrackItem>', prproj, re.DOTALL):
        info = get_info(match.groups()[0], prproj)
        intervals.append(info)

    normalized = []
    for start, end, title_lines in intervals:
        in_time = OFFSET + start / framerate
        out_time = OFFSET + end / framerate
        
        if HEBREW:
            transcript = '\n'.join([fix_hebrew(line) for line in title_lines])
        else:
            transcript = '\n'.join([line for line in title_lines])
        
        normalized.append((in_time, out_time, transcript))
    
    return normalized


if __name__ == "__main__":
    prproj_fname = sys.argv[1]
    subs_fname = sys.argv[2]
    
    prproj = open(prproj_fname, 'r').read()
    intervals = get_intervals(prproj)
    subformat = subtitles.subs_from_fname(subs_fname)
    subs = subformat.render(intervals)
    open(subs_fname, 'wb').write(subs.encode('utf-8'))
