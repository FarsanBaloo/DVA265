import numpy as np
from MaterialAgent import Bauhaus
from BuilderAgent import Builder



if __name__ == "__main__":
    crossOverProbability = 0.6
    mutationProbability = 0.03
    maxGenerations = 1000


    agentBob = Builder("Bauhaus")
    agentBob.check_module()
    
    agentBauhaus = Builder("Bauhaus")








