import sys
from datetime import time

from django.db.models import F

from configure.Configuration import *
from webconf.settings import DEBUG
from multiprocessing import Process, Lock, cpu_count, Value, Array


class BranchAndBoundMethod:
    def __init__(self, budget: int, component_priorities: dict, hdd_ssd_ssdhdd=2, is_benchmark_find=0):
        """:param: hdd_ssd_ssdhdd  hdd_mode - 0, ssd - 1, hdd and ssd - 2
        :param is_benchmark_find: 0 - use price of component, 1 - use benchmark"""
        self.budget = budget
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        self.budget_constraints = self._get_budget_constraints()
        if is_benchmark_find == 0:
            self.maximize_component = ['-price', '-price']
        else:
            self.maximize_component = ['-benchmark_mark', '-benchmark_mark']
        self.is_benchmark_find = is_benchmark_find
        self.set_types()
        self.lower_estimate = 0

    def set_types(self):
        if self.hdd_ssd_ssdhdd == 2:
            self.component_types = [
                'Cpu', 'Gpu', 'Motherboard', 'Ram', 'Cooler', 'Hard35', 'Ssd', 'PowerSupply'
            ]
        elif self.hdd_ssd_ssdhdd == 1:
            self.component_types = [
                'Cpu', 'Gpu', 'Motherboard', 'Ram', 'Cooler', 'Ssd', 'PowerSupply'
            ]
        elif self.hdd_ssd_ssdhdd == 0:
            self.component_types = [
                'Cpu', 'Gpu', 'Motherboard', 'Ram', 'Cooler', 'Hard35' 'PowerSupply'
            ]
        self.count_components = len(self.component_types)

    def _get_budget_constraints(self):
        """:returns: maximum price for each component"""
        budget_constraints = dict()
        for component_name, cost in self.component_priorities.items():
            budget_constraints[component_name] = (cost + 0.02) * self.budget
        return budget_constraints

    def _print_config(self, config):
        """Func only for Debug"""
        resp = ''
        for component_type, component in config.items():
            if component_type == 'Ram':
                resp += str(component.number_of_modules_included) + ' * '
            resp += component.name + '\n'
        print(self.lower_estimate)
        print(resp)
        ыгь = 0
        for component in config.values():
            print(component.price)
            ыгь+= component.price
        print(ыгь)

    def _get_all_available_components(self, cpu=True, gpu=True, mother=True, ram=True,
                                      cool=True, hard=True, ssd=True, power_supply=True, user_constrains=[]):
        """Parameters decide which components will be returned
        :return: dict of components lists, that does not contain
        overpriced components and components with None attributes.
        Key = components type
        value = list<Component>
        Each list sorted by maximized component"""
        from . import models
        # TODO add user constrains
        # budget_constraints keeps max available budget values for each component
        budget_constraints = self._get_budget_constraints()

        # TODO add conditions like writen below:
        # component_lists = {}
        # if cpu:
        #     component_lists['Cpu'] = cpus = models.CPU.objects.filter(price__lte=budget_constraints['CPU'],

        # find all available cpu in database without null values in attributes used in configuring and sort it
        cpus = models.CPU.objects.filter(price__lte=budget_constraints['CPU'], socket__isnull=False,
                                         maximum_frequency_of_ram__isnull=False, minimum_frequency_of_ram__isnull=False,
                                         heat_dissipation_tdp__isnull=False, ).order_by(self.maximize_component[0])
        # maximized attribute selected in Configuration.Cpu.__init__
        cpus = [Cpu(cpu, self.component_priorities['CPU']) for cpu in cpus]  # create list of not Model cpu objects

        gpus = models.GPU.objects.filter(price__lte=budget_constraints['GPU'],
                                         maximum_power_consumption__isnull=False).order_by(self.maximize_component[1])
        # maximized attribute selected in Configuration.Gpu.__init__
        gpus = [Gpu(gpu, self.component_priorities['GPU']) for gpu in gpus]  # create list of not Model gpu objects

        mothers = models.motherboard.objects.filter(price__lte=budget_constraints['motherboard'],
                                                    socket__isnull=False, supported_memory_form_factor__isnull=False,
                                                    supported_memory_type__isnull=False, number_of_memory_slots__isnull=False,
                                                    maximum_memory_frequency__isnull=False,
                                                    minimum_memory_frequency__isnull=False,
                                                    maximum_memory__isnull=False,
                                                    supported_memory_form_factor='dimm'
                                                    ).order_by('price')
        mothers = [Motherboard(mother) for mother in mothers]  # create list of not Model ram objects

        rams = models.RAM.objects.filter(price__lte=budget_constraints['RAM'],
                                         memory_form_factor__isnull=False, memory_type__isnull=False,
                                         number_of_modules_included__isnull=False, clock_frequency__isnull=False,
                                         the_volume_of_one_memory_module__isnull=False,
                                         memory_form_factor='dimm',
                                         ).annotate(stars_per_user=F('the_volume_of_one_memory_module'
                                                              ) * F('number_of_modules_included')).order_by(
            '-stars_per_user', '-clock_frequency', 'price')
        rams = [Ram(ram, self.component_priorities['RAM']) for ram in rams]  # create list of not Model ram objects

        coolers = models.cooler.objects.filter(price__lte=budget_constraints['cooler'],
                                               socket__isnull=False, power_dissipation__isnull=False,
                                               ).order_by('price')
        coolers = [Cooler(cooler) for cooler in coolers]  # create list of not Model cooler objects
        hards = models.hard35.objects.filter(price__lte=self._get_budget_constraints()['hard_35'],
                                             hdd_capacity__isnull=False).order_by('-hdd_capacity')
        hards = [Hard35(hard, self.component_priorities['hard_35'])
                 for hard in hards]  # create list of not Model hard objects
        ssds = models.SSD.objects.filter(price__lte=self._get_budget_constraints()['ssd'],
                                         drive_volume__isnull=False).order_by('-drive_volume')
        ssds = [Ssd(ssd, self.component_priorities['ssd']) for ssd in ssds]  # create list of not Model ssd objects

        powersupplies = models.powersupply.objects.filter(price__lte=budget_constraints['powersupply'],
                                                          power_nominal__isnull=False,
                                                          ).order_by('price')
        powersupplies = [PowerSupply(powersupply) for powersupply in
                         powersupplies]  # create list of not Model ps objects

        component_lists = {'Cpu': cpus, 'Gpu': gpus, 'Motherboard': mothers, 'Ram': rams,
                           'Cooler': coolers, 'Hard35': hards, 'Ssd': ssds, 'PowerSupply': powersupplies}

        return component_lists

    @staticmethod
    def _get_upper_estimates(component_lists: dict):
        """:param component_lists: dict of component types: component list, that can't contain empty list
        :return: dict keys = types of component, values = lists of components"""
        for component_type, components in component_lists.items():
            if component_type is None or len(components) == 0:
                raise AttributeError('Component dict have empty list or None key', component_type, components)
        # we get first component because list must be sorted by maximized component
        return {component_type: components[0].maximized_component for component_type, components in component_lists.items()}

    @staticmethod
    def _get_cheapest_components(component_lists: dict):
        """:param component_lists: dict of component types: component list, that can't contain empty list
        :return: dict keys = types of component, values = lists of components"""
        for component_type, components in component_lists.items():
            if component_type is None or len(components) == 0:
                raise AttributeError('Component dict have empty list or None key', component_type, components)
        # we get first component because list must be sorted by maximized component
        return {component_type: min(components, key=lambda x: x.price).price for component_type, components in
                component_lists.items()}

    def find(self):
        self.component_lists = self._get_all_available_components()
        upper_estimates = self._get_upper_estimates(self.component_lists)
        cheapest = self._get_cheapest_components(self.component_lists)
        configuration = Configuration(upper_estimates, self.budget, cheapest)

        self.find_component(configuration, 0)
        config = {}




        # it's convert from own classes to Model objects
        from . import models
        config['Cpu'] = models.CPU.objects.filter(id=self.the_best_config['Cpu'].id)[0]
        config['Gpu'] = models.GPU.objects.filter(id=self.the_best_config['Gpu'].id)[0]
        config['Motherboard'] = models.motherboard.objects.filter(id=self.the_best_config['Motherboard'].id)[0]
        config['Ram'] = models.RAM.objects.filter(id=self.the_best_config['Ram'].id)[0]
        config['Cooler'] = models.cooler.objects.filter(id=self.the_best_config['Cooler'].id)[0]
        config['Ssd'] = models.SSD.objects.filter(id=self.the_best_config['Ssd'].id)[0]
        config['Hard35'] = models.hard35.objects.filter(id=self.the_best_config['Hard35'].id)[0]
        config['PowerSupply'] = models.powersupply.objects.filter(id=self.the_best_config['PowerSupply'].id)[0]
        return config

    def find_component(self, configuration, index):
        if index != self.count_components:
            component_type = self.component_types[index]
            for component in self.component_lists[component_type]:
                configuration.set_component(component, component_type)
                if configuration.get_upper_estimate() <= self.lower_estimate:
                    configuration.drop_component(component_type)
                    break
                compatibility_condition = configuration.is_compatible(component_type)
                if not compatibility_condition or configuration.get_balance_of_the_budget() < 0:
                    configuration.drop_component(component_type)
                    continue
                self.find_component(configuration, index + 1)
        else:
            objective_function = configuration.get_objective_function()
            if objective_function > self.lower_estimate:
                self.lower_estimate = objective_function
                self.the_best_config = configuration.components.copy()
                if DEBUG:
                    self._print_config(self.the_best_config)

# multiprocess code

    # def find(self):
    #     self.component_lists = self._get_all_available_components()
    #     upper_estimates = self._get_upper_estimates(self.component_lists)
    #     cheapest = self._get_cheapest_components(self.component_lists)
    #
    #     # configuration = Configuration(upper_estimates, self.budget, cheapest)
    #     self.component_lists_for_processes = [None for x in range(cpu_count())]
    #
    #     lock = Lock()
    #     lower_estimate = Value('d', 0)
    #     best_config = Array('i', range(8))
    #     processes = []
    #     process_count = cpu_count() - 1
    #     for i in range(cpu_count()):
    #         self.component_lists_for_processes[i] = self.component_lists.copy()
    #         self.component_lists_for_processes[i]['Cpu'] = self.component_lists['Cpu'][i::cpu_count()]
    #
    #     configurations = [Configuration(self._get_upper_estimates(self.component_lists_for_processes[i]
    #                                                               ), self.budget, cheapest) for i in range(cpu_count())]
    #
    #     for i in range(process_count):
    #         processes.append(Process(target=self.find_component, args=(configurations[i], 0, i, lock, lower_estimate, best_config)))
    #         processes[i].start()
    #     self.find_component(configurations[process_count], 0, process_count, lock, lower_estimate, best_config)
    #     for process in processes:
    #         process.join()
    #
    #
    #     # self.find_component(configuration, 0)
    #     config = {}
    #
    #     # it's convert from own classes to Model objects
    #     from . import models
    #     config['Cpu'] = models.CPU.objects.filter(id=best_config[0])[0]
    #     config['Gpu'] = models.GPU.objects.filter(id=best_config[1])[0]
    #     config['Motherboard'] = models.motherboard.objects.filter(id=best_config[2])[0]
    #     config['Ram'] = models.RAM.objects.filter(id=best_config[3])[0]
    #     config['Cooler'] = models.cooler.objects.filter(id=best_config[4])[0]
    #     config['Hard35'] = models.hard35.objects.filter(id=best_config[5])[0]
    #     config['Ssd'] = models.SSD.objects.filter(id=best_config[6])[0]
    #     config['PowerSupply'] = models.powersupply.objects.filter(id=best_config[7])[0]
    #     # config['Cpu'] = models.CPU.objects.filter(id=self.the_best_config['Cpu'].id)[0]
    #     # config['Gpu'] = models.GPU.objects.filter(id=self.the_best_config['Gpu'].id)[0]
    #     # config['Motherboard'] = models.motherboard.objects.filter(id=self.the_best_config['Motherboard'].id)[0]
    #     # config['Ram'] = models.RAM.objects.filter(id=self.the_best_config['Ram'].id)[0]
    #     # config['Cooler'] = models.cooler.objects.filter(id=self.the_best_config['Cooler'].id)[0]
    #     # config['Ssd'] = models.SSD.objects.filter(id=self.the_best_config['Ssd'].id)[0]
    #     # config['Hard35'] = models.hard35.objects.filter(id=self.the_best_config['Hard35'].id)[0]
    #     # config['PowerSupply'] = models.powersupply.objects.filter(id=self.the_best_config['PowerSupply'].id)[0]
    #     return config
    #
    # def find_component(self, configuration, index, process_number, lock, lower_estimate, best_config):
    #     if index != self.count_components:
    #         component_type = self.component_types[index]
    #         for component in self.component_lists_for_processes[process_number][component_type]:
    #             configuration.set_component(component, component_type)
    #
    #             if configuration.get_upper_estimate() <= lower_estimate.value:
    #                 configuration.drop_component(component_type)
    #                 break
    #             compatibility_condition = configuration.is_compatible(component_type)
    #             if not compatibility_condition or configuration.get_balance_of_the_budget() < 0:
    #                 configuration.drop_component(component_type)
    #                 continue
    #             self.find_component(configuration, index + 1, process_number, lock, lower_estimate, best_config)
    #     else:
    #         lock.acquire()
    #         objective_function = configuration.get_objective_function()
    #         if objective_function > lower_estimate.value:
    #             lower_estimate.value = objective_function
    #             # self.the_best_config = configuration.components.copy()
    #             for i, component in zip(range(8), configuration.components.values()):
    #                 best_config[i] = component.id
    #             if DEBUG:
    #                 #self._print_config(self.the_best_config)
    #                 print(process_number, end=' ')
    #                 print(lower_estimate.value)
    #         lock.release()
