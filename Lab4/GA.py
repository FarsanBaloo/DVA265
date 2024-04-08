import numpy as np
import time

class agentGA:
    def __init__(self,NumberOfIndividuals = 10, NumberOfGens = 10, crossOverProbability = 0.6, mutationProbability = 0.03, terminateGoal = 0, maxGenerations = 100):
        self.population = np.array([])
        self.NumberOfIndividuals = NumberOfIndividuals
        self.NumberOfGens = NumberOfGens
        self.crossOverProbability = crossOverProbability
        self.mutationProbability = mutationProbability
        self.terminateGoal = terminateGoal
        self.countGeneration = 0
        self.maxGenerations = maxGenerations
        self.newpopulation = np.array([])
        self.Individualfitness = np.array([])
        self.IndividualsPropability = np.array([])
        self.cumulativesum = np.array([])
 
    def GeneratePopulation(self):
        self.population = np.random.randint(0,2, (self.NumberOfIndividuals, self.NumberOfGens))
   
    def CalculateFitness(self,individuals):
        fitness = (np.sum(individuals == self.terminateGoal, axis=1) / self.NumberOfGens) * 100
        return fitness
           
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
        
    def crossoverUniform(self,parent1,parent2):
        # generate crossover condition array True/False for each gen depending on the crossover probability vectorized
        crossoverCondition = (np.random.rand(self.NumberOfGens) < self.crossOverProbability)
        #print(f'The Uniform crossover condition based of probability: {crossoverCondition}')

        # Produce the Offsprings and select each gen based on parent 1 or 2 depending on crossoverCondition vectorized
        offspring1 = np.where(crossoverCondition, parent2, parent1)
        offspring2 = np.where(crossoverCondition, parent1, parent2)
        
        return offspring1, offspring2
    
    def crossoverSinglePoint(self,parent1,parent2):
        offspring1 = parent1.copy()
        offspring2 = parent2.copy()
    
        if np.random.rand() < self.crossOverProbability:
            # generate the randome crossover indicie based on number of gens and prevent crossover happend at start or end  
            crossoverIndicie = np.random.randint(1,self.NumberOfGens-1)
            
            #print(f'The crossover happens now becuase of probability at indicies: {crossoverIndicie}')
            # store the crossover gens from parent 1 before it gets swappped with parent 2
            tempCrossoverGenStateParent1 = parent1[crossoverIndicie:].copy()
            # Start doing the gen crossover between the two parent to create the two offsprings
            offspring1[crossoverIndicie:] = parent2[crossoverIndicie:].copy()
            offspring2[crossoverIndicie:] = tempCrossoverGenStateParent1
        
        return offspring1, offspring2
    
    def mutation(self,offspring1,offspring2):
        # Offspring1 generate mutation condition array True/False for each gen depending on the mutation probability vectrorized
        mutationCondition1 = (np.random.rand(self.NumberOfGens) < self.mutationProbability)
        #print(f'The mutation condition for offspring1 based of probability: {mutationCondition1}') 
        offspring1 = np.where(mutationCondition1, 1 - offspring1, offspring1)
        
        # Offspring2 generate mutation condition array True/False for each gen depending on the mutation probability vectrorized
        mutationCondition2 = (np.random.rand(self.NumberOfGens) < self.mutationProbability)
        #print(f'The mutation condition for offspring2 based of probability: {mutationCondition2}')
        offspring2 = np.where(mutationCondition2, 1 - offspring2, offspring2)
        
        return offspring1, offspring2

    def evaluateRanked(self,parent1,parent2,offspring1,offspring2):
        # stack the family members together to easier handle them during calculation
        individuals = np.vstack((parent1,parent2,offspring1,offspring2))
        fitness = self.CalculateFitness(individuals)
        elementsortedbyfitness = np.argsort(-fitness)
        
        return individuals[elementsortedbyfitness[0]],individuals[elementsortedbyfitness[1]]
      
    def updatePopulation(self):
        self.population = self.newpopulation.copy()
        self.newpopulation = np.empty((0, self.population.shape[1]))

    def terminate(self):
        if np.any(np.all(self.population == self.terminateGoal, axis = 1)):
            self.Individualfitness = self.CalculateFitness(self.population)
            print(f'The Agent reached its goal!, with the amount of generations: {self.countGeneration}')
            return True
        
        elif self.countGeneration == self.maxGenerations:
            print(f'The Agent didnt reach its goal! the maxgeneration stopped the agent with the amount of generations: {self.countGeneration}')
            return True
        
        return False
 
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
    NumberOfIndividuals = 40
    NumberOfGens = 50
    crossOverProbability = 0.6
    mutationProbability = 0.03
    terminateGoal = np.array([1]*NumberOfGens)
    maxGenerations = 1000
    #terminateGoal = np.random.randint(0,2,(NumberOfGens))

    # Produce a Genetic Agent Object
    agent = agentGA(NumberOfIndividuals, NumberOfGens, crossOverProbability, mutationProbability, terminateGoal, maxGenerations)

    # Start solve the problem
    starttime = time.time()
    agent.GAStart()
    stoptime = time.time()
    
    
    print(f"Time ended at:, {stoptime - starttime},seconds")
    print(f'The goal to reach was: {terminateGoal}')
    print(agent.population)
   
