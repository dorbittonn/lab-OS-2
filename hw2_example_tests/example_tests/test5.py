#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


def test5():	# cant play because instrument is allocated

    # Create a new band
    pyBand.band_create(SINGING)

    # Add ourselves to every instrument (yeah!)
    #pyBand.band_join(0, GUITAR)
    pyBand.band_join(0, BASS)
    pyBand.band_join(0, DRUMS)

    # Play something
    pyBand.band_play(GUITAR, 10)

#############################################################################

#if __name__ == "__main__":

try:		
	test5()
except OSError,e:
	assert e.errno == errno.EACCES	#EACCES == 13
	

