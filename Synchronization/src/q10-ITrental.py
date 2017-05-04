from rvr import MP, MPthread
import random

# Q10:
#
# IT offers 150 monitors and 100 laptops for students to reserve for course 
# work. 
#
# Each student can reserve a single monitor and a laptop at a time, and may luckily
# receive an extra monitor (with probability 1/2). For each student, a coordinator 
# thread attempts to reserve these devices. 
#
# A device can only be assigned to one student at a time.
#
# Modify the following code to avoid deadlocks.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

mp = MP()

# devices are represented by Lock objects; if a device has been reserved
# then the lock is held.

MONITORNO = 150
LAPTOPNO = 100

monitors = [mp.Lock('m'+str(i)) for i in range(MONITORNO)]
laptops = [mp.Lock('l'+str(i)) for i in range(LAPTOPNO)]

class Coordinator(MPthread):
    def __init__(self, id, mp):
        MPthread.__init__(self, mp, 'Coordinator')
        self.id = id

    def run(self):
        while True:

            mon = random.randrange(MONITORNO)
            lap = random.randrange(LAPTOPNO)

            lucky = random.getrandbits(1)

            if lucky:
                extra_mon = random.randrange(MONITORNO)
                if extra_mon != mon:
                    if mon < extra_mon:
                        monitors[mon].acquire()
                        monitors[extra_mon].acquire()
                        laptops[lap].acquire()
                    else:
                        monitors[extra_mon].acquire()
                        monitors[mon].acquire()
                        laptops[lap].acquire()
                else:
                    monitors[mon].acquire()
                    laptops[lap].acquire()
                    lucky = 0
            else:
                monitors[mon].acquire()
                laptops[lap].acquire()


            # do course work
            if lucky:
                print ("coordinator %i reserved laptop %i and monitor %i, %i" % (self.id, lap, mon, extra_mon))
            else:
                print ("coordinator %i reserved laptop %i and monitor %i" % (self.id, lap, mon))
            self.delay(0.1)

            monitors[mon].release()
            laptops[lap].release()
            if lucky:
                monitors[extra_mon].release()

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

for i in range(20):
    Coordinator(i, mp).start()
