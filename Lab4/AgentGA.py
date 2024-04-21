import numpy as np

class GA:
    def __init__(self, agent, agents, index, numGen):
        self.genes = agent
        self.money = agent[0]
        self.houses = agent[1]

        # 0 = door, 1 = outside door, 2 = window, 3 = wall module, 4 = toilet seat, 5 = tab, 6 = shower cabin
        self.inventory = agent[2:9]
        self.sell_list = agent[14:21]
        self.buy_list = agent[21:28]
        
        # 0 = bed room, 1 = bath room, 2 = living room, 3 = hall, 4 = garret
        self.modules = agent[9:14]
        
        # Decision: 0 = Bauhaus, 1-3 Agents
        self.decision = agent[28]

        self.agent_genes = agents
        self.index = index

        self.numGen = numGen

        self.start_state()

    def start_state(self):
        start_genes = self.genes.copy()
        start_money = self.money.copy()
        start_houses = self.houses.copy()
        start_inventory = self.inventory.copy()
        start_sell_list = self.sell_list.copy()
        start_buy_list = self.buy_list.copy()
        start_modules = self.modules.copy()

    def termination_state(self):
        pass

    def selection(self):
        parents = np.zeros(29, dtype = "int32")
        for i in range(len(self.agent_genes)):
            if i == self.index:
                continue
            parents = np.vstack(parents, self.agent_genes[i])


        pass

    def crossover(self, agent1,agent2):
        
       
        
        r = np.random.randint(4)
        
        offspring1 = (r*agent1+(4-r) * agent2)
        offspring2 = ((4-r) * agent1+r*agent2)
        
         
        return offspring1, offspring2

    def fitness(self):

        

        pass    

    def prints(self):
        print(self.genes)
        print(self.money)
        print(self.houses)
        print(self.inventory)
        print(self.modules)
        print(self.sell_list)
        print(self.buy_list)
        print(self.decision)
    
    def mutation(self):
        pass

    def ga_loop(self):
        generation = 0
        fitness = self.fitness()

        while generation < self.numGen:
            generation += 1
            
            print('='*30)
            print(f'Generation number:{generation}')

            selection = self.selection()



if __name__ == "__main__":
    
    agent1 = np.array([1,1,1,1])
    agent2 = np.array([2,2,2,2])



            
            
            