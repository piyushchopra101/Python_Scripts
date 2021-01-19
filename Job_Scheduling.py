import random
from collections import namedtuple

# Question 1 

# Function that generates the number of jobs to come
# INPUTS: a list - a CDF for the distribution of interest
# a list containing the values to which the CDF corresponds
# RETURNS: a value (coming randomly from this distribution)
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


# FUNCTION THAT RETURNS SEQUWNCE OF JOBS IN THE "FIRST COME FIRST SERVE " SCHEME AND PERFORANCE MEASURES
# INPUT: TIME PERIOD OF SIMULATION
# OUTPUT:NAMED TUPLE CONTAINING SEQUENCE OF JOBS AND OTHER JOB PARAMETERS, PERFORMANCE METRICS JOB TARDINESS, JOB EARLINESS, JOB WAITING TIME, MAKESPAN ,UTILISATION

def fc(T):

    Job = namedtuple("Job", ['index', 'period_arrived', 'waiting_time','processing_time','extra_time_allowed','period_completed', 'due_period','job_lateness', 'job_earliness'])#namedtuples
    seq_jobs=[]
    k=1
    all_jobs= simulateJobs(T)
    waiting_time=0
    for i in range(len(all_jobs)):
        if all_jobs[i] !=0:
            for j in range(len(all_jobs[i])):
                seq_jobs.append(Job(k,i,waiting_time,all_jobs[i][j][0],all_jobs[i][j][1],i+waiting_time+all_jobs[i][j][0],i+all_jobs[i][j][1],0 if waiting_time+all_jobs[i][j][0] < all_jobs[i][j][1] else waiting_time+all_jobs[i][j][0]-all_jobs[i][j][1],0 if waiting_time+all_jobs[i][j][0] > all_jobs[i][j][1] else all_jobs[i][j][1]-waiting_time-all_jobs[i][j][0]))
                waiting_time= waiting_time+ all_jobs[i][j][0]
                k=k+1
        if waiting_time>0:        
            waiting_time=waiting_time-1   

    sum_lateness=0
    sum_earliness=0
    sum_waiting_time=0
    sum_processing_time=0
    idle_time=0

    for i in range(len(seq_jobs)):
        sum_lateness= sum_lateness + seq_jobs[i].job_lateness
        sum_earliness= sum_earliness + seq_jobs[i].job_earliness
        sum_waiting_time= sum_waiting_time + seq_jobs[i].waiting_time
        sum_processing_time= sum_processing_time +seq_jobs[i].processing_time
    
    for i in range(len(seq_jobs)-1): 
        idle_time= idle_time + ((seq_jobs[i+1].period_completed-seq_jobs[i+1].processing_time) - seq_jobs[i].period_completed)

    average_hour_delay= (sum_lateness* 1.0)/len(seq_jobs)
    average_earliness= (sum_earliness* 1.0)/len(seq_jobs)
    average_job_waiting_time= (sum_waiting_time* 1.0)/len(seq_jobs)

    makespan= seq_jobs[len(seq_jobs)-1].period_completed
    utilisation= (sum_processing_time*1.0)/(sum_processing_time+ idle_time)

    return average_hour_delay,average_earliness,average_job_waiting_time,idle_time,makespan,utilisation


# GETTING FIRST SEVRVE FORST SERVE SEQUENCE AND PERFORMANCE FOR T=10,100,1000
print fc(10)
print fc(100)
print fc(1000)


