#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


def test9():	# join a process (me) not in a band

    # Add ourselves to every instrument (yeah!)
    pyBand.band_join(0, GUITAR)


#############################################################################

#if __name__ == "__main__":

try:		
	test9()
except OSError,e:
	
	assert e.errno == errno.EINVAL

