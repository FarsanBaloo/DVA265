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
        self.population = []
        self.generna = {}
        self.newpopulation = []
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
        self.Bauhaus = Bauhaus
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
        print("="*20, "\n" + "SELECTION ROULETTE WHEEEL OF FORTUNE!")
        self.ResultRoulettSpin = np.random.rand(1)
        print(f"Roulette Result: {self.ResultRoulettSpin}")
        genes = self.generna
        self.calculatePropability()
        print(f"Probability Calculation: {self.cumulativesum}")
        self.selectedParentsElement = np.searchsorted(self.cumulativesum, self.ResultRoulettSpin)
        print(f"Selected Element: {self.selectedParentsElement}")
        print(f"Individual Fitness BEFORE: {self.Individualfitness}")
        self.Individualfitness[self.selectedParentsElement] = 0
        print(f"Individual Fitness AFTER: {self.Individualfitness}")
        self.selectedParent1 = self.population[self.selectedParentsElement]
        print(f"Selected Parent: {self.selectedParent1}, with name {self.selectedParent1.name}")

        choice = self.selectedParent1.wantToTrade(genes)
        print(f"Their choice is: {choice}")
        self.calculatePropability()

        checks = 0
        """ VI FORTSÄTTER HÄR!!!! <<<<<<<<<<<<<<<<< """
        while choice:
            checks += 1
            """SPIN AGAIN!!!!"""
            self.ResultRoulettSpin = np.random.rand(1)
            print(f"Roulette Result: {self.ResultRoulettSpin}")
            self.selectedParentsElement = np.searchsorted(self.cumulativesum, self.ResultRoulettSpin)
            self.selectedParent2 = self.population[self.selectedParentsElement]
            if self.selectedParent2 == self.selectedParent1:
                continue
            choice2 = self.selectedParent2.wantToTrade(genes)
            if choice2:
                self.Individualfitness[self.selectedParentsElement] = 0
                return self.selectedParent1, self.selectedParent2
            elif checks == len(self.population):
                break
            else:
                continue
        self.selectedParent2 = self.Bauhaus

        """selected_agents buy/sell lista <-> köp/sälj listor, för att se vad som kan bytas  
        finns det ingenting intressant, så vill jag gå till Bauhaus.
        Men hittar vi att andra agenter har det vi vill ha, så går vi till dem istället. """


        
        # Calculate Probability for all the inviduals
        
        #print(f'The Individual propability:{self.IndividualsPropability}')
        #print(f'The individal Cumulative end boundary of roulett wheel :{self.cumulativesum}')
        
        # Get the indicies for the parents by searching where the roulett wheel results is less then or equal in the cumulativesum array
        
        
        return self.selectedParent1, self.selectedParent2
        
    def BauhausShopping(self, agent):
        # behöver man ta hänsyn till vad (r) får varijera max mellan?, typ med hänsyn vad som agententerna har i sin lista!? 
        
        bauhausInventory = self.Bauhaus.inventory.copy()
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
        
        agentBuyList= agentInventory
        bauhausInventory = bauhausInventory
        agent.money = agentMoney

        
        return agent

    def Trade(self,agent1, agent2):
        
        print(f"Agent 1 inventory: {agent1.inventory}")
        print(f"Agent 2 inventory: {agent2.inventory}")
        
        # generate crossover condition array True/False for each  gen depending on the crossover probability vectorized
        crossoverCondition = (np.random.rand(7) < self.crossOverProbability)
        print(f'crossover condition: {crossoverCondition}')

        # Produce the Offsprings and select each gen based on parent 1 or 2 depending on crossoverCondition vectorized
        offspring1 = np.where(crossoverCondition, agent2.inventory, agent1.inventory)
        offspring2 = np.where(crossoverCondition, agent1.inventory, agent2.inventory)
        
        print(f"Offspring 1: {offspring1}") 
        print(f"Offspring 2: {offspring2}")
            
        

        return offspring1, offspring2
        
    def mutation(self,offspring1,offspring2):
        # Offspring1 generate mutation condition array True/False for each gen depending on the mutation probability vectrorized
        mutationCondition1 = (np.random.rand(7) < self.mutationProbability)
        #print(f'The mutation condition for offspring1 based of probability: {mutationCondition1}') 
        offspring1 = np.where(mutationCondition1, 1 - offspring1.inventory, offspring1.inventory)
        
        # Offspring2 generate mutation condition array True/False for each gen depending on the mutation probability vectrorized
        mutationCondition2 = (np.random.rand(7) < self.mutationProbability)
        #print(f'The mutation condition for offspring2 based of probability: {mutationCondition2}')
        offspring2 = np.where(mutationCondition2, 1 - offspring2.inventory, offspring2.inventory)
        
        return offspring1, offspring2
          
    def evaluateRanked(self,agent1,agent2,offspring1,offspring2):
        individuals = [agent1,agent2,offspring1,offspring2]
        individualsFitness = self.CalculateFitness(individuals)
        elementsortedbyfitness = np.argsort(-individualsFitness)
        
        return individuals[elementsortedbyfitness[0]],individuals[elementsortedbyfitness[1]]
      
    def updatePopulation(self):
            self.population = self.newpopulation.copy()
            self.newpopulation = []

    def terminate(self):
        pass
 
    def GAStart(self):
        
            # Generate Population
            self.GeneratePopulation()
            self.Bauhaus = Bauhaus()
            self.Bauhaus.doSomething
            #print("The Inviduals in the population are:")
            print(self.population)
            for agent in self.population:
                    agent.doSomething()
                    self.generna[agent.name] = agent.generateGenome()
            self.Individualfitness = self.CalculateFitness(self.population)
            #self.newpopulation = np.empty((0, self.population.shape[1]))


            while not self.terminate():
                self.countGeneration += 1
                print('=============================================')
                print(f'Generation number:{self.countGeneration}')
                self.Bauhaus.doSomething
                for agent in self.population:
                    agent.doSomething()
                    self.generna[agent.name] = agent.generateGenome() 
                self.chosenAgents = 0           
                while len(self.population) < self.ChosenAgents:
                
                    # Start Selection of parents using roulett wheel method
                    #print('-----------------------------------')
                    parent1,parent2 = self.selectionRoulettWheel()
                    #print(f'Result of roulett wheel spin during selection :{self.ResultRoulettSpin}')
                    #print(f'The selected individual element numbers from the spin of roulett wheel:\n{self.selectedParentsElement}')
                    #print(f'Parent1: {parent1}')
                    #print(f'Parent2: {parent2}')
                    
                    if isinstance(parent1, Bauhaus) or isinstance(parent2, Bauhaus):
                        
                        if isinstance(parent1, Builder):
                            self.BauhausShopping(parent1)
                        
                        elif isinstance(parent2, Builder):
                            self.BauhausShopping(parent2)
                        
                    else:
                        # Start to "Trade" / Crossover to produce the offspring from the parents
                        offspring1,offspring2 = self.Trade(parent1, parent2)
                        #print(f'Offspring1 after crossover: {offspring1}')
                        #print(f'Offspring2 after crossover: {offspring2}')
                    
                        # Start mutate the offsprings
                        offspring1, offspring2 = self.mutation(offspring1, offspring2)
                        #print(f'Offspring1 after mutation: {offspring1}')
                        #print(f'Offspring2 after mutation: {offspring2}')
    
                        individual1,individual2 = self.evaluateRanked(parent1,parent2,offspring1,offspring2)
                        #print(f'The best ranked individual in the family is: {individual1}')
                        #print(f'The second best ranked individual in the family is: {individual2}')
                    
                        self.newpopulation.extend(individual1,individual2)
                  
                    #print('-----------------------------------')
                self.Individualfitness = self.CalculateFitness(self.newpopulation)
                print(f'The Best fitness of a individual in the population: {np.max(self.populationFitness)} %')
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
    
    
    #GA.GeneratePopulation()
    #print(GA.population)

    GA.GAStart()

    #generation = 0

    #generatedGenomes = np.zeros(29, dtype = "int32")
    #for agent in GA.population:
    #    agent.doSomething()
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
    
    
    #GA.CalculateFitness(GA.population)


    #agentBauhaus = Builder("Bauhaus")








