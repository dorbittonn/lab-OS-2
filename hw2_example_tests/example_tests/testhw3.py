#!/usr/bin/python

import os
import errno
import pyBand
import time

def spend_time(secs):
    for i in range(secs):
        # This spends about 1s. If not, increase the range
        for j in xrange(15000000):
            pass

def test1():
	""" Verify a bass player blocks other processes """
	cpid = os.fork()
	if cpid == 0:
		# In child: Create a band as the bass player, then block the parent
		pyBand.band_create(2)
		spend_time(5)
		os._exit(0)
	# In parent: Give child time to create the band, then join and see if we're blocked
	time.sleep(1) # force de-scheduling of the parent
	s = time.time()
	pyBand.band_join(cpid, 0)
	e = time.time()
	elapsed = e - s
	print elapsed
	assert (elapsed > 3), "Expected singer to yield time to bass player"

def test2():
    """ Verify a bass player blocks other processes """
    cpid = os.fork()
    if cpid == 0:
        # In child: Create a band as the singer, then blocked by the parent
		s = time.time()
		pyBand.band_create(0)
		time.sleep(2)
		e = time.time()
		elapsed = e - s
		assert (elapsed > 3), "Expected singer to yield time to bass player"
		os._exit(0)
    # In parent: Give child time to create the band, then join and see if we block
    time.sleep(1) # force de-scheduling of the parent
    pyBand.band_join(cpid, 2)
    spend_time(5)
	
def test3():
    """ Verify a bass player blocks other processes """
    cpid = os.fork()
    if cpid == 0:
        # In child: Create a band as the singer, then blocked by the parent
		pyBand.band_create(0)
		time.sleep(2)
		pyBand.band_play(0,8)
		os._exit(0)
    # In parent: Give child time to create the band, then join and see if we block
	# then spend time, make sure child cant play, so father cant listen
    time.sleep(1) # force de-scheduling of the parent
    pyBand.band_join(cpid, 2)
    pyBand.band_join(cpid, 1)
    pyBand.band_join(cpid, 3)
    pyBand.band_play(1, 5)
    pyBand.band_play(2, 9)
    pyBand.band_play(3, 2)
    spend_time(1)
    try:
        pyBand.band_listen(os.getpid())
    except OSError,e:
	    assert e.errno == errno.EAGAIN

def test4():
	""" Verify a bass player blocks other processes """
	cpid = os.fork()
	if cpid == 0:
		# In child: Create a band as the bass player, then block the parent
		pyBand.band_create(2)
		spend_time(9)
		os._exit(0)
	# In parent: Give child time to create the band, then join and see if we're blocked
	time.sleep(1) # force de-scheduling of the father
	c2pid = os.fork()
	if c2pid == 0:
		s = time.time()
		pyBand.band_join(cpid, 1)
		e = time.time()
		elapsed = e - s
		assert (elapsed > 3), "Expected guitar player to yield time to bass player"
		os._exit(0)
	s = time.time()
	pyBand.band_join(cpid, 0)
	e = time.time()
	elapsed = e - s
	print(elapsed)
	assert (elapsed > 3), "Expected singer to yield time to bass player"

def test5():
    """ Verify a bass player blocks other processes """
    cpid = os.fork()
    if cpid == 0:
        # In child: Create a band as the bass player, then block the parent
        pyBand.band_create(2)
        spend_time(5)
        print("child goes 2 sleep")
        time.sleep(1)
        print("child awake")
        spend_time(5)
        os._exit(0)
    # In parent: Give child time to create the band, then join and see if we're blocked
    time.sleep(1) # force de-scheduling of the parent
    s = time.time()
    pyBand.band_join(cpid, 0)
    print("father joined")
    e = time.time()
    elapsed = e - s
    assert (elapsed > 3), "Expected singer to yield time to bass player"
    spend_time(10)

if __name__ == "__main__":
    test1()
    test2()	
    test3()
    test4()
    test5()
