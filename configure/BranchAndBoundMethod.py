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
        self.lower_estimate = 2000
        self.budget_constraints = self._get_budget_constraints()
        if is_benchmark_find == 0:
            self.maximize_component = ['-price', '-price']
        else:
            self.maximize_component = ['-benchmark_mark', '-benchmark_mark']
        self.is_benchmark_find = is_benchmark_find
        from configure.StrictConstraintMethod import StrictConstraintMethod
        le = StrictConstraintMethod(budget, component_priorities, hdd_ssd_ssdhdd, is_benchmark_find)

        lel = [cpu, gpu, mother, ram, cooler1, hard, ssd, ps1] = le.find()
        resp = ''
        for c in lel:
            if c.__class__ == RAM:
                resp += str(c.number_of_modules_included) + ' * '
            resp += c.name + '\n'
        print(resp)
        for c in lel:
            print(c.price)
        print()

        cpu, gpu, mother, ram, cooler1, hard, ssd, ps1 = le.find()

        self.lower_estimate = cpu.price * self.component_priorities['CPU'] \
        + gpu.price * self.component_priorities['GPU'] \
        + mother.price * self.component_priorities['motherboard'] \
        + ram.the_volume_of_one_memory_module * ram.number_of_modules_included * self.component_priorities['RAM'] \
        + cooler1.power_dissipation * self.component_priorities['cooler'] \
        + hard.hdd_capacity * self.component_priorities['hard_35'] \
        + ssd.drive_volume * self.component_priorities['ssd'] \
        + ps1.power_nominal * self.component_priorities['powersupply']
        print(self.lower_estimate)

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

    def objective_function(self, components, priorytes):
        answer = 0
        # for name, value in parameters.items():
        #     answer += self.coefficients[name] * value
        return answer

    def summary_price(configure: list):
        sum = 0
        for bit in configure:
            sum += bit.price
        return sum
        # return 2000

    def find(self):
        budget_constraints = self._get_budget_constraints()

        # TODO add func witch find component with maximum value of some attribute
        cpus = CPU.objects.filter(price__lte=budget_constraints['CPU'], socket__isnull=False,
                                  maximum_frequency_of_ram__isnull=False, minimum_frequency_of_ram__isnull=False,
                                  heat_dissipation_tdp__isnull=False, ).order_by(self.maximize_component[0])
        best_available_cpu = cpus.first()
        if self.is_benchmark_find == 0:
            worst_from_better_cpu = best_available_cpu.price + 1
        else:
            worst_from_better_cpu = best_available_cpu.benchmark_mark + 1

        gpus = GPU.objects.filter(price__lte=budget_constraints['GPU'],
                                  maximum_power_consumption__isnull=False).order_by(self.maximize_component[1])
        best_available_gpu = gpus.first()
        if self.is_benchmark_find == 0:
            worst_from_better_gpu = best_available_gpu.price + 1
        else:
            worst_from_better_gpu = best_available_gpu.benchmark_mark + 1
        worst_from_better_gpu *= self.component_priorities['GPU']

        mothers = motherboard.objects.filter(price__lte=budget_constraints['motherboard'],
                                             socket__isnull=False, supported_memory_form_factor__isnull=False,
                                             supported_memory_type__isnull=False,number_of_memory_slots__isnull=False,
                                             maximum_memory_frequency__isnull=False,
                                             minimum_memory_frequency__isnull=False,
                                             maximum_memory__isnull=False,

                                             ).order_by('-price')  # 'price'
        best_available_mother = mothers.first()
        worst_from_better_motherboards = best_available_mother.price + 1
        worst_from_better_motherboards *= self.component_priorities['motherboard']

        rams = RAM.objects.filter(price__lte=budget_constraints['RAM'],
                                  memory_form_factor__isnull=False, memory_type__isnull=False,
                                  number_of_modules_included__isnull=False, clock_frequency__isnull=False,
                                  the_volume_of_one_memory_module__isnull=False,
                                  ).annotate(stars_per_user=F('the_volume_of_one_memory_module'
                                                              ) * F('number_of_modules_included')).order_by(
            '-stars_per_user')
        best_available_ram = rams.first()
        worst_from_better_ram = best_available_ram.the_volume_of_one_memory_module \
                                * best_available_ram.number_of_modules_included + 1
        worst_from_better_ram *= self.component_priorities['RAM']

        coolers = cooler.objects.filter(price__lte=budget_constraints['cooler'],
                                        socket__isnull=False, power_dissipation__isnull=False,
                                        ).order_by('-power_dissipation')
        best_available_cooler = coolers.first()
        worst_from_better_cooler = best_available_cooler.power_dissipation + 1
        worst_from_better_cooler *= self.component_priorities['cooler']

        hards, ssds = self._find_hdd_ssd(budget_constraints)
        best_available_hard = hards.first()
        worst_from_better_hard = best_available_hard.hdd_capacity + 1
        worst_from_better_hard *= self.component_priorities['hard_35']

        best_available_ssd = ssds.first()
        worst_from_better_ssd = best_available_ssd.drive_volume + 1
        worst_from_better_ssd *= self.component_priorities['ssd']

        powersupplies = powersupply.objects.filter(price__lte=budget_constraints['powersupply'],
                                                   power_nominal__isnull=False,
                                                   ).order_by('-power_nominal')
        best_available_powersupply = powersupplies.first()
        worst_from_better_powersupply = best_available_powersupply.power_nominal + 1
        worst_from_better_powersupply *= self.component_priorities['powersupply']

        upper_estimate_cpu = worst_from_better_gpu + worst_from_better_motherboards + worst_from_better_ram \
                                 + worst_from_better_cooler + worst_from_better_hard + worst_from_better_ssd \
                                 + worst_from_better_powersupply
        # if cpu.price*c1 + upper_estimate_for_cpu < lower_estimate:       <- это псевдокод
        #     drop                                                         <- это псевдокод
        # cpu.price*c1 < self.lower_estimate-upper_estimate_for_cpu        <- это псевдокод
        # cpu.price < (self.lower_estimate - upper_estimate_for_cpu) / c1  <- это псевдокод
        # cpu.price >= (self.lower_estimate - upper_estimate_for_cpu) / c1 <- это псевдокод
        # not drop                                                         <- это псевдокод

        anabled_cost = (self.lower_estimate - upper_estimate_cpu) / self.component_priorities['CPU']
        cpus = cpus.filter(price__gte=anabled_cost)
        # TODO move each if into a function
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
                            if mother.socket.lower() != cpu.socket.lower() or\
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
                                            ram.memory_type.lower() != mother.supported_memory_type.lower() or\
                                            ram.number_of_modules_included > mother.number_of_memory_slots or\
                                            clock_frequency < minimum_memory_frequency or \
                                            clock_frequency > maximum_ram_frequency or \
                                            ram.the_volume_of_one_memory_module \
                                                * ram.number_of_modules_included\
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
                                                    * ram.number_of_modules_included * self.component_priorities['RAM']\
                                                    + cooler1.power_dissipation * self.component_priorities['cooler']\
                                                    + uecgmrc <= self.lower_estimate:
                                                continue
                                            else:
                                                uecgmrch =  worst_from_better_ssd + worst_from_better_powersupply
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
                                                            * self.component_priorities['hard_35']\
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
                                                                    * self.component_priorities['ssd']\
                                                                    + uecgmrch <= self.lower_estimate:
                                                                continue
                                                            else:
                                                                ps1 = powersupplies.filter(power_nominal__gt=
                                                                                     cpu.heat_dissipation_tdp +
                                                                                     gpu.maximum_power_consumption +
                                                                                     5 + 20 + 9 + 6 + 3,
                                                                                     ).order_by('-power_nominal'  # TODO replace order_by.first to find_max
                                                                                                ).first()
                                                                obj_func = cpu.price * self.component_priorities['CPU']\
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
                                                                    * self.component_priorities['ssd']\
                                                                    + ps1.power_nominal \
                                                                    * self.component_priorities['powersupply']
                                                                if obj_func > self.lower_estimate:
                                                                    self.lower_estimate = obj_func
                                                                    print(self.lower_estimate)
                                                                    self.the_best_config = (cpu, gpu, mother, ram,
                                                                                            cooler1, hard, ssd,
                                                                                            ps1)
                                                                    resp = ''
                                                                    for c in list(self.the_best_config):
                                                                        if c.__class__ == RAM:
                                                                            resp += str(
                                                                                c.number_of_modules_included) + ' * '
                                                                        resp += c.name + '\n'
                                                                    print(resp)
                                                                    for c in list(self.the_best_config):
                                                                        print(c.price)
                                                                    print()
                                                                    # TODO add outer continues
        print(self.lower_estimate)
        return self.the_best_config










        components = [gpus, mothers, rams, coolers, hards, ssds, powersupplies]
        cgs = [tuple([c] + [g]) for c in cpus for g in gpus]

        bad_confs = set()  # cpu and gpu
        for cg in cgs:
            if self.summary_price(cg) > self.budget:
                bad_confs.add(cg)
                continue
            # if cg[0].price+cg[1].price<+
        cgs = set(cgs).difference(bad_confs)
        print(len(cgs))

        cgms = self.inner_join(cgs, mothers)

        bad_confs = set()
        for cgm in cgms:
            if (self.summary_price(cgm) > self.budget or
                    cgm[0].socket != cgm[2].socket):
                bad_confs.add(cgm)
        cgms = set(cgms).difference(bad_confs)

        cgmrs = self.inner_join(cgms, rams)

        print(len(cgmrs))
        bad_confs = set()
        for cgmr in cgmrs:
            if (cgmr[2].supported_memory_form_factor != 'DIMM' or  # configure only desktops
                    cgmr[3].memory_form_factor != 'DIMM' or  # configure only desktops
                    cgmr[2].supported_memory_type != cgmr[3].memory_type or
                    (cgmr[3].number_of_modules_included) > (
                            cgmr[2].number_of_memory_slots) or
                    (cgmr[2].maximum_memory_frequency) < (cgmr[3].clock_frequency) or
                    (cgmr[2].minimum_memory_frequency) > (cgmr[3].clock_frequency) or
                    (cgmr[0].maximum_frequency_of_ram) < (cgmr[3].clock_frequency) or
                    (cgmr[0].minimum_frequency_of_ram) > (cgmr[3].clock_frequency) or
                    self.summary_price(cgmr) > self.budget
            ):
                bad_confs.add(cgmr)
        print(len(cgmrs))
        cgmrs = set(cgmrs).difference(bad_confs)
        print(len(cgmrs))
        # end ram compotib

        cgmrcs = [tuple(list(conf) + [component]) for conf in cgmrs for component in coolers]
        bad_confs = set()
        for cgmrc in cgmrcs:
            if ((cgmrc[0].heat_dissipation_tdp) > (cgmrc[4].power_dissipation) or
                    cgmrc[0].socket in cgmrc[4].socket.split(', ') or
                    self.summary_price(cgmrc) > self.budget
            ):
                bad_confs.add(cgmrc)
        cgmrcs = set(cgmrcs).difference(bad_confs)
        print(len(cgmrcs))

        cgmrchs = [tuple(list(conf) + [component]) for conf in cgmrcs for component in hards]
        bad_confs = set()
        for cgmrch in cgmrchs:
            if self.summary_price(cgmrch) > self.budget:
                bad_confs.add(cgmrch)
        cgmrchs = set(cgmrchs).difference(bad_confs)
        print(len(cgmrchs))

        cgmrchps = [tuple(list(conf) + [component]) for conf in cgmrchs for component in powersupplies]
        print(len(cgmrchps))
        bad_confs = set()
        for cgmrchp in cgmrchps:
            if (self.summary_price(cgmrchp) > self.budget or
                    self.convert_to_int(cgmrchp[6].power_nominal) <= self.convert_to_int(
                        cgmrchp[0].heat_dissipation_tdp) +
                    self.convert_to_int(cgmrchp[1].maximum_power_consumption) + 5 + 20 + 9 + 6 + 3):
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
