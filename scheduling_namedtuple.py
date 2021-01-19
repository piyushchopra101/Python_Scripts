import random
import collections
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

def performance1(all_jobs):
    cumulative_time_for_job=0
    v=[]
    x=[]
    y=[0]
    he=0
    hd=0
    pick = []
    proc_time=[]
    for i in range (0,len(all_jobs)):
        if (all_jobs[i]>0):
            if len(all_jobs[i])>1:
                for j in range(0,len(all_jobs[i])):
                    cumulative_time_for_job=y[-1]+all_jobs[i][j][0]
                    x.append(cumulative_time_for_job)
                    y.append(max(cumulative_time_for_job,i+1))
                    schedule_pickup = i + all_jobs[i][j][1]
                    process_time=all_jobs[i][j][0]
                    proc_time.append(process_time)

                    pick.append(schedule_pickup)
                v.append(2)
            else:
                cumulative_time_for_job=y[-1]+all_jobs[i][0][0]
                x.append(cumulative_time_for_job)
                y.append(max(cumulative_time_for_job,i+1))
                schedule_pickup = i + all_jobs[i][0][1]
                pick.append(schedule_pickup)
                process_time=all_jobs[i][0][0]
                proc_time.append(process_time)
                v.append(1)

        else:
                y.append(max(0+cumulative_time_for_job,i+1))
                x.append(0)
                pick.append(0)
                proc_time.append(0)
                v.append(0)
                if y[i]<=i:
                    idle_time+=1




    for i in range(0,len(pick)):
        value = pick[i]-x[i]
        if value<0:
            hd=hd-value
        elif value>0:
            he=he+value
        else:
            continue
    average_hour_early=float(he)/(len([i for i,e in enumerate(x) if e != 0]))
    average_hour_delay=float(hd)/(len([i for i,e in enumerate(x) if e != 0]))
    makespan= max(x) - all_jobs.index(min([i for i,e  in enumerate(all_jobs) if e != 0]))


    return x,pick,average_hour_delay,average_hour_early,makespan,proc_time,v
# HERE THE SIMULATION BEGINS
# FIRST, SPECIFY ALL THE INPUTS OF MY PROBLEM INSTANCE
job_num_cdf = [ .40, .85, 1 ]
job_num_values = [ 0, 1, 2 ]
job_proc_time = [ .65, 0.9, 1 ]
job_extra_time_allowed = [ 0.25, 0.85, 0.9, 0.95, 1 ]
T = 5

# NOW BEGIN THE SIMULATION
#all_jobs = []
#for i in range( 0, T ):
#    number_jobs_this_period = GenNumJob( job_num_cdf, job_num_values )
#    if number_jobs_this_period == 0:
#        all_jobs.append( 0 )

 #   else:
#      new_jobs = []
#        for i in range( 0, number_jobs_this_period ):
#            new_jobs.append( GenJobFeat( job_proc_time, job_extra_time_allowed ) )
#        all_jobs.append( new_jobs )






Jobs = collections.namedtuple("Jobs",['index', 'processing_time','allotted_time'])
all_jobs = []

for i in range( 0, T ):
    number_jobs_this_period = GenNumJob( job_num_cdf, job_num_values )

    if number_jobs_this_period == 0:
        all_jobs.append( 0 )
        #job.insert(Jobs(i,0,0,0))
        #Jobs(*all_jobs)
    else:
        new_jobs = []
        #nj=[]
        for i in range( 0, number_jobs_this_period ):
            new_jobs.append( GenJobFeat( job_proc_time, job_extra_time_allowed ) )
            #due_date= i + new_jobs[i][1]

            #nj.insert(Jobs(i,new_jobs[i][0],new_jobs[i][1],due_date))
        all_jobs.append( new_jobs )
        #job.append(nj)

print all_jobs
print performance1(all_jobs)