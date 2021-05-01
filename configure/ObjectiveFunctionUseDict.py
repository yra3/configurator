from configure.ObjectiveFunctionInterface import ObjectiveFunctionInterface


class ObjectiveFunctionUseDict():
    def calculate_coefficients(self):
        pass

    def __init__(self, coefficients: dict = None, coefficients_calculator=lambda x: [0, 0, 0]):
        """Parameter coefficients must be
        dict{component_name: importance_coefficient}"""
        if coefficients is None:
            self.calculate_coefficients()

    def calculate(self, parameters):
        """Get dict{component_name: value} of configuration
        parameters, :returns integer value"""
        answer = 0
        for name, value in parameters.items():
            answer += self.coefficients[name] * value
        return answer

    def get_lower_estimate(self, configure):
        cpu, gpu, mother, ram1, cooler1, hard1, ssd1, powersupply1 = list(find_configure)
        configurate = {
            'CPU': cpu.price,
            'GPU': gpu.price,
            'motherboard': mother.price,
            'RAM': ram1.the_volume_of_one_memory_module * ram1.number_of_modules_included,
            'cooler': cooler1.power_dissipation,
            'hard_35': hard1.hdd_capacity,
            'ssd': ssd1.drive_volume,
            'powersupply': powersupply1.power_nominal,
        }
        return self.objective_function.calculate(configurate)