
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
    # def __init__(self):
    #     self.components = {}

    def __init__(self, upper_estimates: dict, maximum_budget: int, minimum_prices: dict):
        """:param maximum_budget: value of maximum available budget, number
        :param upper_estimates: dict with keys - types of components, value - max maximized value that we can get
        :param minimum_prices:  dict with keys - types of components, value - min price that we must spend"""
        self._constructor_parameters_checking(upper_estimates)
        self.maximum_budget = maximum_budget
        self.upper_estimates = upper_estimates
        self.minimum_prices = minimum_prices
        self.components = {component_type: None for component_type in upper_estimates.keys()}

    def drop_component(self, component_type: str):
        self.components[component_type] = None

    def set_component(self, component: Component, component_type: str):
        self.components[component_type] = component

    def get_upper_estimate(self):
        product = 1
        for component_type, component in self.components.items():
            if component is None:
                product *= self.upper_estimates[component_type]
            else:
                product *= component.maximized_component
        return product

    def is_available_budget(self):
        summary_budget = 0
        for component in self.components.values():
            if component is not None:
                summary_budget += component.price
        return summary_budget <= self.maximum_budget

    def get_balance_of_the_budget(self):
        difference = self.maximum_budget
        for component_type, component in self.components.items():
            if component is not None:
                difference -= component.price
            else:
                difference -= self.minimum_prices[component_type]
        return difference

    def get_objective_function(self):
        product = 1
        for component_type, component in self.components.items():
            if component is None:
                raise Exception('Can\'t calculate objective function. Configuration not completed', component_type)
        for component_type, component in self.components.items():
                product *= component.maximized_component
        return product

    def is_completed(self):
        for component_type, component in self.components.items():
            if component is None:
                return False
        return True

    def get_component(self, component_type: str):
        return self.components[component_type]

    @staticmethod
    def _constructor_parameters_checking(upper_estimates: dict):
        for component_type, upper_estimate in upper_estimates.items():
            if upper_estimate is None:
                raise AttributeError('Upper estimates can\'t contain None values', component_type)

    def is_compatible(self, component_type: str):
        """:param component_type: type of component that you want check to compatible
        this method checks compatible between selected component and the rest contained in configuration
        if they are not None"""
        answer = True
        if component_type == 'Cpu':
            return self.is_compatible_cpu()
        elif component_type == 'Gpu':
            return True
        elif component_type == 'Motherboard':
            return self.is_compatible_mother()
        elif component_type == 'Cooler':
            return self.is_compatible_cooler()
        elif component_type == 'Ram':
            return self.is_compatible_ram()
        elif component_type == 'Hard35':
            return True
        elif component_type == 'Ssd':
            return True
        elif component_type == 'PowerSupply':
            return self.is_compatible_power_supply()
        return answer

    def is_compatible_cpu(self):
        """checks compatible between cpu and the rest components contained in configuration(not None)"""
        answer = True
        cpu = self.components['Cpu']
        mother = self.components['Motherboard']
        ram = self.components['Ram']
        cooler = self.components['Cooler']
        if mother is not None:
            answer = answer and cpu.is_compatible_motherboard(mother)
        if ram is not None:
            answer = answer and cpu.is_compatible_ram(ram)
        if cooler is not None:
            answer = answer and cpu.is_compatible_cooler(cooler)
        return answer

    def is_compatible_mother(self):
        """checks compatible between gpu and the rest components contained in configuration(not None)"""
        answer = True
        mother = self.components['Motherboard']
        cpu = self.components['Cpu']
        ram = self.components['Ram']
        cooler = self.components['Cooler']
        if cpu is not None:
            answer = answer and cpu.is_compatible_motherboard(mother)
        if ram is not None:
            answer = answer and mother.is_compatible_ram(ram)
        if cooler is not None:
            answer = answer and mother.is_compatible_cooler(cooler)
        return answer

    def is_compatible_cooler(self):
        """checks compatible between cooler and the rest components contained in configuration(not None)"""
        answer = True
        cooler = self.components['Cooler']
        mother = self.components['Motherboard']
        cpu = self.components['Cpu']
        if cpu is not None:
            answer = answer and cpu.is_compatible_cooler(cooler)
        if mother is not None:
            answer = answer and mother.is_compatible_cooler(cooler)
        return answer

    def is_compatible_ram(self):
        """checks compatible between ram and the rest components contained in configuration(not None)"""
        answer = True
        ram = self.components['Ram']
        cpu = self.components['Cpu']
        mother = self.components['Motherboard']
        if cpu is not None:
            answer = answer and cpu.is_compatible_ram(ram)
        if mother is not None:
            answer = answer and mother.is_compatible_ram(ram)
        return answer

    def is_compatible_hard35(self):
        """checks compatible between hard35 and the rest components contained in configuration(not None)"""
        return True

    def is_compatible_ssd(self):
        """checks compatible between ssd and the rest components contained in configuration(not None)"""
        return True

    def is_compatible_power_supply(self):
        """checks compatible between power supply and the rest components contained in configuration(not None)"""
        power_supply = self.components['PowerSupply']
        cpu = self.components['Cpu']
        gpu = self.components['Gpu']
        if cpu is not None and gpu is not None:
            return power_supply.is_compatible_cpu_and_gpu(cpu, gpu)
        return True


class Cpu(Component):
    def __init__(self, cpu, priority):
        super().__init__(cpu, cpu.price)# ^ priority)
        self.socket = cpu.socket
        self.maximum_frequency_of_ram = cpu.maximum_frequency_of_ram
        self.minimum_frequency_of_ram = cpu.minimum_frequency_of_ram
        self.heat_dissipation_tdp = cpu.heat_dissipation_tdp
        self.bench = cpu.benchmark_mark

    def is_compatible_motherboard(self, motherboard):
        return self.socket.lower() == motherboard.socket.lower()

    def is_compatible_ram(self, ram):
        return self.minimum_frequency_of_ram <= ram.clock_frequency <= self.maximum_frequency_of_ram

    def is_compatible_cooler(self, cooler):
        return self.heat_dissipation_tdp <= cooler.power_dissipation



class Gpu(Component):
    def __init__(self, gpu,  priority):
        super().__init__(gpu, gpu.price)# ^ priority)
        self.maximum_power_consumption = gpu.maximum_power_consumption
        self.bench = gpu.g3d_mark


class Motherboard(Component):
    def __init__(self, motherboard, priority=1):
        super().__init__(motherboard, 1)  # motherboard.price^(-1)
        self.socket = motherboard.socket
        self.supported_memory_form_factor = motherboard.supported_memory_form_factor
        self.supported_memory_type = motherboard.supported_memory_type
        self.maximum_memory_frequency = motherboard.maximum_memory_frequency
        self.minimum_memory_frequency = motherboard.minimum_memory_frequency
        self.maximum_memory = motherboard.maximum_memory
        self.number_of_memory_slots = motherboard.number_of_memory_slots

    def is_compatible_ram(self, ram):
        return (ram.memory_type == self.supported_memory_type
                and self.number_of_memory_slots >= ram.number_of_modules_included
                and self.maximum_memory >= ram.number_of_modules_included * ram.the_volume_of_one_memory_module
                and self.minimum_memory_frequency <= ram.clock_frequency <= self.maximum_memory_frequency)

    def is_compatible_cooler(self, cooler):
        return self.socket.lower() in cooler.socket.lower()



class Ram(Component):
    def __init__(self, ram, priority=1):
        super().__init__(ram, (ram.the_volume_of_one_memory_module*ram.number_of_modules_included))# ^ priority)
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

    def is_compatible_cpu_and_gpu(self, cpu, gpu):
        return self.power_nominal >= cpu.heat_dissipation_tdp + gpu.maximum_power_consumption + 5 + 20 + 9 + 6 + 3


class Hard35(Component):
    def __init__(self, hard35, priority=1):
        super().__init__(hard35, hard35.hdd_capacity)# ^ priority)
        self.hdd_capacity = hard35.hdd_capacity


class Ssd(Component):
    def __init__(self, ssd, priority=1):
        """:param ssd: ssd object with not none attribute drive_volume
        :param priority: coefficient of priority relative to another components"""
        super().__init__(ssd, ssd.drive_volume)# ^ priority)
        self.drive_volume = ssd.drive_volume

