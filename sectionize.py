#!/usr/bin/env python
# encoding: utf=8
"""
sections.py

Analyze with Echonest, print out details about track and potentially render various sections.

[http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf]

tatums
: list of tatum markers, in seconds. Tatums represent the lowest regular pulse train that a listener intuitively
infers from the timing of perceived musical events (segments).
‣
beats
: list of beat markers, in seconds. A beat is the basic time unit of a piece of music; for example, each tick of
a metronome. Beats are typically multiples of tatums.
‣
bars
: list of bar markers, in seconds. A bar (or measure) is a segment of time defined as a given number of beats.
Bar offsets also indicate downbeats, the first beat of the measure.
‣
sections
: a set of section markers, in seconds. Sections are defined by large variations in rhythm or timbre, e.g.
chorus, verse, bridge, guitar solo, etc. Each section contains its own descriptions of tempo, key, mode,
time_signature, and loudness.

By Mike iLL/mZoo.org, 2014-07-20.
"""
from __future__ import print_function
import echonest.remix.audio as audio
import sys, os
import pickle


usage = """
Usage: 
    python sectionize.py <input_filename> 

Example:
    python sectionize.py audio/Gondoliers11.mp3	 
    python sectionize.py audio/Gondoliers39.mp3
 
"""

try:
    input_filename = sys.argv[1]
except:
     print(usage)
     sys.exit(-1)

spacer = "*" + (' ' * 58) + "*"
border = "*" * 60     

def track_details(track):
    """
    Print echonest analysis details of track to stdout. 
    """
    segments = track.segments
    
    sections = track.sections
    heading = "  Some details about " + input_filename + "  "
    print(heading.center(60,"*"), spacer)
    print("Track Duration: {0:14.4f}".format(track.duration))
    
    if track.sections:
        sections = track.sections
        
        print("* Counted {0:6d} sections".format(len(sections)))
        
        print(spacer, os.linesep, os.linesep, spacer, border)
    else:
        no_beats = "********No Sections Detected********"
        print(no_beats)
        print(spacer)
        print("*" * len(no_beats))
        
    print(spacer)



def main(input_filename):
    """

    """
    try:
        with open(input_filename + '.analysis.en') as f:
            audiofile = pickle.load(f)
    except IOError:
        audiofile = audio.LocalAudioFile(input_filename)
        audiofile.save()
        
    track = audiofile.analysis
    track_details(track)
    for name, section in enumerate(track.sections, 1):
        section.render().encode(str(name) + ".mp3")
        
    print(spacer, os.linesep, border)
    

if __name__ == "__main__":
    main(input_filename)
