#ifndef BAND_API
#define BAND_API

#include <errno.h>
#include <linux/list.h>


/*
Description :
Creates a new band and associates the current process with it. The current process will play
instrument. Valid values for instrument are: 0 for singing, 1 for guitar, 2 for bass guitar and 3
for drums.
return value: 0 - success , 1- failure
*/
int band_create(int instrument){
	
	int res;
	__asm__
	(
		"pushl %%eax;"
		"pushl %%ebx;"
		"movl $243, %%eax;"
		"movl %1, %%ebx;"
		"int $0x80;"
		"movl %%eax, %0;"
		"popl %%ebx;"
		"popl %%eax;"
		:"=m"(res)
		:"m"(instrument)
	);
	
	// Return errno values.
	if (res >= (unsigned long)(-125)) {
		errno = -res;
		res = -1;
	}

	return (int)res;
}


/*Description:
Associate the current process with the band of process member, playing instrument
instrument. If member is zero, use the current band. Values for instrument are the same as in
band_create.
*/
int band_join(pid_t member, int instrument) {

	int res;
	__asm__
	(
		"pushl %%eax;"
		"pushl %%ebx;"
		"pushl %%ecx;"
		"movl $244, %%eax;"
		"movl %1, %%ebx;"
		"movl %2, %%ecx;"
		"int $0x80;"
		"movl %%eax, %0;"
		"popl %%ecx;"
		"popl %%ebx;"
		"popl %%eax;"
		:"=m"(res)
		: "m"(member), "m"(instrument)
	);

	// Return errno values.
	if (res >= (unsigned long)(-125)) {
		errno = -res;
		res = -1;
	}

	return (int)res;
}


/*Description:
Play a single note on instrument.
*/
int band_play(int instrument, unsigned char note) {

	int res;
	__asm__
	(
		"pushl %%eax;"
		"pushl %%ebx;"
		"pushl %%ecx;"
		"movl $245, %%eax;"
		"movl %1, %%ebx;"
		"movl %2, %%ecx;"
		"int $0x80;"
		"movl %%eax, %0;"
		"popl %%ecx;"
		"popl %%ebx;"
		"popl %%eax;"
		:"=m"(res)
		: "m"(instrument), "m"(note)
	);
	// Return errno values.
	// Return errno values.
	if (res >= (unsigned long)(-125)) {
		errno = -res;
		res = -1;
	}
	return (int)res;
}



/*Description:
Play a single note on instrument.
*/
int band_listen(pid_t member, unsigned char *chord) {

	int res;
	__asm__
	(
		"pushl %%eax;"
		"pushl %%ebx;"
		"pushl %%ecx;"
		"movl $246, %%eax;"
		"movl %1, %%ebx;"
		"int $0x80;"
		"movl %%eax, %0;"
		"popl %%ecx;"
		"popl %%ebx;"
		"popl %%eax;"
		:"=m"(res)
		: "m"(member), "m"(chord)
	);

	// Return errno values.
	if (res >= (unsigned long)(-125)) {
		errno = -res;
		res = -1;
	}
	return (int)res;
}

#endif
