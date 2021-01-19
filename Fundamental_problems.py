
#Programming for Analtics assognment 3
#Author : Piyush Chopra

import math

#problem 1
def my_func(a,b,c,arg_x ):
    q=math.pi                           # Using the math import we take the value of pi in q
    p=float(arg_x)
    f = (a*p**2*math.sin(b*q*p))+c      #This calculates the f(x) value by substituting it.
    return f                            # This reurns the value of f whenever it is called

def funcSearch(a, b, c, d, e,esp):
    low = float(d)                                                  #making the lower limit as low and making it into float value
    up = float(e)                                                   #making the upper limit as up and making it into float value
    prec = float(esp)                                               #make the precision a float value
    solution=low                                                    #initialize the solution as low
    current_value = my_func(a,b,c,solution )                        #Using the function to calculate the current value
    left_value = my_func( a,b,c,solution - prec )                   #Using the function to calculate the left value
    right_value = my_func( a,b,c,solution + prec )                  #Using the function to calculate the current value

    while current_value > left_value or current_value > right_value: #This loop heps to find local minima
        if solution<=up:                                            #This stops for value when it exeeds upper bound
            solution = solution + prec
        else:
            break
        current_value = my_func(a,b,c, solution )                   #this is an recursive loop
        left_value = my_func( a,b,c,solution - prec )
        right_value = my_func( a,b,c,solution + prec )
    if right_value<current_value:
        return 'there is no local minima in bounds'

    return [ [solution-prec,solution+prec], [left_value, right_value] ] #returns x and f(x) values
    
############Problem 2
def quadEqu (a,b,c):
    D=(b**2)-4*a*c    # Discriminant i.e b^2-4*a*c
    if a==0:
        return 'Error'  # This gives an error when it is zero
    elif(D<0):
        return 'Error'  # This also gives an error since discriminant is less than zero, hence the roots are imaginary
    elif(D==0):
        x=-b/2*a        #This formula holds good when the roots are equal and discriminant is zero
        print 'both roots are equal'
        x1=x
        x2=x
    else:
        e=math.sqrt(D)    # This does the square root of Discriminant
        x1=(-b+e)/2*a    # This gives one of the real root
        x2=(-b-e)/2*a    # This gives another real root
        print 'Both roots are different and real'
    return x1, x2

############Problem 3
def rpsGame (player1,hand1,player2,hand2):

    if((hand1 !='rock')and(hand1 !='paper')and(hand1 !='scissors')or((hand2 !='rock')and(hand2 !='paper')and(hand2 !='scissors'))):
        return 'Errror in spelling or not the correct type of hand'
    elif hand1==hand2:
        return 'no Winner'
    elif ((hand1=='paper' and hand2=='rock')or(hand1=='scissors' and hand2=='paper')or(hand1=='rock'and hand2=='scissors')):
        return player1
    else:
        return player2


############Problem 4    
def sortLastEl(list):
    x=len(list)
    for i in range(0,x-1):
        for j in range(0,x-1):
          a,b=list[j]
          c,d=list[j+1]
          if b>d:
              temp=list[j]
              list[j]=list[j+1]
              list[j+1]=temp
    return list



############Problem 5
def quadOpt (a,b,c):
    arg_a=float(a)
    arg_b=float(b)
    y=-arg_b/(2*arg_a)
    if a==0:
        return 'error'
    elif(a>0):
        x=a*(y**2)+(b*y)+c
        print 'Minimum at'
        return x
    else:
        x=a*(y**2)+(b*y)+c
        print 'Maximum at'
        return x

print funcSearch(1, 1, 0, 1, 2,0.05)
