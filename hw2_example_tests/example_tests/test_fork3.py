#!/usr/bin/python

import os
import pyBand
import errno
import time

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
	time.sleep(1)
	pid2 = os.fork()
	if pid2:
		time.sleep(1)  # wait for child to play the last note
		print("father listening")
		chord = pyBand.band_listen(os.getpid()) # can listen - all notes are written
		assert chord[0] == 0
		assert chord[1] == 10
		assert chord[2] == 20
		assert chord[3] == 30
		chord1 = pyBand.band_listen(pid) # can listen - all notes are written
		assert chord1[0] == 0
		assert chord1[1] == 10
		assert chord1[2] == 20
		assert chord1[3] == 30

	else:
		print("child2 play note")
		#child2 join and play
		pyBand.band_join(father_pid, BASS)
		pyBand.band_play(BASS, 20)
		pyBand.band_join(pid, BASS)
		pyBand.band_join(pid, SINGING)
		pyBand.band_join(pid, GUITAR)
		pyBand.band_play(SINGING, 0)
		pyBand.band_play(GUITAR, 10)
		pyBand.band_play(BASS, 20)
		time.sleep(5)



else:
	print("child1 play note")
	#child join and play
	pyBand.band_join(father_pid, DRUMS) 
	pyBand.band_play(DRUMS, 30)
	pyBand.band_create(DRUMS)
	pyBand.band_play(DRUMS, 30)
	time.sleep(5)


