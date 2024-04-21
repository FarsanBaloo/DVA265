import numpy as np

class Bauhaus:
    def __init__(self):
        self.name = "Bauhaus"
        """ Inventory: Door, Outside-Door, Window, Wall-Module, Toilet Seat, Tab, Shower Cabin"""
        self.fully_stocked = np.array([10, 10, 10, 5, 10, 10, 10])
        self.max_stock = np.array([15, 15, 15, 15, 10, 15, 15])
        self.inventory = np.random.randint(3, 10, size=7)
        #self.inventory = np.array([10, 10, 10, 10, 10, 10, 10])
        self.ComponentCost = np.array([2500, 8500, 3450, 75000, 2995, 2350, 8300])
        self.fullComponentCost = np.array([2500, 8500, 3450, 75000, 2995, 2350, 8300])
        self.Sale = False
        self.saleChance = 0.2
        self.money = 0
        self.credit = 0

    def resupply(self):
        money = self.money
        difference = self.fully_stocked.copy() - self.inventory.copy()
        print('Difference:', difference)
        componentsToBuy = np.random.randint(difference - 5, difference + 5, size=len(self.inventory))
        print(f"Randomized Components to Buy {componentsToBuy}")
        componentsToBuy = np.where(componentsToBuy > 0, componentsToBuy, 0)
        print('Adjusted for Negatives', componentsToBuy)
        # if np.any(np.all((componentsToBuy + self.inventory) > 15)):
        #     difference = self.max_stock.copy() - componentsToBuy
        #     print("Too many", difference)
        #     componentsToBuy = np.where((componentsToBuy + self.inventory) > 15,
        #                                componentsToBuy, (componentsToBuy - difference))
        cost = int((np.sum(componentsToBuy * self.ComponentCost)) * 0.8)
        print("Finalized Components to Buy:", componentsToBuy)
        print(f"Cost: {cost}")
        money = money-cost
        self.credit += money
        self.money = 0

    def handleCredit(self):
        self.credit = int(self.credit * 1.05)
        print("New Credit:", self.credit)

    def handleSales(self):
        if np.random.rand(1) < self.saleChance:
            salePrices = np.round(self.ComponentCost.copy() * 0.75).astype(int)
            print(salePrices)
            self.Sale = True
            self.ComponentCost = salePrices.copy()
        else:
            self.ComponentCost = self.fullComponentCost.copy()
            self.Sale = False

    def doSomething(self):
        self.resupply()
        self.handleCredit()
        self.handleSales()



if __name__ == "__main__":
    bauhaus = Bauhaus()
    # for i in range(100):
    bauhaus.doSomething()