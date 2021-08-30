#include <linux/kernel.h>
#include <asm/current.h>
#include <asm/uaccess.h>
#include <linux/slab.h>
#include <linux/sched.h>
#include <linux/band.h>

#ifndef __KERNEL__
#define __KERNEL__
#endif 

#define LINUX
#define MODULE

//#include "sched.h"
//#include "band.h"

LIST_HEAD(band_list);

void print_bands(void) {
	if (list_empty(&band_list)) {
		printk(KERN_ALERT "band list is empty\n");
		return;
	}
	list_t* curr;
	Band* pb;
	list_for_each(curr, &band_list) {
		pb = list_entry(curr, Band, list);
		printk(KERN_ALERT "---Band----\n");
		printk("curr %d \n", *curr);
		printk("curr->next %d \n", curr->next);
		printk("curr->prev %d \n", curr->prev);
		int k = 0;
		for (; k < INSTS_NUM; k++) {
			printk(KERN_ALERT "( %d ) - pid %d -note %d -was_listened %d\n",
				k, pb->instruments[k], pb->notes[k].data, pb->notes[k].was_listened);
		}
	}
	
}


void leave_band(Band * new_band_to_assign) {
	Band* prev_band = current->band;
	if (prev_band != NULL && prev_band != new_band_to_assign) {
		int i = 0;
		for (; i < INSTS_NUM; i++) {
			if (prev_band->instruments[i] == current->pid) {
				//printk(KERN_ALERT "--inside if in prev band-- %d\n", current->pid);
				prev_band->members_cnt--;
				prev_band->instruments[i] = -1;
			}
		}
		/*If I am the last process in the previous band, so release the entire band from the list*/
		if (prev_band->members_cnt == 0) {
			//printk(KERN_ALERT "last member in the band\n");
			list_del(&prev_band->list);
			kfree(prev_band);
		}
	}
	
	if (new_band_to_assign != NULL) {
		current->band = new_band_to_assign;
	}
	else {
		current->band = NULL;
	}

}


int band_create(int instrument) {
	//printk(KERN_ALERT "Inside the %s function\n", __FUNCTION__);

	// Checking arguments
	if (instrument < 0 || instrument > 3) {
		return -EINVAL;
	}

	Band* new_band = (Band*)kmalloc(sizeof(Band), GFP_KERNEL);
	if (new_band == NULL) {
		return -ENOMEM;
	}

	// Initializing a Band of the creating process.
	int j = 0;
	for (; j < INSTS_NUM; j++) {
		new_band->instruments[j] = -1;
		Note new_note = { .data='\0', .was_listened=T_TRUE };
		new_band->notes[j] = new_note;
	}
	new_band->instruments[instrument] = current->pid;
	new_band->members_cnt = 1;
	
	// Initialize band list if there's no band 
	if (list_empty(&band_list)) {
		INIT_LIST_HEAD(&band_list); 
	}

	list_add(&new_band->list, &band_list);

	// Leave the current band properly
	leave_band(new_band);
	
	//print_bands();

	return 0;
}

int band_join(pid_t member, int instrument) {
	if (member < 0) {
		return -ESRCH;
	}
	if (instrument < 0 || instrument > 3) {
		return -EINVAL;
	}
		/* join to the current band of the calling process */
	if (member == 0 || member == current->pid) {
		if (current->band == NULL) {
			/*This means this process is not in a band*/
			return -EINVAL;
		}
		else if(current->band->instruments[instrument] != -1){
			return -ENOSPC;
		}
		current->band->instruments[instrument] = current->pid;
		current->band->members_cnt++;
		Note new_note = { .data = '\0', .was_listened = T_TRUE };
		current->band->notes[instrument] = new_note;
	}

	else {
		/* joins to member's band*/
		task_t* member_ts = find_task_by_pid(member);
		if (member_ts == NULL) {
			return -ESRCH;
		} 
		if (member_ts->band == NULL) {
			return -EINVAL;
		}
		if (member_ts->band->instruments[instrument] != -1) {
			return -ENOSPC;
		}

		/*Assign to the new band*/
		member_ts->band->instruments[instrument] = current->pid;
		member_ts->band->members_cnt++;
		Note new_note = { .data = '\0', .was_listened = T_TRUE };
		member_ts->band->notes[instrument] = new_note;
		//list_add(&member_ts->band->list, &band_list);

		/*leave the previous band if exists*/
		leave_band(member_ts->band);
		}
	//print_bands();

	return 0;
}

int band_play(int instrument, unsigned char note) {
	if (instrument < 0 || instrument > 3) {
		return -EINVAL;
	}
	if (current->band == NULL) {
		return -ENOENT;
	}
	if (current->band->instruments[instrument] != current->pid) {
		return -EACCES;
	}
	/*if is_played is true it means that there's no available character to play*/
	if (current->band->notes[instrument].was_listened == T_FALSE) {
		return -EBUSY;
	}
	//printk("char recieved is %d\n", note);

	/*Play the note*/
	current->band->notes[instrument].data = note;
	current->band->notes[instrument].was_listened = T_FALSE;

	//printk("char played is %d\n", current->band->notes[instrument].data);

	//print_bands();

	return 0;
}

int band_listen(pid_t member, unsigned char* chord) {
	if (chord == NULL) {
		return -EFAULT;
	}
	task_t* member_ts = find_task_by_pid(member);
	if ( member < 0 || member_ts == NULL ) {
		return -ESRCH;
	}
	if (member_ts->band == NULL) {
		return -EINVAL;
	}
	/* Check if all instruments played and wasnt listened yet*/
	if (!member_ts->band->notes[SINGING].was_listened &&
		!member_ts->band->notes[GUITAR].was_listened &&
		!member_ts->band->notes[BASS].was_listened &&
		!member_ts->band->notes[DRUMS].was_listened ){

		//printk(KERN_ALERT "Ready to listen \n");

		unsigned char inner_chord[INSTS_NUM] = { member_ts->band->notes[SINGING].data,
												member_ts->band->notes[GUITAR].data,
												member_ts->band->notes[BASS].data,
												member_ts->band->notes[DRUMS].data };
		
		if (copy_to_user((void*)chord, (const void*)inner_chord, sizeof(char)*4 ) != 0) {
			return -EFAULT; /**/
		}

		/* Mark notes as listened */
		member_ts->band->notes[SINGING].was_listened = T_TRUE;
		member_ts->band->notes[GUITAR].was_listened = T_TRUE;
		member_ts->band->notes[BASS].was_listened = T_TRUE;
		member_ts->band->notes[DRUMS].was_listened = T_TRUE;

	}
	else {
		//printk(KERN_ALERT "not ready to play yet\n");

		return -EAGAIN;

	}
	//print_bands();

	return 0;
}
