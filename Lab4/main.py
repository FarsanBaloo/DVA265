import numpy as np
import GA as ga
import time
import random

class Bauhaus:
    def __init__(self):
        self.inventory = {"name": "Bauhaus",
                          "inventory": np.array([20, 20, 20, 20, 20, 20, 20]),
                          "money": 0
                          }

    def init_inventory(self):
        """ Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin"""

        inventory = {"name": "Bauhaus",
                      "inventory": np.array([20, 20, 20, 20, 20, 20, 20]),
                      "money": 0
                      }
        return inventory
    def Initiate_Bauhaus(self):
        pass


class Agent(Bauhaus):
    def __init__(self, name):
        self.inventory = self.init_inventory(name)

    def init_inventory(self):
        """
        Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin
        Modules: Floor, Bed room, bath room, living room, hall, garret
        """

        self.inventory = {"name": name,
                          "inventory": np.array([0, 0, 0, 0, 0, 0, 0]),
                          "money": 5000 * random.randint(10, 30),
                          "modules": np.array([0, 0, 0, 0, 0, 0]),
                          "full_house": 0
                          }

    def value_component(self):
        pass




if __name__ == "__main__":
    NumberOfIndividuals = 40
    NumberOfGens = 50
    crossOverProbability = 0.6
    mutationProbability = 0.03
    terminateGoal = np.array([1]*NumberOfGens)
    maxGenerations = 1000
    #terminateGoal = np.random.randint(0,2,(NumberOfGens))

    # Produce a Genetic Agent Object
    agent = ga.agentGA(NumberOfIndividuals, NumberOfGens, crossOverProbability, mutationProbability, terminateGoal, maxGenerations)
    ga.agentGA.GAStart
    # Start solve the problem
    starttime = time.time()
    agent.GAStart()
    stoptime = time.time()
    
    
    print(f"Time ended at:, {stoptime - starttime},seconds")
    print(f'The goal to reach was: {terminateGoal}')
    print(agent.population)






