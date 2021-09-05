#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


def test10():	# instrument is taken by a different process (me)

    # Create a new band
    pyBand.band_create(SINGING)

    # Add ourselves to every instrument (yeah!)
    pyBand.band_join(os.getpid(), GUITAR)
    pyBand.band_join(0, GUITAR)



#############################################################################

#if __name__ == "__main__":

try:		
	test10()
except OSError,e:
	
	assert e.errno == errno.ENOSPC

