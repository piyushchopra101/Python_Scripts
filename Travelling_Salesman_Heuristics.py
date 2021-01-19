import timeit
import math
import random

# Question 1
# code that returns the objective function of TSP - a tour's length
def obj( tour,my_matrix ):
    tour_length = 0
    for i in range( len( tour ) - 1 ):
        tour_length = tour_length + my_matrix[ tour[ i ] ][ tour[ i+1 ] ]
    return tour_length + my_matrix[ tour[ len(tour) - 1 ] ][ tour[ 0 ] ]
    
# This function returns an improving 2-opt neighbor of the current solution
# If neither neighbor is improving, it retuns an empty list


def randRestart2opt(C):
    start = timeit.default_timer()    
    my_matrix = []
    for city_from in range( len( C  ) ):
        my_matrix.append( [] )
        for city_to in range( len( C ) ):
            my_matrix[ city_from ].append( math.sqrt( (C[city_to][0] - C[city_from][0]) ** 2 + (C[city_to][1] - C[city_from][1]) ** 2) )
    
    a=[]
    for i in range(len(C)):
        a.append(i)
    def improve_tour( current ):
        b1 = 0
        b2 = 0
        for b1 in range( 0, len( current ) - 2  ):
            for b2 in range( b1 + 2, len( current ) ):
                candidate = list( current )
                candidate[ b1 : b2 ] = list( reversed( candidate[ b1 : b2 ] ) )
                delta = obj( candidate,my_matrix ) - obj( current,my_matrix )
                if delta < 0:
                   return( candidate )
# A local search algorithm using 2-opt begins here
# with R random restarts
    R = 30

    best_solution = a
    best_objective = obj( a, my_matrix )

    for iteration in range( 1, R ):
        random.shuffle( a )
        current = a
    
        continue_the_search = 1
        while continue_the_search == 1:
            result = improve_tour( current )
            if not result:
                continue_the_search = 0
            else:
                current = result
                print ' Current best solution = ', current, ' , Objective = ', obj( current,my_matrix )
    
        if obj( current,my_matrix ) < obj( best_solution,my_matrix ):
           best_solution = list( current )
           best_objective = obj( current,my_matrix )
           
    stop = timeit.default_timer()
    print stop-start
    return [best_solution, best_objective] 
    
# Question 2
    
def SimAn2opt(C):
    start = timeit.default_timer()  
    my_matrix = []
    for city_from in range( len( C  ) ):
        my_matrix.append( [] )
        for city_to in range( len( C ) ):
            my_matrix[ city_from ].append( math.sqrt( (C[city_to][0] - C[city_from][0]) ** 2 + (C[city_to][1] - C[city_from][1]) ** 2) )
    
    a=[]
    for i in range(len(C)):
        a.append(i)

############
# The simulated Annealing code begins here
############

# Set the simulated annealing parameters
    PHASES = 10 # how many times the temperature will be updated
    INITIAL_TEMPERATURE = 1 # the initial temperature (in the units of the problem)
    alpha = 0.08 # how fast the temperature will decrease
    ITERATIONS = 10000 # how many candidates to search through before updating the temperature

# Create the variables that will store the best solution (tour) found to date
    current = a

    TEMPERATURE = INITIAL_TEMPERATURE
# loop through the phases
    for phase_counter in range( 1, PHASES):
        print 'Phase counter is ', phase_counter
    # update the temperature
        TEMPERATURE = TEMPERATURE * alpha
    # loop through the iterations with a fixed temperature
        for iteration in range( 1, ITERATIONS):
            b1 = random.randint( 0, len( current ) - 2 )
            b2 = random.randint( b1 + 2, len( current ) )
        # generate the corresponding candidat esolution
            candidate = list( current )
            candidate[ b1 : b2 ] = list( reversed( candidate[ b1 : b2 ] ) )
        # find the difference between the value (tour length) of the candidate tour and
        # the current best known solution (tour)
            delta = obj( candidate, my_matrix ) - obj( current,my_matrix)
        # if the candidate has a better objective value
            if delta < 0:
            # then remember it as the current best solution
                current = candidate
            
             
            # if the candidate is not improving
            # check it still should be accepted
            # (we do this by generating a uniform random variable in [0, 1],
            # and if this random variable is less the the specified probability value,
            # then accept the candidate
            elif random.random() < math.exp( - delta / TEMPERATURE ):
                current = candidate
    stop = timeit.default_timer()
    print stop-start
    return  [current, obj( current, my_matrix)]




def randRestart3opt(C):
    
    start = timeit.default_timer() 
    my_matrix = []
    for city_from in range( len( C  ) ):
        my_matrix.append( [] )
        for city_to in range( len( C ) ):
            my_matrix[ city_from ].append( math.sqrt( (C[city_to][0] - C[city_from][0]) ** 2 + (C[city_to][1] - C[city_from][1]) ** 2) )
    
    a=[]
    for i in range(len(C)):
        a.append(i)

    def improve_tour1( current,my_matrix ):
        b1 = 0
        b2 = 0
        b3 = 0
        for b1 in range( 0, len( current ) - 3  ):
            for b2 in range( b1 + 3, len( current )-2 ):
                candidate = list( current )
                candidate[ b1: b2 ] = list( reversed( candidate[ b1 : b2 ] ) )
                for b3 in range(b2 + 2, len(current)): 
                
               
                    candidate[ b2 : b3 ] = list( reversed( candidate[ b2 : b3 ] ) )
                    delta = obj( candidate ,my_matrix) - obj( current,my_matrix )
                    if delta < 0:
                       return( candidate )
# A local search algorithm using 3-opt begins here
# with R random restarts
    R = 30

    best_solution = a
    best_objective = obj( a,my_matrix )

    for iteration in range( 1, R ):
        random.shuffle( a )
        current = a
    
        continue_the_search = 1
        while continue_the_search == 1:
            result = improve_tour1( current,my_matrix )
            if not result:
                continue_the_search = 0
            else:
                current = result
                print ' Current best solution = ', current, ' , Objective = ', obj( current,my_matrix )
    
        if obj( current,my_matrix ) < obj( best_solution,my_matrix ):
            best_solution = list( current )
            best_objective = obj( current,my_matrix )
    stop = timeit.default_timer()
    print stop-start 
    return [best_solution, best_objective]
    
    
def SimAn3opt(C):
    start = timeit.default_timer()
    my_matrix = []
    for city_from in range( len( C  ) ):
        my_matrix.append( [] )
        for city_to in range( len( C ) ):
            my_matrix[ city_from ].append( math.sqrt( (C[city_to][0] - C[city_from][0]) ** 2 + (C[city_to][1] - C[city_from][1]) ** 2) )
    
    a=[]
    for i in range(len(C)):
        a.append(i)
        
    ############
# The simulated Annealing code begins here
############

# Set the simulated annealing parameters
    PHASES = 10 # how many times the temperature will be updated
    INITIAL_TEMPERATURE = 1 # the initial temperature (in the units of the problem)
    alpha = 0.08 # how fast the temperature will decrease
    ITERATIONS = 10000 # how many candidates to search through before updating the temperature

# Create the variables that will store the best solution (tour) found to date
    current = a

    TEMPERATURE = INITIAL_TEMPERATURE
# loop through the phases
    for phase_counter in range( 1, PHASES):
        print 'Phase counter is ', phase_counter
    # update the temperature
        TEMPERATURE = TEMPERATURE * alpha
    # loop through the iterations with a fixed temperature
        for iteration in range( 1, ITERATIONS):
        # randomly generate the breakpoints for a segment to reverse the order of cities in
            b1 = random.randint( 0, len( current ) - 4 )
            b2 = random.randint( b1 + 2, len( current )-2 )
        # generate the corresponding candidat esolution
            candidate = list( current )
            candidate[ b1 : b2 ] = list( reversed( candidate[ b1 : b2 ] ) )
            b3= random.randint( b2 + 2, len( current ) )
            candidate[ b2 : b3 ] = list( reversed( candidate[ b2 : b3 ] ) )
        # find the difference between the value (tour length) of the candidate tour and
        # the current best known solution (tour)
            delta = obj( candidate,my_matrix ) - obj( current ,my_matrix)
        # if the candidate has a better objective value
            if delta < 0:
            # then remember it as the current best solution
               current = candidate
            # if the candidate is not improving
            # check it still should be accepted
            # (we do this by generating a uniform random variable in [0, 1],
            # and if this random variable is less the the specified probability value,
            # then accept the candidate
            elif random.random() < math.exp( - delta / TEMPERATURE ):
                 current = candidate    
    stop = timeit.default_timer()
    print stop-start
    return [current,obj(current,my_matrix)]
    
c=[[38.24, 20.42],[39.57, 26.15],[40.56 ,25.32],[36.26, 23.12],[33.48, 10.54],
 [37.56, 12.19],[38.42 ,13.11],[37.52, 20.44],[41.23, 9.10],[41.17, 13.05],[36.08, -5.21]
 ,[38.47, 15.13],[38.15 ,15.35],[37.51 ,15.17],[35.49, 14.32],[39.36, 19.56]]
 
print SimAn3opt(c)
    