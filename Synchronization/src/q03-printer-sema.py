from rvr import MP, MPthread
import random

MAX_JOBS = 4

# Q03:
#    Complete the implementation of the PrinterScheduler monitor below using
#    MP Semaphores.

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE ABOVE THIS LINE #############################
################################################################################

class PrinterScheduler(MP):
    """
    The PrinterScheduler handles printers and applications. Applications
    add jobs to a job queue, and printers finish the jobs from the job queue.

    Implement the scheduler such that the Application threads don't attempt to add
    jobs when the queue reached MAX_JOBS and the Printers don't attempt to process
    jobs when there are none to grab. 

    A Printer can process any single job that is on the queue, but each job can only
    be processed once. 
    """
    def __init__(self, max_jobs):
        MP.__init__(self)
        self.jobs = []
        self.job_queue = self.Semaphore('Max Job Sema', max_jobs)
        self.job_process = self.Semaphore('Processing Sema', 0)
        self.mutex_add = self.Semaphore('Add Sema', 1)
        self.mutex_process = self.Semaphore('Remove Sema', 1)

    def add_job(self, job_tuple):
        """Adds a job for it to be available to be processed. job_tuple unqiuely
        represents the job that was added. You should keep track of what is on the
        queue."""
        self.job_queue.procure()
        self.mutex_add.procure()
        self.jobs.append(job_tuple)
        self.mutex_add.vacate()
        self.job_process.vacate()
        

    def process_job(self):
        """Removes a job tuple, and RETURNS it."""
        self.job_process.procure()
        self.mutex_process.procure()
        job = self.jobs.pop(0)
        self.mutex_process.vacate()
        self.job_queue.vacate()
        return job

################################################################################
## DO NOT WRITE OR MODIFY ANY CODE BELOW THIS LINE #############################
################################################################################

class Application(MPthread):
    def __init__(self, scheduler, name, num):
        MPthread.__init__(self, scheduler, num)
        self.scheduler = scheduler
        self.name = name
        self.job_prefix = num * 100

    def run(self):
        for i in range(5):
            job_num = self.job_prefix + i
            print(self.name + ' is trying to add job ' + str(job_num))
            self.scheduler.add_job((self.name, job_num))
            print(self.name + ' has finished adding job ' + str(job_num))

class Printer(MPthread):
    def __init__(self, scheduler, name):
        MPthread.__init__(self, scheduler, name)
        self.scheduler = scheduler
        self.name = name

    def run(self):
        for i in range(5):
            print(self.name + ' is trying to process a job')
            item = self.scheduler.process_job()
            print(self.name + ' has finished processing job ' + str(item))

if __name__ == "__main__":
    b = PrinterScheduler(MAX_JOBS)
    for i in range(3):
        Application(b, "Printer" + str(i+1), i+1).start()
        Printer(b, "Application" + str(i+1)).start()

    b.Ready()