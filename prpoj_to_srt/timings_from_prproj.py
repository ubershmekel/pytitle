'''
timings_from_prproj.py takes a prproj file that has one sequence full of titles
and outputs the in and out times of each title.

This can be useful if you made subtitles using adobe premiere and
want to convert the subtitles to srt or sub files.
'''
from __future__ import division
import re
import pprint

SEQUENCE_FRAMERATE = 25


def get_framerate(prproj):
    rate_match = next(re.finditer(r'<FrameRate>(\d+)</FrameRate>', prproj))
    number_str = rate_match.groups()[0]
    return int(number_str) * SEQUENCE_FRAMERATE

def get_intervals(prproj):
    intervals = []
    framerate = get_framerate(prproj)
    times_str = re.findall(r'<End>(\d+)</End>\s+<Start>(\d+)</Start>', prproj)

    for out_time, in_time in times_str:
        if '0' == in_time:
            continue
        pair = int(in_time), int(out_time)
        
        if pair not in intervals:
            intervals.append(pair)
    
    
    normalized = []
    first_frame = intervals[0][0]
    for pair in intervals:
        in_time = (pair[0] - first_frame) / framerate
        out_time = (pair[1] - first_frame) / framerate
        normalized.append((in_time, out_time))
    
    return normalized


if __name__ == "__main__":
    prproj = open('JustSubs.prproj', 'r').read()
    intervals = get_intervals(prproj)
    open('subtitle_intervals.txt', 'w').write(pprint.pformat(intervals))
