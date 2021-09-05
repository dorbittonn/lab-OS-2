#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


def test8():	# nonexisting process

    # Create a new band
    pyBand.band_create(SINGING)

    # Add ourselves to every instrument (yeah!)
    pyBand.band_join(os.getpid(), GUITAR)
    pyBand.band_join(0, BASS)
    pyBand.band_join(os.getpid()+1, DRUMS)


#############################################################################

#if __name__ == "__main__":

try:		
	test8()
except OSError,e:
	
	assert e.errno == errno.ESRCH

