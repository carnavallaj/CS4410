from rvr import MP, MPthread
import random

# Q09:
# This program simulates the creation of water molecules.
#
# Implement the ChemistryChamber monitor below using MPlocks and
# MPcondition variables.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class ChemistryChamber(MP):
    """
    A water molecule is made from 2 hydrogen atoms and an oxygen atom (each
    hydrogen and oxygen can be used in only one molecule).  A thread offers an
    atom by calling the appropriate method; the thread will block until
    the atom can be used in the molecule.
    """

    def __init__(self):
        MP.__init__(self)
        self.oxygen_waiting = 0
        self.hydrogen_waiting = 0
        self.oxygen_assign = 0
        self.hydrogen_assign = 0
        self.lock = self.Lock('Chamber Entry Lock')
        self.hydrogen_entry = self.lock.Condition('Hydrogen Entry Mon')
        self.oxygen_entry = self.lock.Condition('Oxygen Entry Mon')


    def oxygen_ready(self):
        """Offer an oxygen atom and block until this atom can be used to make
        a molecule."""
        with self.lock:
            self.oxygen_waiting += 1
            while self.oxygen_assign == 0:
                if self.hydrogen_waiting >= 2 and self.oxygen_waiting >= 1:
                    self.hydrogen_waiting -= 2
                    self.oxygen_waiting -= 1
                    self.hydrogen_assign += 2
                    self.oxygen_assign += 1
                    self.hydrogen_entry.signal()
                    self.hydrogen_entry.signal()
                else:
                    self.oxygen_entry.wait()
            self.oxygen_assign -= 1

        

    def hydrogen_ready(self):
        """Offer a hydrogen and block until this atom can be used to make a
        molecule."""
        with self.lock:
            self.hydrogen_waiting += 1
            while self.hydrogen_assign == 0:
                if self.hydrogen_waiting >= 2 and self.oxygen_waiting >= 1:
                    self.hydrogen_waiting -= 2
                    self.oxygen_waiting -= 1
                    self.hydrogen_assign += 2
                    self.oxygen_assign += 1
                    self.hydrogen_entry.signal()
                    self.oxygen_entry.signal()
                else:
                    self.hydrogen_entry.wait()
            self.hydrogen_assign -= 1



################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Oxygen(MPthread):
    def __init__(self, chamber, id):
        MPthread.__init__(self, chamber, id)
        self.chamber = chamber
        self.id = id

    def run(self):
        while True:
            print "Oxygen %d ready" % self.id
            self.chamber.oxygen_ready()
            print "Oxygen %d is in the chamber" % self.id
            self.delay()
            print "Oxygen %d finished reacting" % self.id

class Hydrogen(MPthread):
    def __init__(self, chamber, id):
        MPthread.__init__(self, chamber, id)
        self.chamber = chamber
        self.id = id

    def run(self):
        while True:
            print "Hydrogen %d ready" % self.id
            self.chamber.hydrogen_ready()
            print "Hydrogen %d is in the chamber" % self.id
            self.delay(0.5)
            print "Hydrogen %d finished reacting" % self.id

if __name__ == '__main__':
    NUM_OXYGEN = 5
    NUM_HYDROGEN = 6

    c = ChemistryChamber()

    for i in range(NUM_OXYGEN):
        Oxygen(c, i).start()

    for j in range(NUM_HYDROGEN):
        Hydrogen(c, j).start()

    c.Ready()
