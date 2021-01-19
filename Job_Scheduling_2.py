# Author : Piyush Chopra
# Python Assignment

import random
from collections import namedtuple
#Question2
def GenNumJob( cdf_list, value_list ):
    rnd = random.random()
    for i in range( 0, len( cdf_list ) ):
        if rnd < cdf_list[ i ]:
            return value_list[ i ]

# Function that generates the processing time and extra time for a job
# INPUT: a list - a CDF for the distribution of proc_time, and
# a list - a CDF for the distribution of extra_time (allowed to comlete the job)
# assuming that the values for proc_time are 1, 2, 3, ...
# and the values for extra_time are 0, 1, 2, ...
# RETURNS: a list comprised of the job's proc_time and proc_time + extra_time
def GenJobFeat( cdf_list_proc, cdf_list_extra ):
    rnd = random.random()
    for i in range( 0, len( cdf_list_proc ) ):
        if rnd < cdf_list_proc[ i ]:
            return_value_1 = i + 1
            break
    rnd = random.random()
    for j in range( 0, len( cdf_list_extra ) ):
        if rnd < cdf_list_extra[ j ]:
            return_value_2 = j
            break
    return [ return_value_1, return_value_1 + return_value_2 ]


# HERE THE SIMULATION BEGINS
# FIRST, SPECIFY ALL THE INPUTS OF MY PROBLEM INSTANCE
job_num_cdf = [ .40, .85, 1 ]
job_num_values = [ 0, 1, 2 ]
job_proc_time = [ .65, 0.9, 1 ]
job_extra_time_allowed = [ 0.25, 0.85, 0.9, 0.95, 1 ]


# FUNCTION SIMULATES JOBS WITH THERE PROCESSING TIME AND EXTRA TIME ALLOWED
#INPUTS : TIME PERIOD OF THE SIMULATION
#OUTPUT: A LIST OF JOBS WITH THEIR PROCESSING TIME AND EXTRA TIME ALLOWED

def simulateJobs(T):

    all_jobs = []
    for i in range( 0, T ):
        number_jobs_this_period = GenNumJob( job_num_cdf, job_num_values )
        if number_jobs_this_period == 0:
            all_jobs.append( 0 )
        else:
            new_jobs = []
            for i in range( 0, number_jobs_this_period ):
                new_jobs.append( GenJobFeat( job_proc_time, job_extra_time_allowed ) )
            all_jobs.append( new_jobs )

    return all_jobs


# FUNCTION: FUNCTION THAT RETURNS SEQUENCE OF JOBS IN THE "EARLIEST DUE DATE " SCHEME AND PERFORANCE MEASURES
# INPUT: TIME PERIOD OF SIMULATION, LIST OF SIMULATED JOBS
# OUTPUT:NAMED TUPLE CONTAINING SEQUENCE OF JOBS AND OTHER JOB PARAMETERS, PERFORMANCE METRICS JOB TARDINESS, JOB EARLINESS, JOB WAITING TIME, MAKESPAN ,UTILISATION

def Ed(T,all_jobs):


    Job = namedtuple("Job", ['index', 'period_arrived', 'waitingtime','processing_time','extra_time_allowed','period_completed', 'due_period','job_lateness', 'job_earliness'])
    seq_jobs2=[]
    r=1
    waitingtime=0
    job_waitingtime=[]
    Q=[]
    due_date_list=[]
    for i in range(len(all_jobs)):
        if i==0:
            if all_jobs[i] !=0:
                for j in range(len(all_jobs[i])):
                    Q.append(all_jobs[i][j])
                    due_date_list.append(i + all_jobs[i][j][1])
                for j in range(len(due_date_list)):
                    x= due_date_list[j]
                    y= Q[j]
                    k=j-1
                    while k>= 0 and due_date_list[k] > x :
                        due_date_list[k+1] = due_date_list[k]
                        Q[k+1] = Q[j]
                        k= k-1
                    due_date_list[k+1]=x
                    Q[k+1]=y
                for p in range(len(Q)):
                    job_waitingtime.append(0)
                if len(Q)!=0:
                    if len(Q)>1:
                        for p in range(1,len(Q)):
                            job_waitingtime[p]= job_waitingtime[p] + Q[p-1][0]
        else:
            if all_jobs[i] !=0:
                for j in range(len(all_jobs[i])):
                    Q.append(all_jobs[i][j])
                    due_date_list.append(i + all_jobs[i][j][1])
                    job_waitingtime.append(0)
                for j in range(len(due_date_list)):
                    x= due_date_list[j]
                    y= Q[j]
                    z= job_waitingtime[j]
                    k=j-1
                    while k>= 0 and due_date_list[k] > x :
                        due_date_list[k+1] = due_date_list[k]
                        Q[k+1] = Q[k]
                        job_waitingtime[k+1]=job_waitingtime[k]
                        k= k-1
                due_date_list[k+1]=x
                Q[k+1]=y
                job_waitingtime[k+1]=z
        if len(Q)!=0:
            if len(Q)>1:
                for p in range(1,len(Q)):
                    job_waitingtime[p]= job_waitingtime[p] + Q[p-1][0]
            if waitingtime==0:
                seq_jobs2.append(Job(r,i,job_waitingtime[0],Q[0][0],Q[0][1],i+job_waitingtime[0]+Q[0][0],i+Q[0][1],0 if job_waitingtime[0]+Q[0][0] < Q[0][1] else job_waitingtime[0]+Q[0][0]-Q[0][1],0 if job_waitingtime[0]+Q[0][0] > Q[0][1] else Q[0][1]-job_waitingtime[0]-Q[0][0]))
                waitingtime= waitingtime+ Q[0][0]
                r=r+1
                Q.pop(0)
                due_date_list.pop(0)
                job_waitingtime.pop(0)
        if waitingtime>0:
            waitingtime=waitingtime-1



    sum_lateness=0
    sum_earliness=0
    sum_waitingtime=0
    sum_processing_time=0
    idle_time=0

    for i in range(len(seq_jobs2)):
        sum_lateness= sum_lateness + seq_jobs2[i].job_lateness
        sum_earliness= sum_earliness + seq_jobs2[i].job_earliness
        sum_waitingtime= sum_waitingtime + seq_jobs2[i].waitingtime
        sum_processing_time= sum_processing_time +seq_jobs2[i].processing_time

    for i in range(len(seq_jobs2)-1):
        idle_time= idle_time + ((seq_jobs2[i+1].period_completed-seq_jobs2[i+1].processing_time) - seq_jobs2[i].period_completed)

    average_hour_delay1= (sum_lateness* 1.0)/len(seq_jobs2)
    average_earliness1= (sum_earliness* 1.0)/len(seq_jobs2)
    average_job_waitingtime1= (sum_waitingtime* 1.0)/len(seq_jobs2)

    makespan1= seq_jobs2[len(seq_jobs2)-1].period_completed
    utilisation1=  (sum_processing_time*1.0)/(sum_processing_time+ idle_time)

    return average_hour_delay1,average_earliness1,average_job_waitingtime1,idle_time,makespan1,utilisation1


# FUNCTION FUNCTION THAT RETURNS SEQUENCE OF JOBS IN THE "SHORTEST PROCESSING TIME " SCHEME AND PERFORANCE MEASURES
# INPUT: TIME PERIOD OF SIMULATION, LIST OF SIMULATED JOBS
# OUTPUT:NAMED TUPLE CONTAINING SEQUENCE OF JOBS AND OTHER JOB PARAMETERS, PERFORMANCE METRICS JOB TARDINESS, JOB EARLINESS, JOB WAITING TIME, MAKESPAN ,UTILISATION

def ShortestProcessingTime(T,all_jobs):

    Job = namedtuple("Job", ['index', 'period_arrived', 'waitingtime','processing_time','extra_time_allowed','period_completed', 'due_period','job_lateness', 'job_earliness'])
    seq_jobs3=[]
    r=1
    waitingtime=0
    job_waitingtime=[]
    shortest_processing_time=[]
    Q=[]
    for i in range(len(all_jobs)):
        if i==0:
            if all_jobs[i] !=0:
                for j in range(len(all_jobs[i])):
                    Q.append(all_jobs[i][j])
                    shortest_processing_time.append(all_jobs[i][j][0])
                for j in range(len(shortest_processing_time)):
                    v= shortest_processing_time[j]
                    y= Q[j]
                    k=j-1
                    while k>= 0 and shortest_processing_time[k] > v :
                        shortest_processing_time[k+1] = shortest_processing_time[k]
                        Q[k+1] = Q[j]
                        k= k-1
                    shortest_processing_time[k+1] =v
                    Q[k+1]=y
                for p in range(len(Q)):
                    job_waitingtime.append(0)
                if len(Q)!=0:
                    if len(Q)>1:
                        for p in range(1,len(Q)):
                            job_waitingtime[p]= job_waitingtime[p] + Q[p-1][0]

        else:
            if all_jobs[i] !=0:
                for j in range(len(all_jobs[i])):
                    Q.append(all_jobs[i][j])
                    shortest_processing_time.append(all_jobs[i][j][0])
                    job_waitingtime.append(0)
                for j in range(len(shortest_processing_time)):
                    v=shortest_processing_time[j]
                    y= Q[j]
                    z= job_waitingtime[j]
                    k=j-1
                    while k>= 0 and shortest_processing_time[k] > v :
                        shortest_processing_time[k+1]=shortest_processing_time[k]
                        Q[k+1] = Q[k]
                        job_waitingtime[k+1]=job_waitingtime[k]
                        k= k-1
                shortest_processing_time[k+1] =v
                Q[k+1]=y
                job_waitingtime[k+1]=z
        if len(Q)!=0:
            if len(Q)>1:
                for p in range(1,len(Q)):
                    job_waitingtime[p]= job_waitingtime[p] + Q[p-1][0]
            if waitingtime==0:
                seq_jobs3.append(Job(r,i,job_waitingtime[0],Q[0][0],Q[0][1],i+job_waitingtime[0]+Q[0][0],i+Q[0][1],0 if job_waitingtime[0]+Q[0][0] < Q[0][1] else job_waitingtime[0]+Q[0][0]-Q[0][1],0 if job_waitingtime[0]+Q[0][0] > Q[0][1] else Q[0][1]-job_waitingtime[0]-Q[0][0]))
                waitingtime= waitingtime+ Q[0][0]
                r=r+1
                Q.pop(0)
                job_waitingtime.pop(0)
                shortest_processing_time.pop(0)
        if waitingtime>0:
            waitingtime=waitingtime-1



    sum_lateness=0
    sum_earliness=0
    sum_waitingtime=0
    sum_processing_time=0
    idle_time=0

    for i in range(len(seq_jobs3)):
        sum_lateness= sum_lateness + seq_jobs3[i].job_lateness
        sum_earliness= sum_earliness + seq_jobs3[i].job_earliness
        sum_waitingtime= sum_waitingtime + seq_jobs3[i].waitingtime
        sum_processing_time= sum_processing_time +seq_jobs3[i].processing_time
    for i in range(len(seq_jobs3)-1):
        idle_time= idle_time + ((seq_jobs3[i+1].period_completed-seq_jobs3[i+1].processing_time) - seq_jobs3[i].period_completed)

        average_hour_delay2= (sum_lateness* 1.0)/len(seq_jobs3)
        average_earliness2= (sum_earliness* 1.0)/len(seq_jobs3)
        average_job_waitingtime2= (sum_waitingtime* 1.0)/len(seq_jobs3)

        makespan2= seq_jobs3[len(seq_jobs3)-1].period_completed
        utilisation2=  (sum_processing_time*1.0)/(sum_processing_time+ idle_time)

    return average_hour_delay2,average_earliness2,average_job_waitingtime2,idle_time,makespan2,utilisation2

# OUTPUT OF "EARIEST DUE DATE" AND "SHORTEST PROCESSING TIME" for T=10,100,1000

all_jobs1= simulateJobs(10)
all_jobs2 = simulateJobs(100)
all_jobs3 = simulateJobs(1000)
print Ed(10,all_jobs1)
print ShortestProcessingTime(10, all_jobs1)
print Ed(100,all_jobs2)
print ShortestProcessingTime(100,all_jobs2)
print Ed(1000,all_jobs3)
print ShortestProcessingTime(1000,all_jobs3)
