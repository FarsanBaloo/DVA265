import numpy as np
from MaterialAgent import Bauhaus
from BuilderAgent import Builder
from AgentGA import GA as AgentGA
import time


class GA:
    def __init__(self, numberOfIndividuals = 4, crossOverProbability = 0.6,
                 mutationProbability = 0.03, terminateGoal = 0, maxGenerations = 100, maxbuy = 10):
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
        self.names = ["Rickard", "Greta", "Fredrik", "Johanna", "Maytham",
                      "Lisa", "Gunnar", "Sandra", "Mikael", "Gudryn"]
        self.moduleConstrains = np.array([
        [1,0,2,1,0,0,0],   # Constrains for the bed room
        [1,0,0,1,1,1,1],   # Constrains for the bathroom
        [1,0,3,1,0,0,0],   # Constrains for the living room
        [0,1,1,1,0,0,0],   # Constrains for the hall
        [1,0,3,1,0,0,0]    # Constrains for the garret
        ])
        self.ComponentCost = np.array([2500,8500,3450,75000,2995,2350,8300])
        self.componentNames = ["Door", "Outside Door", "Window", "Wall Module", "Toilet Seat", "Tab", "Shower Cabin"]
        self.ModuleCost = np.sum(self.moduleConstrains * self.ComponentCost, axis = 1)
        self.maxbuy = maxbuy
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
        # Try to do a estamation of performence of the agents of amount of modules he have built against the agent with the most modules
        normalizedPopulationModules = np.divide(populationMoneyFromModules, totalModuleMoneySum, where = totalModuleMoneySum > 0)
        normalizedPopulationComponents = np.divide(populationMonyFromComponents, populationMonyFromComponentsSum, where = populationMonyFromComponentsSum > 0)
        if debug:
            print(f"Normalized population money: {normalizedPopulationMoney}")
            print(f"Normalized population modules: {normalizedPopulationModules}")
            print(f"Normalized population modules: {normalizedPopulationComponents}")
        
        populationFitness = (
            normalizedPopulationMoney * 1 
          + normalizedPopulationModules * 1.2
          + normalizedPopulationComponents * 1.1)
        totalFitnessPopulation = np.sum(populationFitness)
 
        normalizedPopulationFitness = np.divide(populationFitness,totalFitnessPopulation, where = totalFitnessPopulation > 0)
        if debug:
            print(f"Normalized population fitness: {normalizedPopulationFitness}")
        
        # bring in the money and sell the houses
        for i , agent in enumerate(population):
            agent.money = populationMoney[i]
            agent.fitness = normalizedPopulationFitness[i]
            print(f"{agent.name} has {agent.money} after selling {agent.houses} built houses and have now fitness {agent.fitness*100.:2f} % s/he built {agent.modules} modules")
            agent.houses = 0
        
        self.populationFitness = normalizedPopulationFitness
        
        return self.populationFitness


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
        
    def BauhausShopping(self, agent):
        # behöver man ta hänsyn till vad (r) får varijera max mellan?, typ med hänsyn vad som agententerna har i sin lista!? 
        
        bauhausInventory = Bauhaus.inventory.copy()
        agentInventory = agent.inventory.copy()
        crossoverCondition = (np.random.rand(7) < self.crossOverProbability)
        agentMoney = agent.money
        maxbuy = self.maxbuy
        if debug:
            print("="*20, "\n" + f"Crossover Condition: {crossoverCondition}")
            print(f"{agent.name} has {agentMoney}kr of dispensible money.")
            print(f"{agent.name}'s inventory: {agentInventory}")
            print(f"{Bauhaus.name}'s inventory: {bauhausInventory}")
        
        for index in len(crossoverCondition):
            if crossoverCondition[index]:
                if bauhausInventory[index] >= maxbuy:
                    amount = np.random.randint(1, maxbuy+1)
                elif bauhausInventory[index] == 0:
                    continue
                else:
                    amount = np.random.randint(1, bauhausInventory[index]+1)
                    
                print(f"{agent.name} is trying to buy {amount} {self.componentNames[index]} for {amount*self.ComponentCost[index]}")
                while agentMoney <= amount * self.ComponentCost[index]:
                    if debug:
                        print(f"Removing 1 {self.componentNames[index]} of {amount}")
                    amount -= 1
    
                if amount == 0:
                    print(f"Sorry, you can't afford to buy {self.componentNames[index]}.")
                    continue
                
                agentInventory[index] += amount
                bauhausInventory[index] -= amount
                agentMoney -= amount * self.ComponentCost[index]
                if debug:
                    print(f"Updated {agent.name} Inventory: {agentInventory}")
                    print(f"Updated Bauhaus Inventory: {bauhausInventory}")
                    print(f"Updated Moneybag: {agentMoney}")
        
        agent.inventory = agentInventory
        Bauhaus.inventory = bauhausInventory
        agent.money = agentMoney

            
            #np.where(crossoverCondition1, (r*parent1+(t-r) * parent2))
        
        #crossoverCondition2 = (np.random.rand(self.numnberOfIndividuals) < self.crossOverProbability)
        #offspring2 = np.where(crossoverCondition2, ((t-r) * parent1+r*parent2))
        
        
        #return offspring1, offspring2
    
    def BauhausShoppingHybrid(self, agent):
        
        #agent1_buy_list = agent.inventory.copy()
        bauhausInventory = Bauhaus.inventory.copy()
        
        
        # fiskar ut alla element som är större än 0 dvs vad agent1 kan köpa och vad agent2 kan sälja
        #agent1buy = np.where(agent1_buy_list > 0)[0]
        bauhausSell = np.where(bauhausInventory > 0)[0]
        
        
        # kollar vad max som kan köpas
        buy = max(0, bauhausInventory[bauhausSell])
        #maxbuy = max(agent1_buy_list[agent1buy], agent2_sell_list[agent2sell])
        
        
        # kollar om minbuy är större än 0 och om det är det så köper agenten så mycket som den kan och kanske lite till
        if buy > 0:
            amounOfBuy = np.random.randint(self.maxbuy, buy)
        else:
            return
        
        
        
        
        
        
        
        
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
    debug = True
    
    
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








