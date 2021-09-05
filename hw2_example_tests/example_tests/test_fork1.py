#!/usr/bin/python

import os
import pyBand
import errno

SINGING = 0
GUITAR = 1
BASS = 2
DRUMS = 3


# listen to a non member - EINVAL + child dosnt inherit father :(
		
# Create a new band
pyBand.band_create(SINGING)

# Add ourselves to every instrument (yeah!)    
pyBand.band_join(0, GUITAR)

# Play something
pyBand.band_play(SINGING, 0)
pyBand.band_play(GUITAR, 10)

	
father_pid = os.getpid()
pid = os.fork()
if pid:
	# Listen to our groovy music
	os.wait()
	print("Parent inside ",os.getpid())

	
else:
	print("child1 - play note",os.getpid())
	#child join and play
	pyBand.band_join(father_pid, DRUMS) 
	pyBand.band_play(DRUMS, 30)

