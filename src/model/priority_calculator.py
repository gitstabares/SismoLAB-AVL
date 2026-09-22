class PriorityCalculator:

    @staticmethod
    def calculate(magnitude, depth, populated):

        if magnitude >= 6.0:
            return 3

        if magnitude >= 4.5 and depth <= 30 and populated:
            return 3

        if magnitude >= 4.5:
            return 2

        return 1