from configure.ObjectiveFunctionInterface import ObjectiveFunctionInterface


class ConfigurationFinder:
    def __init__(self, budget: int):
        """:param budget: maximum summary cost of components"""
        self.budget = budget


    def find(self):
        """:returns best configuration that can find
        :rtype: tuple"""
        pass
