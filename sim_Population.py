import random
import statistics
import numpy as np
from numpy import genfromtxt
import pandas as pd
import json 
import numpy

#--------------------------------------------------------------------------
# GLOBAL VARIABLES

people = []
population_list = []
food_level_list = []
disasters = {}
total_food = 0

#--------------------------------------------------------------------------
# PARAMETERS

init_population = 50
pregenancy_rate = 0.2
infant_mortality_rate = 0.05
fertelity_x = 18
fertelity_y = 35
productivity = 5 

init_age_low_limit = 18
init_age_high_limit = 50

death_age = 80

disaster_probability = 0.1
disaster_impact_Population_low = 0.05
disaster_impact_Population_high = 0.15

stopping_populaiton_limit = 100000

#--------------------------------------------------------------------------
# CLASSES

class Person(object):
    def __init__(self, initial_age = 0):
        self.gender = self.gender_generator()
        self.age = initial_age
        
    def gender_generator(self):
        self.alias = random.randint(1, 3)
        if self.alias == 2:
            _gender = 'Male'
        else:
            _gender = 'Female'
        return _gender
             

#--------------------------------------------------------------------------
# FUNCTIONS
def age_generator():
    " generate random age between [18,50] for initial population "
    age = numpy.random.randint(init_age_low_limit, init_age_high_limit+1)
    return age  
     

def harvest(people):
    " calculate how much food is produced in a year by counting able people to produce food "
    able_people = 0  
    for p in people:
        if p.age > 8:
            able_people = able_people + 1
            
    return productivity * able_people

def reproduce(people):
    for p in people:
        if p.gender == 'Female' and p.age in range(fertelity_x, fertelity_y+1):
            temp_prob = random.uniform(0, 1)
            if temp_prob < pregenancy_rate:
                people.append(Person())
            
 
def age_decease(people):
    for p in people.copy():
        if p.age > death_age:
            people.remove(p)             
    
    
def infantMortality(people):
    for p in people.copy():
        if p.age == 0:
            temp_prob = random.uniform(0, 1)
            if temp_prob < infant_mortality_rate:
                people.remove(p)

def disasterChance(people, year, disasters):
    temp_prob1 = random.uniform(0, 1)
    if temp_prob1 < disaster_probability:
        impct_popul_rate = random.uniform(disaster_impact_Population_low, disaster_impact_Population_high)      
        impct_popul = impct_popul_rate * len (people)
        impct_popul = int (impct_popul)
        
        for i in range (impct_popul):
            p = random.choice(people)
            people.remove(p)

            disasters.update({year: impct_popul})

      
def beginSim():
    for i in range(0, init_population):
        people.append( Person(age_generator()) )
        

      
#--------------------------------------------------------------------------
# RUN SIMULATION 
def runYear (population_list, food_level_list, inf_mortality = 0, disaster_mortality = 0):

    beginSim()
    population = len(people)
    total_food = 0
    years = 0
    population_list.append(population)
    while (population > 0 and population < stopping_populaiton_limit):
        
        # 1. Use harvest function to find out if the food
        # will leave some people to starve to death, or if there is enough to be stored.
        total_food = total_food + harvest(people)
        if (total_food >= population):
            # no one dies of starvation
            # update total food
            total_food = total_food - population
        else:
            total_food = 0
            starvation_mortality = population - total_food
            
            for i in range (starvation_mortality):
                p = random.choice(people)
                people.remove(p)
                
        # 2. call reproduce function        
        reproduce(people)
        
        # 3. over 80 years death function:
        age_decease(people)
        
        # 4. infants Mortality
        if (inf_mortality == 1):
            infantMortality(people)
        
        # 5. disaster Chance
        if (disaster_mortality == 1):
            disasterChance(people, years, disasters)
        
        # 6. updates people's age:
        for p in people: 
            p.age = p.age + 1
        
        # 7. add a year
        years = years + 1
        
        population = len(people)
        population_list.append(population)
        food_level_list.append(total_food)
    #return:
    return total_food, years , population_list , food_level_list

#--------------------------------------------------------------------------

total_food1, years1 , population_list1, food_level_list1 = runYear (population_list, food_level_list)

#--------------------------------------------------------------------------
# refresh global variables for different run

people = []
population_list = []
food_level_list = []
disasters = {}
total_food = 0

total_food2, years2 , population_list2, food_level_list2 = runYear (population_list, food_level_list , inf_mortality = 1 )

#--------------------------------------------------------------------------
# refresh global variables for different run

people = []
population_list = []
food_level_list = []
disasters = {}
total_food = 0
total_food3, years3 , population_list3, food_level_list3 = runYear (population_list, food_level_list , inf_mortality = 1 , disaster_mortality = 1)

#--------------------------------------------------------------------------
# Visualization

from matplotlib import pyplot as plt
plt.plot(population_list)
plt.plot(population_list1, label='POPULATION ')
plt.plot(population_list2, label='POPULATION w Infant Mortality')
plt.plot(population_list3, label='POPULATION w Infant Mortality w Disasters')

plt.legend()
plt.xlabel("YEAR")
plt.ylabel("POPULATION")
plt.show()