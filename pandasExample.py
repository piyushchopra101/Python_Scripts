#Working with Pandas. Introduction.

#Dictonaries
countries = ['spain', 'france', 'germany', 'norway']
capitals = ['madrid', 'paris', 'berlin', 'oslo']
# From string in countries and capitals, create dictionary europe
europe={"spain":"madrid",
        "france":"paris",
        "germany":"berlin",
        "norway":"oslo"}
# Print europe
print(europe["norway"])
# Print out the keys in europe
print(europe.keys())
#Add italy to europe
europe['italy']='rome'
# Remov
del(europe['italy'])
# Dictionary of dictionaries
europe = { 'spain': { 'capital':'madrid', 'population':46.77 },
           'france': { 'capital':'paris', 'population':66.03 },
           'germany': { 'capital':'berlin', 'population':80.62 },
           'norway': { 'capital':'oslo', 'population':5.084 } } 
# Print out the capital of France
print(europe['france']['capital'])
# Create sub-dictionary data
data ={'capital':'rome','population':59.83}
# Add data to europe under key 'italy'
europe["italy"] = data


"""Pandas"""
import pandas as pd
data = pd.read_csv("distance.csv")
print(data)
print(data[0:2])
print(data.loc[1:4])
print(data.iloc[1:4,1:3])
'''Dictionary to DataFrame (1)
The DataFrame is one of Pandas' most important data structures. 
It's basically a way to store tabular data, where you can label the rows and the columns. 
One way to build a DataFrame is from a dictionary.
'''
names = ['United States', 'Australia', 'Japan', 'India', 'Russia', 'Morocco', 'Egypt']
dr =  [True, False, False, False, True, True, True]
cpc = [809, 731, 588, 18, 200, 70, 45]
# Create dictionary dict with three key:value pairs: dict
dict={'country':names,'drives_right':dr,'cars_per_cap':cpc}

# Build a DataFrame cars from dict: cars
cars = pd.DataFrame(dict)

# Print cars
print(cars)
# Definition of row_labels
row_labels = ['US', 'AUS', 'JAP', 'IN', 'RU', 'MOR', 'EG']
# Specify row labels of cars
cars.index=row_labels

# Print cars again
print(cars)
#CSV to DataFrame (2)
cars = pd.read_csv('cars.csv',index_col=0)
# Print out cars
print(cars)

#Square Brackets (1)
# Print out country column as Pandas Series
print(cars['country'])

# Print out country column as Pandas DataFrame
print(cars[['country']])

# Print out DataFrame with country and drives_right columns
print(cars[['country','drives_right']])
# Print out first 3 observations
print(cars[0:3])

# Print out fourth, fifth and sixth observation
print(cars[3:6])
'''
With loc and iloc you can do practically any data selection operation on
 DataFrames you can think of. loc is label-based, which means that you have to
 specify rows and columns based on their row and column labels. iloc is integer
 index based, so you have to specify rows and columns by their integer index 
 like you did in the previous exercise.
'''
# Print out observation for Japan
print(cars.loc['JAP'])

# Print out observations for Australia and Egypt
print(cars.loc[['AUS','EG']])
# Print out drives_right value of Morocco
print(cars.loc['MOR','drives_right'])

# Print sub-DataFrame
print(cars.loc[['RU','MOR'],['country','drives_right']])
# Print out drives_right column as Series
print(cars.loc[:,'drives_right'])

# Print out drives_right column as DataFrame
print(cars.loc[:,['drives_right']])


# Print out cars_per_cap and drives_right as DataFrame
print(cars.iloc[:,[0,2]])


''' ##############  Filter Pandas DataFrame #############'''
cars = pd.read_csv('cars.csv', index_col = 0)

# Extract drives_right column as Series: dr
dr = cars["drives_right"]

# Use dr to subset cars: sel
sel = cars[dr==True]

# Print sel
print(sel)

# Create car_maniac: observations that have a cars_per_cap over 500
cpc=cars["cars_per_cap"]
many_cars= cpc > 500
car_maniac = cars[many_cars]

# Print car_maniac
print(car_maniac)

# Create medium: observations with cars_per_cap between 100 and 500
medium = cars[np.logical_and(cars["cars_per_cap"]<500,cars["cars_per_cap"]>100)]
# Print medium
print(medium)

