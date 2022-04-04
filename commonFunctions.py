"""
# Name: John-Francis Caccamo


# Class: CS 372
# Date: 3 / 13 / 22
# Description: I created this file to modularize finalProjectServer and
# finalProjectClient and reduce the repetitive code structures shared by both.
"""

"""
README 

The program was done in Python3 (Python 3.8 , specifically) on PyCharm. 
finalProjectServer, finalProjectClient, Pokemon and commonFunctions need to all be in the same directory. 
Afterwards, all that is needed is to simply run finalProjectServer to create the socket, 
then subsequently finalProjectClient and switch terminals 
between them back and forth in order to proceed with the socket communication via the Pokemon battle between them.  

"""


# Simply prints the Pokemon options to the Server / Client user
def printPokemonOptions(name):
    print("\nAlright " + name +
          '\n...Choose your Pokemon... 1: Charmander = fire lizard, 2: Bulbasaur = grass dinosaur, 3: Squirtle = water '
          'creature')


"""
# Citation for the try/except structure for Pokemon Choice
# Date: 3 / 6 / 22 
# Source URL: https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# Author: Kevin 
"""


# decision validation for Pokemon and attack choice, will loop if erroneous input such as not integers
# or integers outside the acceptable range are entered
def pokemonAttackDecision(choice_msg, problem_msg, lower_bound, high_bound):
    choice = None

    while True:
        try:
            choice = input(choice_msg)

            # exit clause
            if choice == '/q':
                return choice
            else:
                # try to make client_choice an int
                choice = int(choice)

        # something other than an int has been entered
        except ValueError:
            print(problem_msg)
            continue

        # an integer outside of the range has been entered
        if choice < lower_bound or choice > high_bound:
            print("Please enter an integer from " + str(lower_bound) + " to " + str(high_bound))
            continue
        else:
            break

    return choice


# get the string attack data title associated with the integer user input
def assignAttackData(pokemon, attack_choice):
    attack_data = None

    if attack_choice == 1:
        attack_data = pokemon.get_moves()[0]
    if attack_choice == 2:
        attack_data = pokemon.get_moves()[1]

    return attack_data