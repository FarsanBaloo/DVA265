import numpy as np
import GA as ga
import time







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






