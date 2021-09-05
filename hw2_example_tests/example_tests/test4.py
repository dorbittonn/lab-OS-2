#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3

def test4():	# process is not in any band - play

    pyBand.band_play(GUITAR, 10)

#############################################################################

#if __name__ == "__main__":

try:		
	test4()
except OSError,e:
	assert e.errno == errno.ENOENT	#ENOENT == 2
