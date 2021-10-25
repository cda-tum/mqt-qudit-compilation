class Vine:
    # TODO DATA STRUCTURE USEFUL FOR SIMPLE RESCHEDULING OF OPERATIONS
    # TODO TO INTEGRATE IN CASE OF DAG SCEDULING STRATEGY
    def __init__(self, dimension):
        self.couplings = [[] for x in range(dimension-1)]
        self.dimension = dimension

    def head_push(self, couple,  item):
        self.couplings[couple].insert(0, item)

    def head_pop(self, couple):
        return self.couplings[couple].pop(0)

    def tail_push(self, couple,  item):
        self.couplings[couple].append(item)

    def tail_pop(self, couple):
        return self.couplings[couple].pop()

    def insert(self, couple, index, item):
        self.couplings[couple].insert(index, item)

    def delete(self, couple, index):
        return self.couplings[couple].pop(index)



