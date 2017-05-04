from rvr import MP, MPthread

# Q01: 
#
# You will be asked a few questions about the behavior of this program
# in some short multiple choice questions on CMS. In the meantime,
# look over and then run the following concurrent program. Try running
# it by itself and then try running it while browsing the web.

class Worker1(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 1")

    def run(self):
        while True:
            print("Hello from Worker 1")

class Worker2(MPthread):
    def __init__(self, mp):
        MPthread.__init__(self, mp, "Worker 2")

    def run(self):
        while True:
            print("Hello from Worker 2")
mp = MP()
w1 = Worker1(mp)
w2 = Worker2(mp)
w1.start()
w2.start()
