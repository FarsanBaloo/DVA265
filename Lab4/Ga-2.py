

class GA:
    def __init__(self, numberOfIndividuals = 4, crossOverProbability = 0.6,
                 mutationProbability = 0.03, terminateGoal = 0, maxGenerations = 100):
        self.numnberOfIndividuals = numberOfIndividuals
        self.crossOverProbability = crossOverProbability
        self.mutationProbability = mutationProbability
        self.terminateGoal = terminateGoal
        self.countGeneration = 0
        self.maxGenerations = maxGenerations
        self.newpopulation = np.array([])
        self.populationFitness = np.array([])
        self.IndividualsPropability = np.array([])
        self.cumulativesum = np.array([])