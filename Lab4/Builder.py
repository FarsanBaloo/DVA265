import numpy as np
import Bauhaus 

class BobtheBuilder():

    def __init__(self, name):
        """
        Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin
        Modules: Floor, Bed room, bath room, living room, hall, garret
        """
        self.name = name
        # 0 = door 
        # 1 = outside door 
        # 2 = window       
        # 3 = wall module
        # 4 = toilet seat
        # 5 = tab
        # 6 = shower cabin
        self.inventory = np.random.randint(40, size=7)
        #self.inventory = np.array([1,0,3,1,0,0,0])
        self.modules = np.zeros(7)
        self.sell_list = np.zeros(7)
        self.buy_list = np.zeros(7)
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
        self.ComponentCost = [2500,8500,3450,75000,2995,2350,8300] 
        self.ModuleCost = np.sum(self.moduleConstrains * self.ComponentCost)

        self.ModuleNames = np.array(["bedroom", "bath room", "living room", "hall", "garret"])  
        # 0 = bed room
        # 1 = bath room
        # 2 = living room
        # 3 = hall
        # 4 = garret
        self.roomCountNeeded = np.array([4,2,1,1,1]) 


    def check_module(self):
        components = self.inventory.copy()
        print("Components:", components)
        modules = self.modules.copy()
        #modules[0] = 4
        #modules[2] = 1
        print("START Modules:", modules, "\n", "-"*20)
        loops = 0
        #any_room = np.any(np.all(self.moduleConstrains <= components, axis=1))
        #print(any_room)
        #print()
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
        self.modules = modules

    def buildHouse(self):
        pass

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



    def check_value(self):
        pass

    def check_fitness(self):
        pass



if __name__ == "__main__":

    # Produce a Genetic Agent Object
    agent = Agent("Bauhaus")
    agent.check_module()
 

    
    
  
 






