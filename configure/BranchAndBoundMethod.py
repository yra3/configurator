from django.db.models import F

from configure.ConfigurationFinder import ConfigurationFinder
from configure.ObjectiveFunctionInterface import ObjectiveFunctionInterface
from configure.ObjectiveFunctionUseDict import ObjectiveFunctionUseDict
from configure.models import *



class BranchAndBoundMethod(ConfigurationFinder):
    def __init__(self, budget: int, component_priorities: dict, lower_estimate, hdd_ssd_ssdhdd=2, is_benchmark_find=0):
        super().__init__(budget)
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        self.lower_estimate = lower_estimate
        self.budget_constraints = self._get_budget_constraints()
        if is_benchmark_find==0:
            self.maximize_component = ['-price', '-price']
        else:
            self.maximize_component = ['-benchmark_mark', '-benchmark_mark']
        self.is_benchmark_find = is_benchmark_find

    def _get_budget_constraints(self):
        """:returns: maximum price for each component"""
        budget_constraints = dict()
        for component_name, cost in self.component_priorities.items():
            budget_constraints[component_name] = cost * self.budget + 0.1
        return budget_constraints

    def _find_hdd(self, budget_constraint):
        return hard35.objects.filter(price__lte=self._get_budget_constraints()['hard_35']).order_by('-hdd_capacity')

    def _find_ssd(self, budget_constraint):
        return SSD.objects.filter(price__lte=self._get_budget_constraints()['ssd']).order_by('-drive_volume')

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
        return hard1, ssd1

    def inner_join(configure_list: list, component_list):
        return [tuple(list(configure) + [component]) for configure in configure_list for component in component_list]

    def objective_function(self, configurations):
        answer = 0
        for name, value in parameters.items():
            answer += self.coefficients[name] * value
        return answer

    def summary_price(configure: list):
        sum = 0
        for bit in configure:
            sum += bit.price
        return sum

    def find(self):
        budget_constraints = self._get_budget_constraints()

        # TODO add func witch find component with maximum value of some attribute
        cpus = CPU.objects.filter(price__lte=budget_constraints['CPU']).order_by(self.maximize_component[0])
        best_available_cpu = cpus.first()
        if self.is_benchmark_find==0:
            worst_from_better_cpu = best_available_cpu.price + 1
        else:
            worst_from_better_cpu = best_available_cpu.benchmark_mark + 1

        gpus = GPU.objects.filter(price__lte=budget_constraints['GPU']).order_by(self.maximize_component[1])
        best_available_gpu = gpus.first()
        if self.is_benchmark_find == 0:
            worst_from_better_gpu = best_available_gpu.price + 1
        else:
            worst_from_better_gpu = best_available_gpu.benchmark_mark + 1

        mothers = motherboard.objects.filter(price__lte=budget_constraints['motherboard']).order_by(
                '-price')  # 'price'
        best_available_mother = mothers.first()
        worst_from_better_motherboards = best_available_mother.price + 1

        rams = RAM.objects.filter(price__lte=budget_constraints['RAM']
                                  ).annotate(stars_per_user=F('the_volume_of_one_memory_module'
                                  ) * F('number_of_modules_included')).order_by('-stars_per_user')
        best_available_ram = rams.first()
        worst_from_better_rams = best_available_ram.the_volume_of_one_memory_module\
                                 * best_available_ram.number_of_modules_included + 1

        coolers = cooler.objects.filter(price__lte=budget_constraints['cooler']).order_by('-power_dissipation')
        best_available_cooler = coolers.first()
        worst_from_better_coolers = best_available_cooler.power_dissipation + 1

        hards, ssds = self._find_hdd_ssd(budget_constraints)
        best_available_hard = hards.first()
        worst_from_better_hard = best_available_hard.hdd_capacity + 1

        best_available_ssd = ssds.first()
        worst_from_better_ssd = best_available_ssd.drive_volume + 1

        powersupplies = powersupply.objects.filter(price__lte=budget_constraints['powersupply']
                                                   ).order_by('-power_nominal')
        best_available_powersupply = powersupplies.first()
        worst_from_better_powersupply = best_available_powersupply.drive_volume + 1

        components = [gpus, mothers, rams, coolers, hards, ssds, powersupplies]
        cgs = [tuple([c] + [g]) for c in cpus for g in gpus]

        bad_confs = set()  # cpu and gpu
        for cg in cgs:
            if self.summary_price(cg) > self.budget:
                bad_confs.add(cg)
                continue
            if cg[0].price+cg[1].price<+
        cgs = set(cgs).difference(bad_confs)
        print(len(cgs))

        cgms = inner_join(cgs, mothers)

        bad_confs = set()
        for cgm in cgms:
            if (summary_price(cgm) > budget or
                    cgm[0].socket != cgm[2].socket):
                bad_confs.add(cgm)
        cgms = set(cgms).difference(bad_confs)

        cgmrs = inner_join(cgms, rams)

        print(len(cgmrs))
        bad_confs = set()
        for cgmr in cgmrs:
            if (cgmr[2].supported_memory_form_factor != 'DIMM' or  # configure only desktops
                    cgmr[3].memory_form_factor != 'DIMM' or  # configure only desktops
                    cgmr[2].supported_memory_type != cgmr[3].memory_type or
                    convert_to_int(cgmr[3].number_of_modules_included) > convert_to_int(
                        cgmr[2].number_of_memory_slots) or
                    convert_to_int(cgmr[2].maximum_memory_frequency) < convert_to_int(cgmr[3].clock_frequency) or
                    convert_to_int(cgmr[2].minimum_memory_frequency) > convert_to_int(cgmr[3].clock_frequency) or
                    convert_to_int(cgmr[0].maximum_frequency_of_ram) < convert_to_int(cgmr[3].clock_frequency) or
                    convert_to_int(cgmr[0].minimum_frequency_of_ram) > convert_to_int(cgmr[3].clock_frequency) or
                    summary_price(cgmr) > budget
            ):
                bad_confs.add(cgmr)
        print(len(cgmrs))
        cgmrs = set(cgmrs).difference(bad_confs)
        print(len(cgmrs))
        # end ram compotib

        cgmrcs = [tuple(list(conf) + [component]) for conf in cgmrs for component in coolers]
        bad_confs = set()
        for cgmrc in cgmrcs:
            if (convert_to_int(cgmrc[0].heat_dissipation_tdp) > convert_to_int(cgmrc[4].power_dissipation) or
                    cgmrc[0].socket in cgmrc[4].socket.split(', ') or
                    summary_price(cgmrc) > budget
            ):
                bad_confs.add(cgmrc)
        cgmrcs = set(cgmrcs).difference(bad_confs)
        print(len(cgmrcs))

        cgmrchs = [tuple(list(conf) + [component]) for conf in cgmrcs for component in hards]
        bad_confs = set()
        for cgmrch in cgmrchs:
            if summary_price(cgmrch) > budget:
                bad_confs.add(cgmrch)
        cgmrchs = set(cgmrchs).difference(bad_confs)
        print(len(cgmrchs))

        cgmrchps = [tuple(list(conf) + [component]) for conf in cgmrchs for component in powersupplies]
        print(len(cgmrchps))
        bad_confs = set()
        for cgmrchp in cgmrchps:
            if (summary_price(cgmrchp) > budget or
                    convert_to_int(cgmrchp[6].power_nominal) <= convert_to_int(cgmrchp[0].heat_dissipation_tdp) +
                    convert_to_int(cgmrchp[1].maximum_power_consumption) + 5 + 20 + 9 + 6 + 3):
                bad_confs.add(cgmrchp)
        cgmrchps = set(cgmrchps).difference(bad_confs)
        print(len(cgmrchps))



        # TODO add try except construction for each loop iteration
        cpus = CPU.objects.filter(price__lt=budget_constraints['CPU']).order_by(self.maximize_component[0])  # 'price'
        for cpu in cpus:
            # TODO add using difference between component cost and component max cost

            # For configure only desktops supported_memory_form_factor='DIMM'
            # TODO add filter motherboard.ram_min_frequency < cpu.ram_max_frequency
            mother = motherboard.objects.filter(price__lt=budget_constraints['motherboard'],
                                                socket__iexact=cpu.socket,
                                                supported_memory_form_factor__iexact='DIMM'
                                                ).order_by(self.maximize_component[2]).first()

            gpu = GPU.objects.filter(price__lt=budget_constraints['GPU']).order_by(
                self.maximize_component[1]).first()  # 'price'

            # TODO uncomment next 2 rows, when change db attributes to integer
            # maximum_ram_frequency = min(mother.maximum_memory_frequency, cpu.maximum_frequency_of_ram)
            # minimum_memory_frequency = max(mother.minimum_memory_frequency, cpu.minimum_frequency_of_ram)
            ram1 = RAM.objects.filter(price__lt=budget_constraints['RAM'],
                                      memory_form_factor__iexact='DIMM',
                                      memory_type__iexact=mother.supported_memory_type,
                                      # TODO uncomment, when change db attributes to integer
                                      # number_of_modules_included__lte=mother.number_of_memory_slots,
                                      # clock_frequency__range=(minimum_memory_frequency, maximum_ram_frequency),
                                      # number_of_modules_included__lte=F('number_of_memory_slots')
                                      # // mother.max_ram_memory,
                                      # TODO change order by when change db attributes to integer
                                      # ).annotate(stars_per_user=F('number_of_memory_slots') *
                                      # F('number_of_modules_included')).order_by('-stars_per_user').first()
                                      ).order_by('price').first()

            cooler1 = cooler.objects.filter(price__lt=budget_constraints['cooler'],
                                            socket__in=mother.socket,
                                            # TODO uncomment next row, when change db attributes to integer
                                            # power_dissipation__gt=cpu.heat_dissipation_tdp
                                            ).order_by('power_dissipation').first()

            if self.hdd_ssd_ssdhdd == 0:
                hard1 = self._find_hdd(budget_constraints['hdd'])
                ssd1 = None
            elif self.hdd_ssd_ssdhdd == 1:
                ssd1 = self._find_ssd(budget_constraints['ssd'])
                hard1 = None
            elif self.hdd_ssd_ssdhdd == 2:
                hard1 = self._find_hdd(budget_constraints['hdd'])
                ssd1 = self._find_ssd(budget_constraints['ssd'])
            else:
                raise Exception(AttributeError)


            # TODO uncomment next row, when change db attributes to integer
            # summary_tdp = cpu.heat_dissipation_tdp + gpu.maximum_power_consumption + 5 + 20 + 9 + 6 + 3
            powersupply1 = powersupply.objects.filter(price__lt=budget_constraints['powersupply'],
                                                      # TODO uncomment next row, when change db attributes to integer
                                                      # power_nominal__gt=summary_tdp,
                                                      ).order_by('power_nominal').first()

            return cpu, gpu, mother, ram1, cooler1, hard1, ssd1, powersupply1
