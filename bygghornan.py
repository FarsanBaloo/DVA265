import numpy as np

class builder:
    def __init__(self,name):
        self.name = name
        
        # 0 = door 
        # 1 = outside door 
        # 2 = window       
        # 3 = wall module
        # 4 = toilet seat
        # 5 = tab
        # 6 = shower cabin
        self.components = np.random.randint(10,30, 7)
        self.moduleConstrains = np.array([
            [1,0,2,1,0,0,0],   # Constrains for the bed room
            [1,0,0,1,1,1,1],   # Constrains for the bathroom
            [1,0,3,1,0,0,0],   # Constrains for the living room
            [0,1,1,1,0,0,0],   # Constrains for the hall
            [1,0,3,1,0,0,0]    # Constrains for the garret
            ])   
        # 0 = bed room ()
        # 1 = bath room ()
        # 2 = living room
        # 3 = hall
        # 4 = garret
        self.roomCountNeeded = np.array([4,2,1,1,1])
        # 0 = bed room
        # 1 = bath room
        # 2 = living room 
        # 3 = hall
        # 4 = garret
        # 5 = floor
        self.modules = np.array([0,0,0,0,0,0])
        self.houses = 0
   
    def buildmodules(self,roomindex):
        moduleComponentsNeeded = self.moduleConstrains[roomindex]
        modulecountNeeded = self.roomCountNeeded[roomindex]
        print(f"Module index: {roomindex}, moduleComponentsNeeded: {moduleComponentsNeeded}, modulecountNeeded: {modulecountNeeded}")
        while self.modules[roomindex] < modulecountNeeded:
            if np.all(self.components >= moduleComponentsNeeded):
                self.components -= moduleComponentsNeeded
                self.modules[roomindex] += 1
                print(f"Built module: {roomindex}, ")
            else:
                print(f"Couldnt build module: {roomindex}, ")
                # stop try building the moduls run out of components
                break

    def buildHouse(self):
        # try build the modules
        #for roomindex in range(len(self.roomCountNeeded)):
            #self.buildmodules(roomindex)
        self.buildmodules(0)
       
        # build floor
        if np.all(self.modules >= np.array([4,2,1,1,0,0])):
            self.modules -= np.array([4,2,1,1,0,0])
            self.modules += np.array([0,0,0,0,0,1])
        
        # build house
        if np.all(self.modules >= np.array([0,0,0,0,1,1])):
            self.modules -= np.array([0,0,0,0,1,1])
            self.houses += 1

   

if __name__ == "__main__":
    # Produce a Genetic Agent Object
    agent = builder("Fredrik")
    print(f"The agent name: {agent.name}, Components: {agent.components} ,Built modules: {agent.modules},Built houses: {agent.houses}")
    agent.buildHouse()
    print(f"The agent name: {agent.name}, Components: {agent.components} ,Built modules: {agent.modules},Built houses: {agent.houses}")
  
    
   
