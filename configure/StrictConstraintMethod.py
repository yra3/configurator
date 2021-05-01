from configure.ConfigurationFinder import ConfigurationFinder
from configure.ObjectiveFunctionInterface import ObjectiveFunctionInterface
from configure.ObjectiveFunctionUseDict import ObjectiveFunctionUseDict
from configure.models import *

maximize_component = ['price', 'price', 'count_of_memory']


class StrictConstraintMethod(ConfigurationFinder):
    def __init__(self, budget: int, component_priorities: dict, hdd_ssd_ssdhdd=2, is_benchmark_find=0):
        super().__init__(budget)
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        self.is_benchmark_find = is_benchmark_find

    def _get_budget_constraints(self):
        """:returns: maximum price for each component"""
        budget_constraints = dict()
        for component_name, cost in self.component_priorities.items():
            budget_constraints[component_name] = cost * self.budget
        return budget_constraints


    def find_hdd(self, budget_constraint):
        return hard35.objects.filter(price__lt=budget_constraint).order_by('hdd_capacity').first()

    def find_ssd(self, budget_constraint):
        return SSD.objects.filter(price__lt=budget_constraint).order_by('drive_volume').first()

    def find(self):
        budget_constraints = self._get_budget_constraints()

        # TODO add try except construction for each loop iteration
        cpus = CPU.objects.filter(price__lt=budget_constraints['CPU']).order_by(maximize_component[0])  # 'price'
        for cpu in cpus:
            # TODO add using difference between component cost and component max cost

            # For configure only desktops supported_memory_form_factor='DIMM'
            # TODO add filter motherboard.ram_min_frequency < cpu.ram_max_frequency
            mother = motherboard.objects.filter(price__lt=budget_constraints['motherboard'],
                                                socket__iexact=cpu.socket,
                                                supported_memory_form_factor__iexact='DIMM'
                                                ).order_by(maximize_component[2]).first()

            gpu = GPU.objects.filter(price__lt=budget_constraints['GPU']).order_by(
                maximize_component[1]).first()  # 'price'

            # TODO uncomment next 2 rows, when change db attributes to integer
            # maximum_ram_frequency = min(mother.maximum_memory_frequency, cpu.maximum_frequency_of_ram)
            # minimum_memory_frequency = max(mother.minimum_memory_frequency, cpu.minimum_frequency_of_ram)
            ram1 = RAM.objects.filter(price__lt=budget_constraints['RAM'],
                                      memory_form_factor__iexact='DIMM',
                                      memory_type__iexact=mother.supported_memory_type,
                                      # TODO add filter memory*number_of_modules< mother.max_ram_memory
                                      # TODO uncomment next 3 rows, when change db attributes to integer
                                      # number_of_modules_included__lte=mother.number_of_memory_slots,
                                      # clock_frequency__lt=maximum_ram_frequency,
                                      # clock_frequency__gt=minimum_memory_frequency,
                                      ).order_by(maximize_component[1]).first()

            cooler1 = cooler.objects.filter(price__lt=budget_constraints['cooler'],
                                            socket__in=mother.socket,
                                            # TODO uncomment next row, when change db attributes to integer
                                            # power_dissipation__gt=cpu.heat_dissipation_tdp
                                            ).order_by('power_dissipation').first()

            # TODO add ability to switch between hdd, ssd, ssd+hdd modes
            if self.hdd_ssd_ssdhdd == 0:
                hard1 = self.find_hdd(budget_constraints['hdd'])
                ssd1 = None
            elif self.hdd_ssd_ssdhdd == 1:
                ssd1 = self.find_ssd(budget_constraints['ssd'])
                hard1 = None
            elif self.hdd_ssd_ssdhdd == 2:
                hard1 = self.find_hdd(budget_constraints['hdd'])
                ssd1 = self.find_ssd(budget_constraints['ssd'])
            else:
                raise Exception(AttributeError)


            # TODO uncomment next row, when change db attributes to integer
            # summary_tdp = cpu.heat_dissipation_tdp + gpu.maximum_power_consumption + 5 + 20 + 9 + 6 + 3
            powersupply1 = powersupply.objects.filter(price__lt=budget_constraints['powersupply'],
                                                      # TODO uncomment next row, when change db attributes to integer
                                                      # power_nominal__gt=summary_tdp,
                                                      ).order_by('power_nominal').first()

            return cpu, gpu, mother, ram1, cooler1, hard1, ssd1, powersupply1
