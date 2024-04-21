import numpy as np

class Bauhaus:
    def __init__(self):
        self.name = "Bauhaus"
        """ Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin"""
        self.fully_stocked = np.array([10, 10, 10, 10, 6, 10, 10])
        self.max_stock = np.array([15, 15, 15, 15, 15, 15, 15])
        self.inventory = np.random.randint(11, size=7)
        #self.inventory = np.array([10, 10, 10, 10, 10, 10, 10])
        self.ComponentCost = np.array([2500,8500,3450,75000,2995,2350,8300])
        self.money = 8000000
        self.credit = 0

    def resupply(self):
        money = self.money
        print(money)
        full_stock = self.fully_stocked.copy()
        difference = self.fully_stocked.copy() - self.inventory.copy()
        print(difference)
        componentsToBuy = np.random.randint(difference-np.random.randint(0,6), 
                                            difference+np.random.randint(0,6), size=len(self.inventory))
        componentsToBuy = np.where(componentsToBuy < 0, 0)
        print(componentsToBuy)

        

    def doSomething(self):
        
        
        self.resupply()


    self.buy_list = np.where(agent_needs < 0, np.abs(agent_needs), 0)





if __name__ == "__main__":
    bauhaus = Bauhaus()
    bauhaus.resupply()