"""
# Name: John-Francis Caccamo
# Class: CS 372
# Date: 3 / 13 / 22
# Description: The Pokemon class file for Server vs Client Pokemon battle utizing the random module for
attack accuracy
"""

"""
README 

The program was done in Python3 (Python 3.8 , specifically) on PyCharm. 
finalProjectServer, finalProjectClient, Pokemon and commonFunctions need to all be in the same directory. 
Afterwards, all that is needed is to simply run finalProjectServer to create the socket, 
then subsequently finalProjectClient and switch terminals 
between them back and forth in order to proceed with the socket communication via the Pokemon battle between them.  

"""

import random

"""
The Pokemon class for Pokemon object creation, stats assigning and battle / damage facilitation 
"""


class Pokemon:
    pokemon_choices = {1: ["Charmander", "fire"], 2: ["Bulbasaur", "grass"], 3: ["Squirtle", "water"]}
    strongVs_dic = {"fire": "grass", "water": "fire", "grass": "water"}
    weakness_dic = {"fire": "water", "water": "grass", "grass": "fire"}
    moves_options = {"Charmander": ["fire blast", "scratch"], "Bulbasaur": ["bloom shot", "tackle"],
                     "Squirtle": ["water jet", "headbutt"]}
    move_stats = {"fire blast": [25, 50, True, "fire"], "bloom shot": [25, 50, True, "grass"],
                  "water jet": [25, 50, True, "water"], "scratch": [10, 75, False], "tackle": [10, 75, False],
                  "headbutt": [10, 75, False]}
    HEALTH = 100

    def __init__(self, choice):
        self._name = self.pokemon_choices[choice][0]
        self._type = self.pokemon_choices[choice][1]
        self._strongVs = self.strongVs_dic[self.get_type()]
        self._weakness = self.weakness_dic[self.get_type()]
        self._moves = self.moves_options[self._name]
        self._health = self.HEALTH

    """
    Series of getters 
    """
    def get_choices(self):
        return self.pokemon_choices

    def get_name(self):
        return self._name

    def get_health(self):
        return self._health

    def get_type(self):
        return self._type

    def get_strongVs(self):
        return self._strongVs

    def get_weakness(self):
        return self._weakness

    def get_health(self):
        return self._health

    def get_moves(self):
        return self._moves

    def get_move_stats(self):
        return self.move_stats

    # Deducts health if attack is successful
    def set_health(self, reduce_health):
        self._health -= reduce_health

    """
    perform_attack determines if attack lands and how much damage to assign
    the attacked Pokemon  
    """
    def perform_attack(self, attack):
        attack_stats = self.get_move_stats()[attack]
        attack_damage = attack_stats[0]
        attack_accuracy = attack_stats[1]
        attack_special = attack_stats[2]

        """
        Refresher for random module
        
        Citation: https://www.codegrepper.com/code-examples/python/generate+random+number+between+1+and+100+python
        
        Date: 3 / 7 / 21
        """

        # determine if attack is successful if randint is under the accuracy threshold
        attack_impact = random.randint(1, 101)

        if attack_impact <= attack_accuracy:
            if attack_special:

                # determine the type of the special attack
                attack_type = attack_stats[3]

                # if the attack type is what the Pokemon is weak vs
                if attack_type == self.get_weakness():
                    self.set_health(attack_damage + attack_damage * .1)

                # if the attack type is what the Pokemon is strong vs or if the Pokemon is of the same type
                # as the attack
                elif attack_type == self.get_type() or attack_type == self.get_strongVs():
                    self.set_health(attack_damage - attack_damage * .1)

                # none of the above - a clause for further Pokemon to add in the future! Electric, Rock, etc.
                else:
                    self.set_health(attack_damage + attack_damage * .05)
                print("SPECIAL ATTACK SUCCESSFUL")

            # normal attack landed
            else:
                self.set_health(attack_damage)
                print("NORMAL ATTACK SUCCESSFUL!!")

        else:
            print("ATTACK MISSED!!")

        return

    # publishes the stats, strengths, weaknesses and moves of the Pokemon object
    def info_and_stats_publisher(self):
        print(
            "\n" + self.get_name() + " is a " + self.get_type() + " Pokemon and it is strong vs " + self.get_strongVs()
            + " and it is weak against " + self.get_weakness())

        print("Its health is " + str(self.get_health()) + " and its moves include: ")

        for move in self.get_moves():
            print(move + " with a damage of " + str(self.get_move_stats()[move][0]) + " accuracy of " +
                  str(self.get_move_stats()[move][1]) + " and " +
                  str(self.get_move_stats()[move][2]) + " special damage against opponent who is weak vs it")

        return