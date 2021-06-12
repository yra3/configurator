

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