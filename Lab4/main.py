import numpy as np
from MaterialAgent import Bauhaus
from BuilderAgent import Builder


class GA:
    def __init__(self, numberOfIndividuals = 4, crossOverProbability = 0.6, mutationProbability = 0.03, terminateGoal = 0, maxGenerations = 100):
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
 
 
    def GeneratePopulation(self):
        
        agents = []
        for i in range(self.numnberOfIndividuals):
            agent = Builder("agent" + str(i))
            agents.append(agent)
        
        self.population = agents


    def CalculateFitness(self, population):
        
        # prototype för att ha något att utgå ifrån för en selection så får vi ändra den till det bätte senare  
        
        sellPriceHouse = 1000000
        
        populationMoney = np.array([agents.money for agents in population])
        populationHouses = np.array([agents.houses for agents in population])
        populationModules = np.array([np.sum(agents.modules) for agents in population])
        # Get the agent with the most modules built
        amountOfmaxModules = np.max(populationModules)
      
        populationMoney += populationHouses * sellPriceHouse
        totalPopulationMoney = np.sum(populationMoney)
        
        normalizedPopulationMoney = np.divide(populationMoney, totalPopulationMoney , where = totalPopulationMoney > 0)
        print(f"Normalized population money: {normalizedPopulationMoney}")
        # Try to do a estamation of performence of the agents of amount of modules he have built against the agent with the most modules
        normalizedPopulationModules = np.divide(populationModules, amountOfmaxModules, where = amountOfmaxModules > 0)
        print(f"Normalized population modules: {normalizedPopulationModules}")
        
        populationFitness = (normalizedPopulationMoney * 0.9 + normalizedPopulationModules * 0.1) * 100
        totalFitnessPopulation = np.sum(populationFitness)
 
        normalizedPopulationFitness = np.divide(populationFitness,totalFitnessPopulation, where = totalFitnessPopulation > 0)
        print(f"Normalized population fitness: {normalizedPopulationFitness}")
        
        # bring in the money and sell the houses
        for i , agent in enumerate(population):
            agent.money = populationMoney[i]
            agent.fitness = normalizedPopulationFitness[i]
            print(f"{agent.name} has {agent.money} after selling {agent.houses} built houses and have now fitness {agent.fitness} % he built {agent.modules} modules")
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
        
    def crossover(self,parent1,parent2):

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
    
    
    GA = GA(numberOfIndividuals, crossOverProbability, mutationProbability, terminateGoal , maxGenerations)
    
    
    GA.GeneratePopulation()
    print(GA.population)
    
    generation = 0
    
    while generation < 1:
        
        for agent in GA.population:
            
            generation += 1
            print(f"Generation: {generation}")
            
            print(f"======={agent.name}'s turn! =========")
            agent.doSomething()
            agent.generateGenome()
            #print(agent.generateGenome())
    
    
        GA.CalculateFitness(GA.population)


    agentBauhaus = Builder("Bauhaus")








