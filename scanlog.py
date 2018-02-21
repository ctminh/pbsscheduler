import re
import time
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import os
import matplotlib.pyplot as plt

# DEFINE SOME STRING
JOB_QUEUED = "Job Queued"
JOB_RUN = "Job Run"
JOB_END = "Exit_status"

# ###############################################################
# Define a class of jobs in HPC system
# ###############################################################
class Job:
    def __init__(self, id):
        self.id = id

    def add_name(self, name):
        self.name = name
        self.end_time = datetime.strptime('01/01/2018 00:00:00', '%m/%d/%Y %H:%M:%S')
        self.cpu_percent = 0
        self.cpu_time = 0
        self.vmem = 0

    def add_queuedtime(self, queued_time):
        self.queued_time =queued_time

    def add_walltime(self, walltime):
        self.walltime = walltime

    def add_rcpu(self, r_cpu):
        self.r_cpu = r_cpu

    def add_rmem(self, r_mem):
        self.r_mem = r_mem

    def add_rdisk(self, r_disk):
        self.r_disk = r_disk

    def add_start_time(self, start_time):
        self.start_time = start_time

    def add_end_time(self, end_time):
        self.end_time = end_time

    def add_acpu(self, a_cpu):
        self.a_cpu = a_cpu

    def add_amem(self, a_mem):
        self.a_mem = a_mem

    def add_adisk(self, a_disk):
        self.a_disk = a_disk

    def add_cpupercent(self, cpu_percent):
        self.cpu_percent = cpu_percent

    def add_cputime(self, cpu_time):
        self.cpu_time = cpu_time

    def add_vmem(self, vmem):
        self.vmem = vmem

    def add_turnaroundtime(self, turnaroundtime):
        self.turnaroundtime = turnaroundtime

    def add_responsetime(self, responsetime):
        self.responsetime = responsetime

    def add_executiontime(self, executiontime):
        self.executiontime = executiontime

    def add_waitingtime(self, waitingtime):
        self.waitingtime = waitingtime

    def add_bsld(self, bsld_value):
        self.bsld = bsld_value

    # def add_score(self, score):
    #     self.score = score

# ---------------------------------------------------------------
# Function: findIndex() is to find the index of a job in the list
# Return: index of a job
# ---------------------------------------------------------------
def findIndex(jid, listOfJobs = []):
    for index, item in enumerate(listOfJobs):
        if item.id == jid:
            break
        else:
            index = -1
    return index

# ---------------------------------------------------------------
# Function: print a list of jobs
# ---------------------------------------------------------------
def print_jobs(listofJobs = [], numofJobs = 0):
    for index, job in enumerate(listofJobs):
        # print 'job ', job.id, ': \n name - ', job.name,\
        #     '\n queue_time - ', job.queued_time,\
            # '\n wall time - ', job.wall_time, \
            # '\n r_cpu - ', job.r_cpu, \
            # '\n r_mem - ', job.r_mem, \
            # '\n r_disk - ', job.r_disk, \
            # '\n start time - ', job.start_time,\
            # '\n a_cpu - ', job.a_cpu, \
            # '\n a_mem - ', job.a_mem, \
            # '\n a_disk - ', job.a_disk, \
            # '\n end time - ', job.end_time,\
            # '\n cpu_percent - ', job.cpu_percent,\
            # '\n cpu_time - ', job.cpu_time,\
            # '\n vmem - ', job.vmem,\
            # '\n--------------------------'\
            # '\n'
        print 'job ', job.id, ': \n name - ', job.name,\
            '\n queue_time - ', job.queued_time, \
            '\n start time - ', job.start_time, \
            '\n end time - ', job.end_time, \
            '\n cpu_percent - ', job.cpu_percent,\
            '\n cpu_time - ', job.cpu_time,\
            '\n vmem - ', job.vmem,\
            '\n--------------------------'\
            '\n'
    print   '############################'
    print   'Number of jobs = ', numofJobs
    print   '############################'


# ---------------------------------------------------------------
# Function: write a new logfiles for job info
# ---------------------------------------------------------------
def writeOutput(outputfile, listofJobs = [], numofJobs = 0, AVEwt = 0, AVEtat = 0, AVEte = 0, AVEth = 0, AVEbsld = 0):
    output = open(outputfile, "w")
    output.write("-------------------------------------------------------------------------------------------\n")
    output.write("Job ID \t | Submit time \t\t\t | Start time \t\t\t | End time \t\t\t | Runtime \t | Job name\n")
    output.write("-------------------------------------------------------------------------------------------\n")
    for index, job in enumerate(listofJobs):
        output.write("{0}:\t {1} \t {2} \t {3} \t {4} \t {5}\n" \
                     .format(job.id, job.queued_time, job.start_time, job.end_time, job.executiontime, job.name))
    output.write("-------------------------------------------------------------------------------------------\n")
    output.write("The total number of jobs: {0}\n".format(numOfJobs))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.write("FCFS AVE_waitingtime: {0}s\n".format(AVEwt))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.write("FCFS AVE_turnaroundtime: {0}s\n".format(AVEtat))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.write("FCFS AVE_totalexectime: {0} hours\n".format(AVEte))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.write("FCFS AVE_throughput: {0} jobs/hour\n".format(AVEth))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.write("FCFS AVE_bsld: {0}\n".format(AVEbsld))
    output.write("-------------------------------------------------------------------------------------------\n")

    output.close()

# ---------------------------------------------------------------
# Scan log files to get all of information for a list of jobs
# Create a list of job for easily to access elements
# ---------------------------------------------------------------
def scanDB(filenames):
    list_jobs = []
    count = []
    numofJobs = 0
    for file in filenames:
        with open(file, 'r') as f:
            for line in f:
                if line.__contains__(JOB_QUEUED):
                    content = line.split(';')
                    # print content
                    jid = content[4].split('.')[0]
                    jname = content[5].split(',')[2].split('=')[1]
                    queued_time = datetime.strptime(content[0], '%m/%d/%Y %H:%M:%S')

                    # Store: name, queued_time, id of a job
                    j = Job(jid)
                    j.add_name(jname)
                    j.add_queuedtime(queued_time)
                    list_jobs.append(j)

                    # Count the number of jobs submitted
                    numofJobs += 1

                    # Store index by count to trace the position of job in the list
                    count.append(0)

                    # print 'job ', jid, ': \n name -', jname,\
                    #     '\n queue_time -', queued_time,\
                    #     '\n walltime -', wall_time,\
                    #     '\n r_cpu -', r_cpu,\
                    #     '\n r_mem -', r_mem,\
                    #     '\n r_disk -', r_disk,\
                    #     '\n--------------------------'

                if line.__contains__(JOB_RUN):
                    content = line.split(';')
                    # print content
                    jid = content[4].split('.')[0]

                    # Find index of the job
                    index = findIndex(jid, list_jobs)

                    # If the number of JOB_RUN line > 0, do not store information
                    if count[index] == 0:
                        start_time = datetime.strptime(content[0], '%m/%d/%Y %H:%M:%S')

                        # Store: start_time of each job
                        list_jobs[index].add_start_time(start_time)

                        # print 'job ', jid, ': \n start_time -', start_time,\
                        #     '\n a_cpu -', a_cpu,\
                        #     '\n a_mem -', a_mem,\
                        #     '\n a_disk -', a_disk,\
                        #     '\n a_mem -', a_mem,\
                        #     '\n exe_nodes -', exe_nodes,\
                        #     '\n--------------------------'
                    else:
                        count[index] += 1

                if line.__contains__(JOB_END):
                    content = line.split(';')
                    # print content
                    jid = content[4].split('.')[0]

                    # Find index of the job
                    index = findIndex(jid, list_jobs)

                    # Get info: end_time, cpu_usage, cpu_percent
                    end_time = datetime.strptime(content[0], '%m/%d/%Y %H:%M:%S')

                    cpu_p = content[5].split(' ')[1].split('=')[1]
                    cpu_percent = map(float, re.findall('\d+', cpu_p))[0]

                    cpu_info = content[5].split(' ')[4].split('=')[1]
                    ncpu = map(float, re.findall('\d+', cpu_info))[0]

                    cpu_time = datetime.strptime(content[5].split(' ')[2].split('=')[1], '%H:%M:%S')

                    vmem_info = content[5].split(' ')[5].split('=')[1].split('k')[0]
                    vmem = map(float, re.findall('\d+', vmem_info))[0]

                    # Store: end_time, cpu_percent, ncpu, cpu_time, vmem
                    list_jobs[index].add_end_time(end_time)
                    list_jobs[index].add_cpupercent(cpu_percent)
                    list_jobs[index].add_acpu(ncpu)
                    list_jobs[index].add_cputime(cpu_time)
                    list_jobs[index].add_vmem(vmem)

                    # print 'job ', jid, ': \n end_time -', end_time,\
                    #     '\n cpu_percent -', cpu_percent,\
                    #     '\n cpu_time -', cpu_time,\
                    #     '\n vmem -', vmem,\
                    #     '\n--------------------------'

    return list_jobs, numofJobs


# ---------------------------------------------------------------
# Function: calculate turn around time of jobs submitted
# Return:
# ---------------------------------------------------------------
def job_turn_around_time(listofJobs = [], numofJobs = 0):
    # The turnaround time of a job is defined
    # as the time at which the job completes minus the time at which the job
    # arrived in the system. More formally, the turnaround time Tturnaround is
    # Tturnaround = Tcomplete - Tarrival
    sum_turnaroundtime = 0.0
    for index, job in enumerate(listofJobs):
        turnaroundtime = job.end_time - job.queued_time
        job.add_turnaroundtime(turnaroundtime)
        sum_turnaroundtime += turnaroundtime.seconds
        # print 'Job ', job.id, ' - ',job.name, ': \tqueued_time=', job.queued_time,\
        #     ', end_time=', job.end_time, ', turnaroundtime=',job.turnaroundtime,\
        #     '(', job.turnaroundtime.seconds, 's)|'
    AVE_turnaroundtime = float(sum_turnaroundtime / numofJobs)
    # print "AVE TurnAround Time = {} / {} =  {}".format(sum_turnaroundtime, numofJobs, AVE_turnaroundtime)
    return AVE_turnaroundtime


# ---------------------------------------------------------------
# Function: calculate execution time for each job and total execution time
# Return: total_executiontime
# ---------------------------------------------------------------
def total_executiontime(listofJobs = []):
    lastendtime = max(job.end_time for job in listofJobs)
    total_exectime = (lastendtime - listofJobs[0].start_time)
    for index, job in enumerate(listofJobs):
        executiontime = job.end_time - job.start_time
        job.add_executiontime(executiontime)
    #     print 'Job ', job.id, ' - ', job.name, ': \tstart_time=', job.start_time,\
    #         ', end_time=', job.end_time, ', executiontime=', job.executiontime,\
    #         '(', job.executiontime.seconds, 's)|'

    # print   'Total execution time = last_job.endtime - first_job.starttime = ',\
    #           lastendtime, ' - ', listofJobs[0].start_time, ' = ', total_exectime
    return total_exectime.seconds / 3600.0


# ---------------------------------------------------------------
# Function: calculate the througput
# Return: num of jobs / hour
# ---------------------------------------------------------------
def throughput(total_executiontime, numofJobs):
    throughput = float(numofJobs / total_executiontime)
    # print 'Throughput = numofJobs / total_executiontime = ', numofJobs, ' / ', total_executiontime,\
    #     ' = ', throughput, 'jobs/hour'
    return throughput


# ---------------------------------------------------------------
# Function: calculate waiting time of each job
# Return:
# ---------------------------------------------------------------
def job_waitingtime(listofJobs = [], numofJobs = 0):
    sum_waitingtime = 0.0
    for index, job in enumerate(listofJobs):
        waiting_time = job.start_time - job.queued_time
        job.add_waitingtime(waiting_time)
        sum_waitingtime += waiting_time.seconds
        # print 'Job ', job.id, ' - ', job.name, ': \tstart_time=', job.start_time,\
        #     ', queued_time=', job.queued_time,', waitingtime=', job.waitingtime,\
        #     '(', job.waitingtime.seconds, 's)|'
    AVEWaitingTime = float(sum_waitingtime / numofJobs)
    # print "AVE Waiting Time = {} / {} =  {}" .format(sum_waitingtime, numofJobs, AVEWaitingTime)
    return AVEWaitingTime

# ---------------------------------------------------------------
# Function: Objective function - Bounded Slowdown
# Return: bsld = max( (w(i) + p(i))/max(p(i), t), 1 )
# ---------------------------------------------------------------
def bsld(listofJobs = [], t = 0):
    bsld_list = []
    for index, job in enumerate(listofJobs):
        sum_w_p = float(job.waitingtime.seconds + job.executiontime.seconds)
        max_p_t = float(max(job.executiontime.seconds, t))
        bsld_value = max(sum_w_p / max_p_t, 1.0)
        job.add_bsld(bsld_value)
        bsld_list.append(bsld_value)
        # print 'Job ', job.id, ' - ', job.name, ': \twaiting_time=', job.waitingtime.seconds, \
        #     ', execution_time=', job.executiontime.seconds,\
        # ', bsld = max(', (sum_w_p / max_p_t), ',', 1.0, ') = ', job.bsld, '|'

    return bsld_list


# ---------------------------------------------------------------
# Function: Average Bounded Slowdown
# Return: AVEbsld(T) = (1/T) * Sum[max( (w(i) + p(i))/max(p(i), t), 1 )]
# ---------------------------------------------------------------
def AVEbsld(listofJobs = [], numofJobs = 1):
    sum_bsld = 0.0
    for index, job in enumerate(listofJobs):
        sum_bsld += job.bsld

    AVEbsld_value = sum_bsld / numofJobs
    # print 'AVEbsld = sum_bsld / numofJobs = ', sum_bsld, ' / ', numofJobs, ' = ', AVEbsld_value, '|'
    return AVEbsld_value



# ###############################################################
# Function: Main Function
# Return:
# ###############################################################
if __name__ == '__main__':

    # FCFS Policy
    # outputfile = "logfiles/FCFS_20180219.swf"
    # list_of_files = ["logfiles/20180216", "logfiles/20180217"]
    # jobs_FCFS, numOfJobs = scanDB(list_of_files)
    # FCFS_avewaitingtime = job_waitingtime(jobs_FCFS, numOfJobs)
    # FCFS_turnaroundtime = job_turn_around_time(jobs_FCFS, numOfJobs)
    # FCFS_totalexectime = total_executiontime(jobs_FCFS)
    # FCFS_throughput = throughput(FCFS_totalexectime, numOfJobs)
    # bsld(jobs_FCFS, 10)
    # FCFS_AVEbsld = AVEbsld(jobs_FCFS, numOfJobs)
    # writeOutput(outputfile,\
    #             jobs_FCFS,\
    #             numOfJobs,\
    #             FCFS_avewaitingtime,\
    #             FCFS_turnaroundtime,\
    #             FCFS_totalexectime,\
    #             FCFS_throughput,\
    #             FCFS_AVEbsld)

    # SJF Policy
    # list_of_files = ["logfiles/20180218", "logfiles/20180219"]
    # outputfile = "logfiles/SJF_20180219.swf"
    # jobs_SJF, numOfJobs = scanDB(list_of_files)
    # SJF_avewaitingtime = job_waitingtime(jobs_SJF, numOfJobs)
    # SJF_turnaroundtime = job_turn_around_time(jobs_SJF, numOfJobs)
    # SJF_totalexectime = total_executiontime(jobs_SJF)
    # SJF_throughput = throughput(SJF_totalexectime, numOfJobs)
    # bsld(jobs_SJF, 10)
    # SJF_AVEbsld = AVEbsld(jobs_SJF, numOfJobs)
    # writeOutput(outputfile,\
    #             jobs_SJF,\
    #             numOfJobs,\
    #             SJF_avewaitingtime,\
    #             SJF_turnaroundtime,\
    #             SJF_totalexectime,\
    #             SJF_throughput,\
    #             SJF_AVEbsld)

    # LJF Policy
    list_of_files = ["logfiles/20180219new", "logfiles/20180220"]
    outputfile = "logfiles/LJF_20180220.swf"
    jobs_LJF, numOfJobs = scanDB(list_of_files)
    LJF_avewaitingtime = job_waitingtime(jobs_LJF, numOfJobs)
    LJF_turnaroundtime = job_turn_around_time(jobs_LJF, numOfJobs)
    LJF_totalexectime = total_executiontime(jobs_LJF)
    LJF_throughput = throughput(LJF_totalexectime, numOfJobs)
    bsld(jobs_LJF, 10)
    LJF_AVEbsld = AVEbsld(jobs_LJF, numOfJobs)
    writeOutput(outputfile,\
                jobs_LJF,\
                numOfJobs,\
                LJF_avewaitingtime,\
                LJF_turnaroundtime,\
                LJF_totalexectime,\
                LJF_throughput,\
                LJF_AVEbsld)
