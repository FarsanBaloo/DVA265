import numpy as np

class Bauhaus:
    def __init__(self):
        self.name = "Bauhaus"
        """ Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin"""
        # self.totalCompNeed = np.array([8, 1, 15, 9, 2, 2, 2])
        self.fully_stocked = np.array([12, 3, 25, 9, 5, 5, 5])
        self.max_stock = np.array([18, 8, 30, 15, 10, 10, 10])
        #self.inventory = np.random.randint(3, 10, size=7)
        self.inventory = np.zeros(7)
        #self.inventory = np.array([10, 10, 10, 10, 10, 10, 10])
        self.ComponentCost = np.array([2500, 8500, 3450, 75000, 2995, 2350, 8300])
        self.fullComponentCost = np.array([2500, 8500, 3450, 75000, 2995, 2350, 8300])
        self.REA = False
        self.REAChance = 0.2
        self.money = 650000
        self.BankBalance = 0
        self.interestRate = 0.05
        self.inkopspris = 0.5

    def resupply(self):
        money = self.money
        difference = self.fully_stocked.copy() - self.inventory.copy()
        #print('Difference:', difference)
        componentsToBuy = np.random.randint(difference - 5, difference + 5, size=len(self.inventory))
        #print(f"Randomized Components to Buy {componentsToBuy}")
        componentsToBuy = np.where(componentsToBuy > 0, componentsToBuy, 0)
        #print('Adjusted for Negatives', componentsToBuy)
       
        cost = int((np.sum(componentsToBuy * self.ComponentCost)) * self.inkopspris)
        #print("Finalized Components to Buy:", componentsToBuy)
        #print(f"Cost: {cost}")
        money = money - cost

        self.inventory += componentsToBuy
        self.BankBalance += money
        self.money = 0

    def handleBank(self):
        self.BankBalance += int(self.BankBalance * self.interestRate)
        #print("New Bank Balance:", self.BankBalance)

    def handleREA(self):
        if np.random.rand(1) < self.REAChance:
            salePrices = np.round(self.ComponentCost.copy() * 0.75).astype(int)
            print(salePrices)
            self.REA = True
            self.ComponentCost = salePrices.copy()
        else:
            self.ComponentCost = self.fullComponentCost.copy()
            self.Sale = False


    def doSomething(self):
        self.resupply()
        self.handleBank()
        self.handleREA()



if __name__ == "__main__":
    bauhaus = Bauhaus()
    # for i in range(100):
    bauhaus.doSomething()