from rvr import MP, MPthread

# Q05:
# You are in charge of seating assignments for a nonpartisan political
# convention.
#
# The convention center’s numerous seats will be holding guests who will be
# allowed to come and go as seating permits, and who will hold widespread
# ideologies and allegiances. For simplicity, however, we will assume that
# seats will only be filled by three types of guests: Bernie Sanders supporters,
#  Hillary Clinton supporters, and Donald Trump supporters.
# (Assume, likewise for simplicity, that no one present considers themselves
# more than one of the above.)
# In addition, due to the potential for disagreements breaking out,
# security personnel must also be given access to the seats:
# for simplicity, assume they fill seats in the same way as normal guests.
#
# The rules are as follows: 
# (a) There are no more than N seats assigned to guests (or inspectors)
# at any given time.
# (b) A Sanders supporter will not be allowed to take a seat if, after doing so,
# more than 50% of the seats in use would be assigned to Sanders supporters.
# On an unrelated note, the convention's committee hereby denies any contact
# with a certain Mrs. Wasserman Schultz.
# (c) A Clinton supporter will not be allowed to take a seat if there are any
# Trump supporters currently seated at the convention. Noise ordinance violations
# and meme oversaturation would otherwise follow.
# (d) Likewise, a Trump supporter will not be allowed to take a seat if there
# are any Clinton supporters currently sitting at the convention. The existing
# security detail would not be enough to hold them back.
# (e) Security guards are always allowed priority access to the seats,
# subject to condition (a).
# No guest should be allowed to use a seat if a security guard is waiting.

# Implement the Seater monitor using MPlocks and MPcondition variables.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class Seater(MP):
    def __init__(self, n):
        MP.__init__(self)
        self.seats = n
        self.total_seat = 0
        self.hil_seat = 0
        self.trump_seat = 0
        self.sand_seat = 0
        self.sec_wait = 0
        self.hil_wait = 0
        self.sand_wait = 0
        self.trump_wait = 0
        self.lock = self.Lock('Seating Lock')
        self.hil = self.lock.Condition('Hilary Mon')
        self.trump = self.lock.Condition('Trump Mon')
        self.sand = self.lock.Condition('Sanders Mon')
        self.sec = self.lock.Condition('Security Mon')

    def sanders_sit(self):
        with self.lock:
            self.sand_wait += 1
            while (self.total_seat == 25 or self.total_seat == 0 or (((self.sand_seat + 1)/self.total_seat) > .5)):
                self.sand.wait()
            self.total_seat += 1
            self.sand_seat += 1
            self.sand_wait -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()

    def sanders_leave(self):
        with self.lock:
            self.total_seat -= 1
            self.sand_seat -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
                

    def clinton_sit(self):
        with self.lock:
            self.hil_wait += 1
            while (self.total_seat == 25 or self.trump_seat > 0):
                self.hil.wait()
            self.total_seat += 1
            self.hil_seat += 1
            self.hil_wait -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
            
            

    def clinton_leave(self):
        with self.lock:
            self.total_seat -= 1
            self.hil_seat -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
                

    def trump_sit(self):
        with self.lock:
            self.trump_wait += 1
            while (self.total_seat == 25 or self.hil_seat > 0):
                self.trump.wait()
            self.total_seat += 1
            self.trump_seat += 1
            self.trump_wait -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
            

    def trump_leave(self):
        with self.lock:
            self.total_seat -= 1
            self.trump_seat -= 1
            if (self.sec_wait > 0 and self.total_seat != 25):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
                

    def security_sit(self):
        with self.lock:
            self.sec_wait += 1
            while (self.total_seat == 25):
                self.sec.wait()
            self.total_seat += 1
            self.sec_wait -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
            


    def security_leave(self):
        with self.lock:
            self.total_seat -= 1
            if (self.total_seat != 25 and self.sec_wait > 0):
                self.sec.signal()
            elif (self.sand_wait > 0 and self.total_seat != 25 and self.total_seat != 0 and (((self.sand_seat + 1)/self.total_seat) < .5)):
                self.sand.signal()
            elif (self.hil_wait > 0 and self.total_seat != 25 and self.trump_seat == 0):
                self.hil.signal()
            elif (self.trump_wait > 0 and self.total_seat != 25 and self.hil_seat == 0):
                self.trump.signal()
                

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

SANDERS     = 0
CLINTON     = 1
TRUMP       = 2
SECURITY    = 3

class Guest(MPthread):
    def __init__(self, supporter_type, seater, name):
        MPthread.__init__(self, seater, name)
        self.supporter_type = supporter_type
        self.seater = seater

    def run(self):
        enters = [self.seater.sanders_sit,
                  self.seater.clinton_sit,
                  self.seater.trump_sit,
                  self.seater.security_sit]
        leaves = [self.seater.sanders_leave,
                  self.seater.clinton_leave,
                  self.seater.trump_leave,
                  self.seater.security_leave]
        names  = ['sanders supporter',
                  'clinton supporter',
                  'trump supporter',
                  'security']

        print("%s trying to take a seat" % names[self.supporter_type])
        enters[self.supporter_type]()
        print("%s has sat down" % names[self.supporter_type])
        self.delay(0.1)
        print("%s getting up to leave" % names[self.supporter_type])
        leaves[self.supporter_type]()
        print("%s has left" % names[self.supporter_type])

max_seats = 25
numbers = [20, 35, 30, 6]
seater = Seater(max_seats)
for t in [SANDERS, CLINTON, TRUMP, SECURITY]:
    for i in range(numbers[t]):
        if t == 0:
            Guest(t, seater, 'SANDERS' + str(i)).start()
        elif t == 1:
            Guest(t, seater, 'CLINTON' + str(i)).start()
        elif t == 2:
            Guest(t, seater, 'TRUMP' + str(i)).start()
        else:
            Guest(t, seater, 'SECURITY' + str(i)).start()

seater.Ready()
