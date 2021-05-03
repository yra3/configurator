from django.db.models import F

from configure.ConfigurationFinder import ConfigurationFinder
from configure.ObjectiveFunctionInterface import ObjectiveFunctionInterface
from configure.ObjectiveFunctionUseDict import ObjectiveFunctionUseDict
from configure.models import *


class StrictConstraintMethod(ConfigurationFinder):
    def __init__(self, budget: int, component_priorities: dict, hdd_ssd_ssdhdd=2, is_benchmark_find=0):
        super().__init__(budget)
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        if is_benchmark_find == 0:
            self.maximize_component = ['-price', '-price', '-count_of_memory']
        else:
            self.maximize_component = ['-benchmark_mark', '-benchmark_mark', '-count_of_memory']
        self.is_benchmark_find = is_benchmark_find

    def _get_budget_constraints(self):
        """:returns: maximum price for each component"""
        budget_constraints = dict()
        for component_name, cost in self.component_priorities.items():
            budget_constraints[component_name] = cost * self.budget
        return budget_constraints

    def _find_hdd(self, budget_constraint):
        return hard35.objects.filter(price__lt=budget_constraint).order_by('-hdd_capacity')

    def _find_ssd(self, budget_constraint):
        return SSD.objects.filter(price__lt=budget_constraint).order_by('-drive_volume')

    def _find_hdd_ssd(self, budget_constraints):
        if self.hdd_ssd_ssdhdd == 0:
            hard1 = self._find_hdd(budget_constraints['hard_35'])
            ssd1 = None
        elif self.hdd_ssd_ssdhdd == 1:
            ssd1 = self._find_ssd(budget_constraints['ssd'])
            hard1 = None
        elif self.hdd_ssd_ssdhdd == 2:
            hard1 = self._find_hdd(budget_constraints['hard_35'])
            ssd1 = self._find_ssd(budget_constraints['ssd'])
        else:
            raise Exception(AttributeError)
        return zip(hard1, ssd1)

    def find(self):
        budget_constraints = self._get_budget_constraints()

        cpus = CPU.objects.filter(price__lte=budget_constraints['CPU']).order_by(self.maximize_component[0])  # 'price'
        for cpu in cpus:
            try:
                # TODO add using difference between component cost and component max cost
                # TODO add cashing components
                # For configure only desktops supported_memory_form_factor='DIMM'
                for mother in motherboard.objects.filter(price__lte=budget_constraints['motherboard'],
                                                         socket__iexact=cpu.socket,
                                                         supported_memory_form_factor__iexact='DIMM'
                                                         ).order_by('-price'):
                    for gpu in GPU.objects.filter(price__lt=budget_constraints['GPU']).order_by(
                            self.maximize_component[1]):
                        # TODO add checking Null attributes like in row below
                        if gpu.maximum_power_consumption is None:
                            continue

                        maximum_ram_frequency = min(mother.maximum_memory_frequency, cpu.maximum_frequency_of_ram)
                        minimum_memory_frequency = max(mother.minimum_memory_frequency, cpu.minimum_frequency_of_ram)

                        for ram1 in RAM.objects.filter(price__lte=budget_constraints['RAM'],
                                                       memory_form_factor__iexact='DIMM',
                                                       memory_type__iexact=mother.supported_memory_type,
                                                       number_of_modules_included__lte=mother.number_of_memory_slots,
                                                       clock_frequency__range=(
                                                               minimum_memory_frequency, maximum_ram_frequency),
                                                       the_volume_of_one_memory_module__lte=mother.maximum_memory /
                                                                                            F(
                                                                                                'number_of_modules_included'),
                                                       ).annotate(stars_per_user=F('the_volume_of_one_memory_module') *
                                                                                 F(
                                                                                     'number_of_modules_included')).order_by(
                            '-stars_per_user'):

                            # TODO add sort with 2 parms tdp and cost
                            for cooler1 in cooler.objects.filter(price__lte=budget_constraints['cooler'],
                                                                 socket__icontains=mother.socket,
                                                                 power_dissipation__gte=cpu.heat_dissipation_tdp
                                                                 ).order_by('-power_dissipation'):

                                for hard1, ssd1 in self._find_hdd_ssd(budget_constraints):
                                    summary_tdp = cpu.heat_dissipation_tdp + gpu.maximum_power_consumption + 5 + 20 + 9 + 6 + 3
                                    powersupply1 = powersupply.objects.filter(
                                        price__lte=budget_constraints['powersupply'],
                                        power_nominal__gt=summary_tdp,
                                    ).order_by('-power_nominal').first()
                                    return cpu, gpu, mother, ram1, cooler1, hard1, ssd1, powersupply1
            except:
                pass
