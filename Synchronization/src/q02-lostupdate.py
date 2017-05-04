from rvr import MP, MPthread

# Q02:
# 
# This question requires you to answer a few questions about this code
# on a CMS quiz and to modify the code itself.
# 
# This program simulates a game between two teams.  Each team presses
# their button as fast as they can.  There is a counter that starts at
# zero; the red team's button increases a counter, while the blue
# team's button decreases the counter.  They each get to press their
# button 10000 times. If the counter ends up positive, the read team
# wins; a negative counter means the blue team wins.
#
# This game is boring: it should always end in a draw.  However the
# provided implementation is not properly synchronized.
#
# YOUR TASK: Add appropriate synchronization such that updates to the
# counter occur in a critical section, ensuring that the energy level
# is always at 0 when the two threads terminate.
#
# Your synchronization must still allow interleaving between the two threads.
#     
# (Now would be a good time to go read the file rvr.md in your docs folder.
#  It will explain how to use a variety of synchronization primitives supported
#  by the 4410 Synchronization Library, which must be exclusively used for this
#  entire assignment.)

class Contest(MP):
    def __init__(self):
        MP.__init__(self)
        self.counter = self.Shared("counter", 0)
        self.lock = self.Lock(self.counter)

    def pushRed(self):
        self.counter.inc()

    def pushBlue(self):
        self.counter.dec()

class RedTeam(MPthread):
    def __init__(self, contest):
        MPthread.__init__(self, contest, "Red Team")
        self.contest = contest     

    def run(self):
        for i in range(10000):
            with self.contest.lock:
                self.contest.pushRed()

class BlueTeam(MPthread):
    def __init__(self, contest):
        MPthread.__init__(self, contest, "Blue Team")
        self.contest = contest

    def run(self):
        for i in range(10000):
            with self.contest.lock:
                self.contest.pushBlue()

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

contest = Contest()
red  = RedTeam(contest)
blue = BlueTeam(contest)
red.start()
blue.start()
contest.Ready()

print("The counter is " + str(contest.counter.read()))
