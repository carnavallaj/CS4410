from rvr import MP, MPthread
import time, random

# Q08:
#
#   Circuit de Monaco is one of the world's most famous racetracks. It has been 
#	in operation since its first race in 1929, and is due for a tech upgrade. You 
#	are a software engineer hired to design a program that controls the racetrack's 
#	automated lights. 
#
#   In order to keep their skills sharp and save time, professional racecar drivers 
#	run 1 lap races, one round after another. At the start of each round, all racers 
#	(threads) will leave the start line simultaneously. In order to avoid collision 
#	and confusion, there cannot be more than 1 race being run on the track at any 
#	given time.
#
#   When a racer finishes a round, it will call the start_next_round() function. 
#   The function blocks until all other racers finish the round, before starting 
#   the next one. 
#
#   Implement the RaceTrack monitor using Python MPlock and MPcondition variables.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class RaceTrack(MP):

	def __init__(self, num_racers):
		MP.__init__(self)
		self.num_racers = num_racers
		self.race = 0
		self.racers_ready1 = 0
		self.racers_ready2 = 0
		self.lock = self.Lock('Racer Lock')
		self.all_racers_finished1 = self.lock.Condition('All Racers Finished Race 0 Mon')
		self.all_racers_finished2 = self.lock.Condition('All Racers Finished Race 1 Mon')

	def start_next_round(self):
		""" 
		Called by a racer who has just completed a round. Wait until all other
		racers are done before starting the next round.
		"""
		with self.lock:
			if self.race == 0:
				self.racers_ready1 += 1
				if self.racers_ready1 < self.num_racers:
					while self.racers_ready1 < self.num_racers:
						self.all_racers_finished1.wait()
				else:
					self.race = 1
					self.racers_ready2 = 0
					self.all_racers_finished1.broadcast()
			elif self.race == 1:
				self.racers_ready2 += 1
				if self.racers_ready2 < self.num_racers:
					while self.racers_ready2 < self.num_racers:
						self.all_racers_finished2.wait()
				else:
					self.race = 0
					self.racers_ready1 = 0
					self.all_racers_finished2.broadcast()

			
			



################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Racer(MPthread):

	def __init__(self, racetrack, name, id):
		MPthread.__init__(self, racetrack, name)
		self.racetrack = racetrack
		self.id         = id

	def run(self):
		while True:
			# wait for start of race
			print("racer #%d: waiting for start" % self.id)
			self.racetrack.start_next_round()

			# run the race
			print("racer #%d: starting race" % self.id)
			self.delay(random.randint(0, 2))
			print("racer #%d: finished race" % self.id)


if __name__ == '__main__':
	num_threads = 10
	racetrack = RaceTrack(num_threads)
	for i in range(num_threads):
		Racer(racetrack, 'Racer' + str(i), i).start()

	racetrack.Ready()

