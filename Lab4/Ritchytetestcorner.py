import numpy as np

class agent:
    def __init__(self):
        self.BuyList = np.array([3,2,1])

 
class bauhaus:
    def __init__(self):
        self.inventory = np.array([2,1,0], dtype="int32")
    

def BauhausShoppingHybrid(agenten, bauhausen):
    maxbuy = 10
    crossOverProbability = 0.99
    
    agentInventory = agenten.BuyList.copy()
    print("Agentens buy lista:", agentInventory)
    
    bauhausInventory = bauhausen.inventory.copy()
    print("Bauhaus inventory:", bauhausInventory)
  
    
     
    # kontrollera vad agenten vill ha och vad som finns på bauhaus hyllan     
    canBuyElement = np.where((agentInventory> 0) & (bauhausInventory > 0))[0]
    print("Agenten vill köpa:", canBuyElement)
    
    # finns det något att köpa? om inte avsluta
    if not canBuyElement.size:
        print("tomt på hyllan hos bauhas")
        return agentInventory, bauhausInventory
       

    # uppskatta max antal som kan handlas baserat på bauhaus lager
    canByAmount = np.min(agentInventory[canBuyElement], bauhausInventory[canBuyElement])
    print("Agenten kan köpa max antal antal baserat på bauhasus lager:", canByAmount)
    
    # begräns yterligare antal baserat på maxbuy
    canByAmount = np.min(canByAmount, maxbuy)
    print("Agenten kan köpa max antal antal baserat på begränsning av maxbuy:", canByAmount)


    # slumpa vilken vara att köpa ifrån köplistan baserat på Proben
    toBuyElement = np.random.rand(canBuyElement.size) < crossOverProbability
    print("Agenten vill köpa element:", toBuyElement)
    print("Agenten vill köpa element:", toBuyElement)
    buyElement = canBuyElement[toBuyElement]
    print("Agenten vill köpa element:", buyElement)
    
    # slumpa antal att köpa inom intervallet 1 till maxbuy
    buy_amounts = np.random.randint(1, canByAmount[toBuyElement] + 1)
    print("Agenten köper antal:", buyElement)

    # Genomför köp
    print("Agent inventory innan köp:", agentInventory)
    agentInventory[buyElement] += buy_amounts
    print("Agent inventory efter köp:", agentInventory)
    
    print("Bauhaus inventory innan köp:", bauhausInventory)
    bauhausInventory[buyElement] -= buy_amounts
    print("Bauhaus inventory efter köp:", bauhausInventory)

    return agentInventory, bauhausInventory
    
    
if __name__ == "__main__":
    agenten = agent()
    Bauhausen = bauhaus() 

    agentinventory, bauhausinventory = BauhausShoppingHybrid(agenten, Bauhausen)

    print("Agent new inventory:", agentinventory)
    print("Bauhaus new inventory:", bauhausinventory)