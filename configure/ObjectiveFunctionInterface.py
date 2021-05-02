

class ObjectiveFunctionInterface:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def calculate(self, parameters):
        ''':param parameters:  list or dict of parameters
        :returns: value of objective function
        :rtype: int'''
        pass