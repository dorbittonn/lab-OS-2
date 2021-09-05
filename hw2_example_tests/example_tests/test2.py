#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


def test2():  # check if listen won't work when we play only 3 notes

    # Create a new band
    pyBand.band_create(SINGING)

    # Add ourselves to every instrument (yeah!)
    pyBand.band_join(0, GUITAR)
    pyBand.band_join(0, BASS)
    pyBand.band_join(0, DRUMS)

    # Play something
    pyBand.band_play(SINGING, 0)
    pyBand.band_play(GUITAR, 10)
    #pyBand.band_play(BASS, 20)
    pyBand.band_play(DRUMS, 30)

    # Listen to our groovy music
    chord = pyBand.band_listen(os.getpid()) # band_
	
#############################################################################

try:		
	test2()
except OSError,e:
	assert e.errno == errno.EAGAIN #EAGAIN == 11
