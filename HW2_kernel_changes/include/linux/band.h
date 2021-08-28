#ifndef BAND_H
#define BAND_H

#include <linux/list.h>
#include <linux/types.h>
#include <linux/linkage.h>
#include <linux/errno.h>
///*Remove before compiling ot kernel*/!!!
//#include "list.h"
//#include "sched.h
//#include "current.h"
//#include "types.h"


/*defines:*/
#define SINGING 0
#define GUITAR 1
#define BASS 2
#define DRUMS 3
#define INSTS_NUM 4
typedef enum { T_FALSE, T_TRUE } T_BOOL;

/*structs*/
typedef struct note {
	unsigned char data;
	T_BOOL was_listened;
} Note;

typedef struct band {
	list_t list;
	pid_t instruments[INSTS_NUM];
	Note notes[INSTS_NUM];
	int members_cnt;
} Band;

/*Declarations*/
void leave_band(Band* new_band_to_assign);
#endif
