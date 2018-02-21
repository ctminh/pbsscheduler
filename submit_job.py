import numpy as np
import re
import random
import subprocess
import sys
import os.path
import operator

INPUTFILE = "distribution/lublin_256.swf"
OUTPUTFILE = "distribution/output_edd.txt"
JOBDIR = "/home/ctminh/pbs/jobs/"
JOBS = ["open_telemac/submit_testcase1",
        "open_telemac/submit_testcase2",
        "open_telemac/submit_testcase3",
        "mic-jobs/4.01-overview-nbody/submit-job.sh",
        "mic-jobs/4.02-vectorization-data-structures-coulomb/submit-job.sh",
        "mic-jobs/4.03-vectorization-tuning-lu-decomposition/submit-job.sh",
        "mic-jobs/4.04-threading-misc-histogram/submit-job.sh",
        "mic-jobs/4.05-threading-insufficient-parallelism-sweep/submit-job.sh",
        "mic-jobs/4.06-threading-scheduling-jacobi/submit-job.sh",
        "mic-jobs/4.07-threading-affinity/submit-job.sh",
        "mic-jobs/4.08-memory-tiling-matrix_x_vector/submit-job.sh",
        "qe/submit-job.sh",
        "vast/si/submit-job.sh"
        ]

class Job:
    def __init__(self, id):
        self.id = id
        # self.submit_time = submit_time
        # self.run_time = run_time
        # self.num_nodes = num_nodes

    def add_submittime(self, submit_time):
        self.submit_time = submit_time

    def add_runtime(self, run_time):
        self.run_time = run_time

    def add_numnodes(self, num_nodes):
        self.num_nodes = num_nodes

# ----------------------------------------------------------
# -------------- Reading lublin_256.swf --------------------
# ----------------------------------------------------------
id = 0
joblist = []
for line in file(INPUTFILE):
  row = re.split(" +", line.lstrip(" "))
  if row[0] == ';':
    continue
  #print("%f %d" % (float(row[4]), int(row[5])))
  if int(row[4]) > 0 and int(row[4]) <= 256 and int(row[3]) > 0:
      j = Job(id)
      j.add_submittime(int(row[1]))
      j.add_runtime(int(row[3]))
      j.add_numnodes(int(row[4]))
      id += 1
      joblist.append(j)

# sorted_joblist = sorted(joblist, key=operator.attrgetter('submit_time'))

print("Passed Reading lublin_256.swf \n ---------------------------------------")

output = open(OUTPUTFILE, "w")
output.write("Job \t | Submit time \t | Run time \t | Job Type-ExecTime \t | Num nodes\n")
output.write("-------------------------------------------------\n")
real_job_exectime = [210, 240, 180, 15, 10, 5, 10, 10, 60, 30, 5, 1200, 600]
# total_waitingtime_for_submit = 0
# total_runtime = 0

for j in range(0, 1000):
    # print("{} \t   {} \t   {}".format(joblist[j].submit_time, joblist[j].run_time, joblist[j].num_nodes))
    if j == 0:
        waiting_for_time = 0
    else:
        waiting_for_time = (joblist[j].submit_time - joblist[j-1].submit_time) / 50

    if waiting_for_time > 300:
        waiting_for_time = 300

    job_type = joblist[j].run_time % 13
    exec_time = real_job_exectime[job_type]

    output.write("Job {0:2d}: {1:6d} \t {2:6d} \t {3:6d}-{4:6d} \t {5:6d}\n"\
                 .format(j, waiting_for_time, joblist[j].run_time, job_type, exec_time, joblist[j].num_nodes))

    subprocess.call(['qsub ' + JOBDIR + JOBS[job_type]], shell=True)
    # total_waitingtime_for_submit += waiting_for_time
    # total_runtime += exec_time
    if waiting_for_time > 0:
        print("Waiting for {0}s ...".format(waiting_for_time))
        subprocess.call(['sleep ' + str(waiting_for_time)], shell=True)

# print("Total waiting time for submitting job: {0}s\n".format(total_waitingtime_for_submit))
# print("Total runtime: {0}s\n".format(total_runtime))

output.write("Number of jobs: {}".format(len(joblist)))
output.close()