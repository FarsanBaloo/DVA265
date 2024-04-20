import numpy as np
from MaterialAgent import Bauhaus
from BuilderAgent import Builder
from AgentGA import GA as AgentGA
import time


class GA:
    def __init__(self, numberOfIndividuals = 4, crossOverProbability = 0.6,
                 mutationProbability = 0.03, terminateGoal = 0, maxGenerations = 100):
        self.numnberOfIndividuals = numberOfIndividuals
        self.crossOverProbability = crossOverProbability
        self.mutationProbability = mutationProbability
        self.terminateGoal = terminateGoal
        self.countGeneration = 0
        self.maxGenerations = maxGenerations
        self.newpopulation = np.array([])
        self.populationFitness = np.array([])
        self.IndividualsPropability = np.array([])
        self.cumulativesum = np.array([])
        self.names = ["Rickard", "Greta", "Fredrik", "Johanna"]
        self.moduleConstrains = np.array([
        [1,0,2,1,0,0,0],   # Constrains for the bed room
        [1,0,0,1,1,1,1],   # Constrains for the bathroom
        [1,0,3,1,0,0,0],   # Constrains for the living room
        [0,1,1,1,0,0,0],   # Constrains for the hall
        [1,0,3,1,0,0,0]    # Constrains for the garret
        ])
        self.ComponentCost = [2500,8500,3450,75000,2995,2350,8300] 
        self.ModuleCost = np.sum(self.moduleConstrains * self.ComponentCost, axis = 1)
        #self.ModuleCost = np.sum(self.moduleConstrains.transpose().prod(self.ComponentCost))
        #self.ModuleCost = self.moduleConstrains.transpose()
        


    def GeneratePopulation(self):
        
        agents = []
        for i in range(self.numnberOfIndividuals):
            agent = Builder("Agent " + self.names[i])
            agents.append(agent)
        
        self.population = agents

    def CalculateFitness(self, population):
        
        # prototype för att ha något att utgå ifrån för en selection så får vi ändra den till det bätte senare  
        
        sellPriceHouse = 1000000
        
        # Calculate the money each individual has in wallet and in assets.
        populationMoney = np.array([agents.money for agents in population])                             # Wallet Money
        populationHouses = np.array([agents.houses for agents in population])                           # Built Houses?
        populationComponents = np.array([agents.inventory for agents in population])                    # Inventory for Each Agent
        populationModules = np.array([agents.modules for agents in population])                         # Find Modules
        populationMoneyFromModules = np.sum(populationModules * self.ModuleCost, axis = 1)              # 
        populationMonyFromComponents = np.sum(populationComponents * self.ComponentCost, axis = 1)


        populationMoney += populationHouses * sellPriceHouse
        totalPopulationMoney = populationMoney + populationMonyFromComponents + populationMoneyFromModules
        totalpopulationMoneySum = np.sum(totalPopulationMoney)
        totalModuleMoneySum = np.sum(populationMonyFromComponents)
        populationMonyFromComponentsSum = np.sum(populationMonyFromComponents)
        #print(f"Total population money: {totalpopulationMoneySum}")
        
        normalizedPopulationMoney = np.divide(totalPopulationMoney, totalpopulationMoneySum , where = totalpopulationMoneySum > 0)
        print(f"Normalized population money: {normalizedPopulationMoney}")
        # Try to do a estamation of performence of the agents of amount of modules he have built against the agent with the most modules
        normalizedPopulationModules = np.divide(populationMoneyFromModules, totalModuleMoneySum, where = totalModuleMoneySum > 0)
        print(f"Normalized population modules: {normalizedPopulationModules}")
        normalizedPopulationComponents = np.divide(populationMonyFromComponents, populationMonyFromComponentsSum, where = populationMonyFromComponentsSum > 0)
        print(f"Normalized population modules: {normalizedPopulationComponents}")
        
        populationFitness = (
            normalizedPopulationMoney * 1 
          + normalizedPopulationModules * 1.2
          + normalizedPopulationComponents * 1.1)
        totalFitnessPopulation = np.sum(populationFitness)
 
        normalizedPopulationFitness = np.divide(populationFitness,totalFitnessPopulation, where = totalFitnessPopulation > 0)
        print(f"Normalized population fitness: {normalizedPopulationFitness}")
        
        # bring in the money and sell the houses
        for i , agent in enumerate(population):
            agent.money = populationMoney[i]
            agent.fitness = normalizedPopulationFitness[i]
            print(f"{agent.name} has {agent.money} after selling {agent.houses} built houses and have now fitness {agent.fitness*100.:2f} % s/he built {agent.modules} modules")
            agent.houses = 0
        
        self.populationFitness = normalizedPopulationFitness
        
        return self.populationFitness

    def Crossover(self):
        pass
           
    def calculatePropability(self):
        # Calculate each individual propability in a normalized fashion
        self.IndividualsPropability = self.Individualfitness/np.sum(self.Individualfitness)
        # Calculate the cumulative sum of the propability
        self.cumulativesum = np.cumsum(self.IndividualsPropability)

    def selectionRoulettWheel(self):
        # Spinn the roulette wheel "two" times to get two random floats each between 0 and 1
        self.ResultRoulettSpin = np.random.rand(2)
        
        # Calculate Probability for all the inviduals
        self.calculatePropability()
        #print(f'The Individual propability:{self.IndividualsPropability}')
        #print(f'The individal Cumulative end boundary of roulett wheel :{self.cumulativesum}')
        
        # Get the indicies for the parents by searching where the roulett wheel results is less then or equal in the cumulativesum array
        self.selectedParentsElement = np.searchsorted(self.cumulativesum, self.ResultRoulettSpin)
        self.selectedParents = self.population[self.selectedParentsElement]
        
        return self.selectedParents[0], self.selectedParents[1]
        
    def crossover(self, parent1, parent2):
        pass
        
    def mutation(self,agent1,agent2):
        pass

    def evaluateRanked(self,agent1,agent2,offspring1,offspring2):
        pass    
      
    def updatePopulation(self):
        pass

    def terminate(self):
        pass
 
    def GAStart(self):
        
            # Generate Population
            self.GeneratePopulation()
            #print("The Inviduals in the population are:")
            print(self.population)
            self.Individualfitness = self.CalculateFitness(self.population)
            
            self.newpopulation = np.empty((0, self.population.shape[1]))
              
            while not self.terminate():
                self.countGeneration += 1
                print('=============================================')
                print(f'Generation number:{self.countGeneration}')
                            
                while len(self.newpopulation) < self.NumberOfIndividuals:
                
                    # Start Selection of parents using roulett wheel method
                    #print('-----------------------------------')
                    parent1,parent2 = self.selectionRoulettWheel()
                    #print(f'Result of roulett wheel spin during selection :{self.ResultRoulettSpin}')
                    #print(f'The selected individual element numbers from the spin of roulett wheel:\n{self.selectedParentsElement}')
                    #print(f'Parent1: {parent1}')
                    #print(f'Parent2: {parent2}')
                    
                    # Start Crossover to produce the offspring from the parents
                    offspring1,offspring2 = self.crossoverUniform(parent1, parent2)
                    #print(f'Offspring1 after crossover: {offspring1}')
                    #print(f'Offspring2 after crossover: {offspring2}')
                    
                    # Start mutate the offsprings
                    offspring1, offspring2 = self.mutation(offspring1, offspring2)
                    #print(f'Offspring1 after mutation: {offspring1}')
                    #print(f'Offspring2 after mutation: {offspring2}')
 
                    individual1,individual2 = self.evaluateRanked(parent1,parent2,offspring1,offspring2)
                    #print(f'The best ranked individual in the family is: {individual1}')
                    #print(f'The second best ranked individual in the family is: {individual2}')
                    
                    self.newpopulation = np.vstack((self.newpopulation,individual1))
                    self.newpopulation = np.vstack((self.newpopulation,individual2))
                    #print('-----------------------------------')
                self.Individualfitness = self.CalculateFitness(self.newpopulation)
                #print(f'The Individuals fitness in the population:{self.Individualfitness}')
                print(f'The Best fitness of a individual in the population: {np.max(self.Individualfitness)} %')
                self.updatePopulation()       
                 





if __name__ == "__main__":
    numberOfIndividuals = 4
    crossOverProbability = 0.6
    mutationProbability = 0.03
    terminateGoal = 0
    maxGenerations = 1000
    strategyGenerations = 3
    
    
    GA = GA(numberOfIndividuals, crossOverProbability, mutationProbability, terminateGoal , maxGenerations)
    
    
    GA.GeneratePopulation()
    print(GA.population)

    generation = 0

    generatedGenomes = np.zeros(29, dtype = "int32")
    for agent in GA.population:
        agent.doSomething()
    #    generatedGenomes = np.vstack([generatedGenomes,agent.generateGenome()])

    #np.delete(generatedGenomes, 0,0)
    #print(generatedGenomes)
    #time.sleep(20)
    #while generation < 1:
    #    
    #    for index, agent in enumerate(GA.population):
    #        generation += 1
    #        print(f"Generation: {generation}")
    #        
    #        print(f"======={agent.name}'s turn! =========")
    #        iteration = AgentGA(generatedGenomes[index+1], generatedGenomes[1:], index, strategyGenerations)
    #        iteration.prints()
    #        action = iteration.ga_loop
            

            #print(agent.generateGenome())
    
    
    GA.CalculateFitness(GA.population)


    agentBauhaus = Builder("Bauhaus")








