import numpy as np

class agent:
    def __init__(self):
        self.inventory = np.random.randint(0, 10, size=7)

 
class bauhaus:
    def __init__(self):
        self.inventory = np.array([5,4,3,2,1,0,1], dtype="int32")
    

def Buy(agenten, bauhausen):
    # Har inte funktionaliten att försöka köpa mindre om agenten inte har råd 
    maxbuy = np.array([10, 10, 10, 10, 10, 10, 10])
    crossOverProbability = 0.6
    
    agentInventory = agenten.inventory.copy()    
    bauhausInventory = bauhausen.inventory.copy()
    print(f"Agentens buy lista: {agentInventory}, Bauhaus inventory: {bauhausInventory}")
    
    decisions = np.zeros(7, dtype=bool)
    canBuyComponent = np.where(bauhausInventory > 0)[0]
    decisions[canBuyComponent] = np.random.rand(len(canBuyComponent)) < crossOverProbability

 
    byAmount = np.minimum(bauhausInventory, maxbuy)
    print(f"Agenten kan köpa komponenterna: {byAmount} med hänsyn till Bauhaus lager och max begränsning")
    print(f"Agenten köper slumpmässigt: {decisions}")

    if not decisions.any():
        print("Inga köp genomfördes på grund av  slut i bauhhaus lager")
        return agentInventory, bauhausInventory
    
    choosenAmounts = np.random.randint(1, byAmount[decisions] + 1)
    buyAmounts = np.zeros(len(bauhausInventory), dtype=np.int32)
    buyAmounts[decisions] = choosenAmounts

    
    print(f"Agent inventory innan köp: {agentInventory}")
    agentInventory += buyAmounts
    print("Agenten köper antalet:", buyAmounts)
    print(f"Agent inventory efter köp: {agentInventory}")
    
    print(f"Bauhaus inventory innan köp: {bauhausInventory}")
    bauhausInventory -= buyAmounts
    print(f"Bauhaus inventory efter köp: {bauhausInventory}")

    return agentInventory, bauhausInventory


def Trade(agent1, agent2):
    crossOverProbability = 0.6
    
    agent1Inventory = agent1.inventory.copy()    
    agent2Inventory = agent2.inventory.copy()
    print(f"Agent 1 inventory: {agent1Inventory}")
    print(f"Agent 2 inventory: {agent2Inventory}")
    
    
    # generate crossover condition array True/False for each  gen depending on the crossover probability vectorized
    crossoverCondition = (np.random.rand(7) < crossOverProbability)
    print(f'crossover condition: {crossoverCondition}')

    # Produce the Offsprings and select each gen based on parent 1 or 2 depending on crossoverCondition vectorized
    offspring1 = np.where(crossoverCondition, agent2Inventory, agent1Inventory)
    offspring2 = np.where(crossoverCondition, agent1Inventory, agent2Inventory)
    
    print(f"Offspring 1: {offspring1}") 
    print(f"Offspring 2: {offspring2}")
        
    

    return offspring1, offspring2
    
    
if __name__ == "__main__":
    agent1 = agent()
    agent2 = agent()
    Bauhausen = bauhaus() 

        
        

    agentinventory, bauhausinventory = Trade(agent1, agent2)

