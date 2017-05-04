from rvr import MP, MPthread
import random

# Q06:
# a. Complete the implementation of the NarrowBridge monitor below using 
#    MPlocks and MPcondition variables. Your implementation should be able 
#    to make progress if there are any cars that can cross.
#

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class NarrowBridge(MP):
    """
    A narrow, one-lane bridge allows cars to pass in either direction, north (0) 
    or south (1). But at any point in time, all cars on the bridge must be going
    in the same direction... or you can imagine what'll happen.

    Cars arriving at the bridge will call the enter() function and will call the
    leave() function upon safely making it to the other side.
    """

    north = 0
    south = 1

    def __init__(self):
        MP.__init__(self)
        self.lock = self.Lock('Bridge Lock')
        self.north = self.lock.Condition('North Mon')
        self.south = self.lock.Condition('South Mon')
        self.cars_north = 0
        self.cars_south = 0


    def enter(self, direction):
        """wait for permission to flow through the pipe. direction should be either
        0 or 1."""
        with self.lock:
            if direction == 0:
                while self.cars_south != 0:
                    self.north.wait()
                self.cars_north += 1
            else:
                while self.cars_north != 0:
                    self.south.wait()
                self.cars_south += 1

        

    def leave(self,direction):
        with self.lock:
            if direction == 0:
                self.cars_north -= 1
                if self.cars_north == 0:
                    self.south.broadcast()
            else:
                self.cars_south -= 1
                if self.cars_south == 0:
                    self.north.broadcast()


################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Car(MPthread):

    def __init__(self, bridge, car_id):
        MPthread.__init__(self, bridge, car_id)
        self.direction = random.randrange(2)
        self.wait_time = random.uniform(0.1,0.5)
        self.bridge    = bridge
        self.car_id    = car_id


    def run(self):
        # drive to the bridge
        self.delay(self.wait_time)
        print "Car %d: Trying to cross %s" % (self.car_id, "south" if self.direction else "north")
        # request permission to cross
        self.bridge.enter(self.direction)
        print "Car %d: Crossing" % self.car_id
        # drive across
        self.delay(0.01)
        print "Car %d: Crossed" % self.car_id
        # signal that we have finished crossing
        self.bridge.leave(self.direction)
        print "Car %d: Finished crossing" % self.car_id


if __name__ == "__main__":

    bridge = NarrowBridge()
    for i in range(100):
        Car(bridge, i).start()

