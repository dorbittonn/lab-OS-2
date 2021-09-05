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
	pid2 = os.fork()
	if pid2:
		os.wait()  # wait for child to play the last note
		print("father listening")
		chord = pyBand.band_listen(os.getpid()) # can listen - all notes are written
		assert chord[0] == 0
		assert chord[1] == 10
		assert chord[2] == 20
		assert chord[3] == 30
	else:
		print("child2 play note")
		#child2 join and play
		pyBand.band_join(father_pid, BASS)
		pyBand.band_play(BASS, 20)
else:
	print("child1 play note")
	#child join and play
	pyBand.band_join(father_pid, DRUMS) 
	pyBand.band_play(DRUMS, 30)

