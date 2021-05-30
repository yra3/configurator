from datetime import time

from django.db.models import F

from configure.StrictConstraintMethod import StrictConstraintMethod
from configure.ConfigurationFinder import ConfigurationFinder
from configure.Configuration import *


class BranchAndBoundMethod(ConfigurationFinder):
    def __init__(self, budget: int, component_priorities: dict, hdd_ssd_ssdhdd=2, is_benchmark_find=0):
        super().__init__(budget)
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        self.budget_constraints = self._get_budget_constraints()
        if is_benchmark_find == 0:
            self.maximize_component = ['-price', '-price']
        else:
            self.maximize_component = ['-benchmark_mark', '-benchmark_mark']
        self.is_benchmark_find = is_benchmark_find
        le = StrictConstraintMethod(budget, component_priorities, hdd_ssd_ssdhdd, is_benchmark_find)
        self.the_best_config = le.find()
        try:
            self.lower_estimate = self.objective_function(self.the_best_config)
        except:
            self.lower_estimate = 0
        from webconf.settings import DEBUG
        if DEBUG:
            try:
                self._print_config(self.the_best_config)
            except:
                pass

    def _get_budget_constraints(self):
        """:returns: maximum price for each component"""
        budget_constraints = dict()
        for component_name, cost in self.component_priorities.items():
            budget_constraints[component_name] = (cost + 0.05) * self.budget
        return budget_constraints

    # def _print_config(self, config):
    #     lel = list(config)
    #     resp = ''
    #     for c in lel:
    #         if c.__class__ == RAM:
    #             resp += str(c.number_of_modules_included) + ' * '
    #         resp += c.name + '\n'
    #     print(self.lower_estimate)
    #     print(resp)
    #     for c in lel:
    #         print(c.price)
    #     print()

    # def objective_function(self, components):
    #     cpu, gpu, mother, ram, cooler1, hard, ssd, ps1 = components
    #     answer = cpu.price * self.component_priorities['CPU'] \
    #              + gpu.price * self.component_priorities['GPU'] \
    #              + mother.price * self.component_priorities['motherboard'] \
    #              + ram.the_volume_of_one_memory_module * ram.number_of_modules_included * self.component_priorities[
    #                  'RAM'] \
    #              + cooler1.power_dissipation * self.component_priorities['cooler'] \
    #              + hard.hdd_capacity * self.component_priorities['hard_35'] \
    #              + ssd.drive_volume * self.component_priorities['ssd'] \
    #              + ps1.power_nominal * self.component_priorities['powersupply']
    #
    #     return answer



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
                                                    supported_memory_form_factor='dimm'#TODO test
                                                    ).order_by('price')
        mothers = [Motherboard(mother) for mother in mothers]  # create list of not Model ram objects

        rams = models.RAM.objects.filter(price__lte=budget_constraints['RAM'],
                                         memory_form_factor__isnull=False, memory_type__isnull=False,
                                         number_of_modules_included__isnull=False, clock_frequency__isnull=False,
                                         the_volume_of_one_memory_module__isnull=False,
                                         memory_form_factor='dimm', #TODO test
                                         ).annotate(stars_per_user=F('the_volume_of_one_memory_module'
                                                              ) * F('number_of_modules_included')).order_by(
            '-stars_per_user')
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

    def find(self):
        self.component_lists = self._get_all_available_components()
        self.upper_estimates = self._get_upper_estimates(self.component_lists)
        configuration = Configuration(upper_estimates, self.budget)

        for cpu in component_lists['Cpu']:
            configuration.set_component(cpu, 'Cpu')
            if configuration.get_upper_estimate() < self.lower_estimate:
                configuration.drop_component('Cpu')
                continue
            else:
                for mother in component_lists['Motherboard']:
                    configuration.set_component(mother, 'Motherboard')
                    if configuration.get_upper_estimate()<self.lower_estimate and\
                        configuration.is_available_budget() and\
                        cpu.price<23:
                        pass
                    else
                        for x in mother:
                            pass
                        pass
        return 0

    def find_all(self, cpus):
        if self.hdd_ssd_ssdhdd == 3:
            self.finders = [self.find_cpu
            ,self.find_gpu
            ,self.find_motherboard
            ,self.find_cooler
            ,self.find_ram
            ,self.find_hard
            ,self.find_ssd
            ,self.find_power_supply]
        elif self.hdd_ssd_ssdhdd == 2:
            self.finders = [self.find_cpu
                , self.find_gpu
                , self.find_motherboard
                , self.find_cooler
                , self.find_ram
                , self.find_ssd
                , self.find_power_supply]
        else:
            self.finders = [self.find_cpu
                , self.find_gpu
                , self.find_motherboard
                , self.find_cooler
                , self.find_ram
                , self.find_hard
                , self.find_power_supply]
        self.find()

    def find_cpu(self, configuration, index):
        for cpu in self.component_lists['Cpu']:
            configuration.set_component(cpu, 'Cpu')
            compatibility_condition = True
            if configuration.get_upper_estimate() < self.lower_estimate:
                configuration.drop_component('Cpu')
                continue
            else:
                self.finders[index+1](configuration, index+1)

    def find_gpu(self, configuration, index):
        for cpu in self.component_lists['Cpu']:
            configuration.set_component(cpu, 'Cpu')
            compatibility_condition = True
            if configuration.get_upper_estimate() < self.lower_estimate:
                configuration.drop_component('Cpu')
                continue
            else:
                self.finders[index + 1](configuration, index + 1)

    def find_motherboard(self, configuration, index):
        pass

    def find_cooler(self, configuration, index):
        pass

    def find_ram(self, configuration, index):
        pass

    def find_hard(self, configuration, index):
        pass

    def find_ssd(self, configuration, index):
        pass

    def find_power_supply(self, configuration, index):
        pass

    def asdfawegs(self):

        anabled_cost = (self.lower_estimate - upper_estimate_cpu) / self.component_priorities['CPU']
        cpus = cpus.filter(price__gte=anabled_cost)
        for cpu in cpus:
            if cpu.price * self.component_priorities['CPU'] + upper_estimate_cpu <= self.lower_estimate:
                continue
            else:
                uecg = worst_from_better_motherboards + worst_from_better_ram + worst_from_better_cooler \
                       + worst_from_better_hard + worst_from_better_ssd + worst_from_better_powersupply
                for gpu in gpus:
                    if cpu.price * self.component_priorities['CPU'] + gpu.price * self.component_priorities['GPU'] \
                            + uecg <= self.lower_estimate:
                        continue
                    else:
                        uecgm = worst_from_better_ram + worst_from_better_cooler \
                                + worst_from_better_hard + worst_from_better_ssd + worst_from_better_powersupply
                        for mother in mothers:
                            if mother.socket.lower() != cpu.socket.lower() or \
                                    mother.supported_memory_form_factor.lower() != 'dimm' or \
                                    cpu.price * self.component_priorities['CPU'] \
                                    + gpu.price * self.component_priorities['GPU'] \
                                    + mother.price * self.component_priorities['motherboard'] \
                                    + uecgm <= self.lower_estimate:
                                continue
                            else:
                                uecgmr = worst_from_better_cooler + worst_from_better_hard \
                                         + worst_from_better_ssd + worst_from_better_powersupply
                                maximum_ram_frequency = min(mother.maximum_memory_frequency,
                                                            cpu.maximum_frequency_of_ram)
                                minimum_memory_frequency = max(mother.minimum_memory_frequency,
                                                               cpu.minimum_frequency_of_ram)
                                for ram in rams:
                                    clock_frequency = ram.clock_frequency
                                    # TODO var that will by keep number_of_memory_slots in mother
                                    if ram.memory_form_factor.lower() != 'dimm' or \
                                            ram.memory_type.lower() != mother.supported_memory_type.lower() or \
                                            ram.number_of_modules_included > mother.number_of_memory_slots or \
                                            clock_frequency < minimum_memory_frequency or \
                                            clock_frequency > maximum_ram_frequency or \
                                            ram.the_volume_of_one_memory_module \
                                            * ram.number_of_modules_included \
                                            > mother.maximum_memory or \
                                            cpu.price * self.component_priorities['CPU'] \
                                            + gpu.price * self.component_priorities['GPU'] \
                                            + mother.price * self.component_priorities['motherboard'] \
                                            + ram.the_volume_of_one_memory_module \
                                            * ram.number_of_modules_included * self.component_priorities['RAM'] \
                                            + uecgmr <= self.lower_estimate:
                                        continue
                                    else:
                                        uecgmrc = worst_from_better_hard + worst_from_better_ssd \
                                                  + worst_from_better_powersupply
                                        for cooler1 in coolers:  # I write cooler1 because name cooler already exist
                                            if cooler1.power_dissipation < cpu.heat_dissipation_tdp or \
                                                    mother.socket not in cooler1.socket or \
                                                    cpu.price * self.component_priorities['CPU'] \
                                                    + gpu.price * self.component_priorities['GPU'] \
                                                    + mother.price * self.component_priorities['motherboard'] \
                                                    + ram.the_volume_of_one_memory_module \
                                                    * ram.number_of_modules_included * self.component_priorities['RAM'] \
                                                    + cooler1.power_dissipation * self.component_priorities['cooler'] \
                                                    + uecgmrc <= self.lower_estimate:
                                                continue
                                            else:
                                                uecgmrch = worst_from_better_ssd + worst_from_better_powersupply
                                                for hard in hards:
                                                    if cpu.price * self.component_priorities['CPU'] \
                                                            + gpu.price * self.component_priorities['GPU'] \
                                                            + mother.price * self.component_priorities['motherboard'] \
                                                            + ram.the_volume_of_one_memory_module \
                                                            * ram.number_of_modules_included \
                                                            * self.component_priorities['RAM'] \
                                                            + cooler1.power_dissipation \
                                                            * self.component_priorities['cooler'] \
                                                            + hard.hdd_capacity \
                                                            * self.component_priorities['hard_35'] \
                                                            + uecgmrch <= self.lower_estimate:
                                                        continue
                                                    else:
                                                        uecgmrchs = worst_from_better_powersupply
                                                        for ssd in ssds:
                                                            if cpu.price * self.component_priorities['CPU'] \
                                                                    + gpu.price * self.component_priorities['GPU'] \
                                                                    + mother.price \
                                                                    * self.component_priorities['motherboard'] \
                                                                    + ram.the_volume_of_one_memory_module \
                                                                    * ram.number_of_modules_included \
                                                                    * self.component_priorities['RAM'] \
                                                                    + cooler1.power_dissipation \
                                                                    * self.component_priorities['cooler'] \
                                                                    + hard.hdd_capacity \
                                                                    * self.component_priorities['hard_35'] \
                                                                    + ssd.drive_volume \
                                                                    * self.component_priorities['ssd'] \
                                                                    + uecgmrch <= self.lower_estimate:
                                                                continue
                                                            else:
                                                                ps1 = powersupplies.filter(power_nominal__gt=
                                                                                           cpu.heat_dissipation_tdp +
                                                                                           gpu.maximum_power_consumption +
                                                                                           5 + 20 + 9 + 6 + 3,
                                                                                           ).order_by('-power_nominal'
                                                                                                      # TODO replace order_by.first to find_max
                                                                                                      ).first()
                                                                obj_func = cpu.price * self.component_priorities['CPU'] \
                                                                           + gpu.price * self.component_priorities[
                                                                               'GPU'] \
                                                                           + mother.price \
                                                                           * self.component_priorities['motherboard'] \
                                                                           + ram.the_volume_of_one_memory_module \
                                                                           * ram.number_of_modules_included \
                                                                           * self.component_priorities['RAM'] \
                                                                           + cooler1.power_dissipation \
                                                                           * self.component_priorities['cooler'] \
                                                                           + hard.hdd_capacity \
                                                                           * self.component_priorities['hard_35'] \
                                                                           + ssd.drive_volume \
                                                                           * self.component_priorities['ssd'] \
                                                                           + ps1.power_nominal \
                                                                           * self.component_priorities['powersupply']
                                                                if obj_func > self.lower_estimate:
                                                                    self.lower_estimate = obj_func
                                                                    self.the_best_config = (cpu, gpu, mother, ram,
                                                                                            cooler1, hard, ssd,
                                                                                            ps1)
                                                                    from webconf.settings import DEBUG

                                                                    if DEBUG:
                                                                        self._print_config(self.the_best_config)

                                                                    # TODO add outer continues

        return self.the_best_config
