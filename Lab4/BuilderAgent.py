import numpy as np
import AgentGA as GA
import random

class Builder():

    def __init__(self, name, personality=0):
        """
        Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin
        Modules: Floor, Bedroom, bath room, living room, hall, garret
        """
        self.name = name
        # 0 = door 
        # 1 = outside door 
        # 2 = window       
        # 3 = wall module
        # 4 = toilet seat
        # 5 = tab
        # 6 = shower cabin
        self.inventory = np.random.randint(9, size=7, dtype="int32")
        #self.inventory = np.zeros(7, dtype="int32")
        #self.inventory = np.array( [1,0,2,1,0,0,6])
        self.modules = np.zeros(5, dtype="int32")
        #self.modules = np.array([4,2,1,0,1])
        self.sell_list = np.zeros(7, dtype="int32")
        self.buy_list = np.zeros(7, dtype="int32")
        self.money = 750000
        self.houses = 0
        self.fitness = 0
        self.moduleConstrains = np.array([
        [1,0,2,1,0,0,0],   # Constrains for the bed room
        [1,0,0,1,1,1,1],   # Constrains for the bathroom
        [1,0,3,1,0,0,0],   # Constrains for the living room
        [0,1,1,1,0,0,0],   # Constrains for the hall
        [1,0,3,1,0,0,0]    # Constrains for the garret
        ])
        self.ComponentCost = np.array([2500,8500,3450,75000,2995,2350,8300])
        self.ModuleCost = np.sum(self.moduleConstrains * self.ComponentCost)
        self.totalCompNeed = np.array([8, 1, 15, 9, 2, 2, 2])
        self.ModuleNames = np.array(["bedroom", "bath room", "living room", "hall", "garret"])  
        # 0 = bed room
        # 1 = bath room
        # 2 = living room
        # 3 = hall
        # 4 = garret
        self.roomCountNeeded = np.array([4, 2, 1, 0, 1])

        # 0 = bauhaus, 1 = enthusiastic, 2 = unchanged, 
        # 3 = conservative, 4 = My money, my rules
        self.sell_personality = random.randint(1,4)
        self.buy_personality = random.randint(0,4)
        self.fitness = 0

    def check_module(self):
        components = self.inventory.copy()
        print("Components:", components)
        modules = self.modules.copy()
        print("START Modules:", modules, "\n", "-"*20)
        loops = 0

        while np.any(np.all(self.moduleConstrains <= components, axis=1)):
            loops += 1
            print("Iteration:", loops, "\n", "="*20)
            buildable = np.all(self.moduleConstrains <= components, axis=1)
            print("Buildable Elements:", buildable)
            component, module, build = self.buildModule(np.where(buildable == True), components.copy(), modules.copy())
            print("Updated Components:", component, "Built Module:", module)
            print("-"*10)
            print("Unupdated Modules:", modules)
            print("-"*10)

            if build == False:
                print("---WE BREAK!---")
                break

            components = component.copy()
            modules = module.copy()
            print("Updated Modules:", modules)
        self.inventory = components.copy()
        self.modules = modules

    def buildHouse(self):
        modules = self.modules.copy()
        roomCount = self.roomCountNeeded.copy()
        while np.any(np.all(roomCount <= modules)):
            modules = modules - roomCount
            self.houses += 1
            print(f"----{self.name.upper()} BUILT A HOUSE!----")
            self.modules = modules
        return

    def buildModule(self, element, component, modules):
        for e in element[0]:
            if self.roomCountNeeded[e] <= modules[e]:
                print(f"----{self.ModuleNames[e].upper()} HAVE BEEN PASSED!----")
                continue
            if np.all(self.moduleConstrains[e] <= component):
                print("Cost of Module", self.moduleConstrains[e])
                print("Current Components:", component)
                component -= self.moduleConstrains[e]
                print("After Subtraction of Cost:", component)
                modules[e] += 1
                print(f"Built Module: {self.ModuleNames[e].capitalize()}")
                return component, modules, True
        print("NON FOUND")
        return component, modules, False
    
    def testgenerateSellBuyList(self):
        """Generate a sell and buy list, depending on what the Agent has in its inventory"""
        room_need = self.roomCountNeeded - self.modules
        print("Room need:", room_need)
        
        TransponatmoduleConstrains = self.moduleConstrains.transpose()
        total_need = np.dot(TransponatmoduleConstrains, room_need)
        
        print("Total need", total_need)
        print("Inventory", self.inventory)
        
        agent_needs = self.inventory - total_need
        self.sell_list = np.where(agent_needs > 0, agent_needs, 0)
        self.buy_list = np.where(agent_needs < 0, np.abs(agent_needs), 0)
        
        print("We have too many of:", self.sell_list)
        print("We need to buy:", self.buy_list)

    def generateSellBuyList(self):
        """Generate a sell and buy list, depending on what the Agent has in its inventory"""
        room_need = self.roomCountNeeded - self.modules
        print("Room need:", room_need)
        total_need = np.zeros(7)
        for i, a in enumerate(self.moduleConstrains):
            total_need += a * room_need[i]
        print("Total need", total_need)
        print("Inventory", self.inventory)
        agent_needs = self.inventory - total_need
        sell_list = [x if x >= 0 else 0 for x in agent_needs]
        buy_list = [-x if x <= 0 else 0 for x in agent_needs]
        print("We have too many of:", sell_list)
        print("We need to buy:", buy_list)
        self.buy_list = np.array(buy_list, dtype="int32")
        self.sell_list = np.array(sell_list, dtype="int32")

    def doSomething(self):
        self.check_module()
        self.buildHouse()
        #self.generateSellBuyList()
        self.testgenerateSellBuyList()

    def generateGenome(self):
        base = np.array([self.money, self.houses], dtype="int32")
        return np.concatenate((
            base.copy(),
            self.inventory.copy(),
            self.modules.copy(),
            self.sell_list.copy(),
            self.buy_list.copy(),
            self.sell_personality,
            self.buy_personality))

    
  
 

if __name__ == "__main__":
    agent = Builder("Oscar")
    agent.doSomething()
    genome = agent.generateGenome()
    print(genome)




