
class Component:
    # def __init__(self):
    #     self.price = 0
    #     self.name = None
    #     self.maximized_component = None

    def __init__(self, model_component, maximized_component):
        if maximized_component is None:
            raise AttributeError('parm maximized component can\'t be None')
        self.id = model_component.id
        self.price = model_component.price
        self.name = model_component.name
        self.maximized_component = maximized_component


class Configuration:
    def __init__(self, count_components=8):
        self.components = {}
        self.count_components = count_components

    def __int__(self, upper_estimates: dict):  #, priorities: dict):
        """:param upper_estimates: dict with keys - types of components, value - max available maximized value
        :param priorities:  dict with keys - types of components, value - coefficient of influence on the objective function
        """
        self._constructor_parameters_checking(upper_estimates, priorities)
        self.upper_estimates = upper_estimates
        self.priorities = priorities
        self.components = {component_type: None for component_type in upper_estimates.keys()}

    def drop_component(self, component_type: str):
        self.components[component_type] = None

    def set_component(self, component: Component, component_type: str):
        self.components[component_type] = component

    def get_upper_estimate(self):
        product = 1
        for component_type, component in self.components:
            if component is None:
                product *= self.upper_estimates[component_type] ^ (self.priorities[component_type])
            else:
                product *= component.maximized_component ^ (self.priorities[component_type])
        return product

    def get_objective_function(self):
        product = 1
        for component_type, component in self.components.items():
            if component is None:
                raise Exception('Can\'t calculate objective function. Configuration not completed', component_type)
        for component_type, component in self.components:
                product *= component.maximized_component ^ (self.priorities[component_type])
        return product

    def is_completed(self):
        for component_type, component in self.components.items():
            if component is None:
                return False
        return True

    def get_component(self, component_type: str):
        return self.components[component_type]

    @staticmethod
    def _constructor_parameters_checking(upper_estimates: dict, priorities: dict):
        if len(upper_estimates) != len(priorities):
            raise AttributeError('Can\'t create configuration count upper estimates does\'t match with count priorities'
                                 , len(upper_estimates), len(priorities))
        for component_type in upper_estimates.keys():
            if component_type not in priorities.keys():
                raise AttributeError('No such upper estimate type in priorities types', component_type)
        for component_type in priorities.keys():
            if component_type not in upper_estimates.keys():
                raise AttributeError('No such priority type in upper estimate types', component_type)
        for component_type, priority in priorities.items():
            if priority is None:
                raise AttributeError('Priorities can\'t contain None values', component_type)
        for component_type, upper_estimate in upper_estimates.items():
            if upper_estimate is None:
                raise AttributeError('Upper estimates can\'t contain None values', component_type)


class Cpu(Component):
    def __init__(self, cpu, priority):
        super().__init__(cpu, cpu.price ^ priority)
        self.socket = cpu.socket
        self.maximum_frequency_of_ram = cpu.maximum_frequency_of_ram
        self.minimum_frequency_of_ram = cpu.minimum_frequency_of_ram
        self.heat_dissipation_tdp = cpu.heat_dissipation_tdp
        self.bench = cpu.benchmark_mark


class Gpu(Component):
    def __init__(self, gpu,  priority):
        super().__init__(gpu, gpu.price ^ priority)
        self.maximum_power_consumption = gpu.maximum_power_consumption
        self.bench = gpu.benchmark_mark


class Motherboard(Component):
    def __init__(self, motherboard, priority=1):
        super().__init__(motherboard, 1)  # motherboard.price^(-1)
        self.socket = motherboard.socket
        self.supported_memory_form_factor = motherboard.supported_memory_form_factor
        self.supported_memory_type = motherboard.supported_memory_type
        self.maximum_memory_frequency = motherboard.maximum_memory_frequency
        self.minimum_memory_frequency = motherboard.minimum_memory_frequency
        self.maximum_memory = motherboard.maximum_memory


class Ram(Component):
    def __init__(self, ram, priority=1):
        super().__init__(ram, (ram.the_volume_of_one_memory_module*ram.number_of_modules_included) ^ priority)
        self.memory_type = ram.memory_type
        self.memory_form_factor = ram.memory_form_factor
        self.number_of_modules_included = ram.number_of_modules_included
        self.the_volume_of_one_memory_module = ram.the_volume_of_one_memory_module
        self.clock_frequency = ram.clock_frequency


class Cooler(Component):
    def __init__(self, cooler, priority=1):
        super().__init__(cooler, 1)  # cooler.price^(-1)
        self.socket = cooler.socket
        self.power_dissipation = cooler.power_dissipation


class PowerSupply(Component):
    def __init__(self, powerSupply, priority=1):
        super().__init__(powerSupply, 1)  # powerSupply.price^(-1)
        self.power_nominal = powerSupply.power_nominal


class Hard35(Component):
    def __init__(self, hard35, priority=1):
        super().__init__(hard35, hard35.hdd_capacity ^ priority)
        self.hdd_capacity = hard35.hdd_capacity


class Ssd(Component):
    def __init__(self, ssd, priority=1):
        super().__init__(ssd, ssd.drive_volume ^ priority)
        self.drive_volume = ssd.drive_volume

