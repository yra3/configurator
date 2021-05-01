from django.http import HttpResponse
from django.shortcuts import render
from configure.models import *

maximize_component = ['price', 'price', 'count_of_memory']


def convert_to_int(string_value):
    return int(string_value.split(' ')[0])


def summary_price(configure: list):
    sum = 0
    for bit in configure:
        sum += bit.price
    return sum


def remove_over_budget(configurates: list, budget):
    for configure in configurates:
        if summary_price(configure) > budget:
            configurates.remove(configure)


def inner_join(configure_list: list, component_list):
    return [tuple(list(configure) + [component]) for configure in configure_list for component in component_list]


budget_constraints = {
    'CPU': 0.310000,
    'GPU': 0.51000,
    'motherboard': 0.41203,
    'RAM': 0.23476,
    'cooler': 0.23,
    'hard_35': 0.234,
    'ssd': 0.234,
    'powersupply': 0.3,
}


class ObjectiveFunctionInterface:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def calculate(self, parameters):
        '''Get list or dict of parameters
        returns integer value'''
        pass


class ObjectiveFunctionUseDict(ObjectiveFunctionInterface):
    def __init__(self, coefficients: dict):
        '''Parameter coefficients must be
        dict{component_name: importance_coefficient}'''
        super().__init__(coefficients)

    def calculate(self, parameters):
        '''Get dict{component_name: value} of configuration
        parameters, returns integer value'''
        answer = 0
        for name, value in parameters.items():
            answer += self.coefficients[name] * value
        return answer


def _get_budget_constraints(budget: int, component_priorities: dict):
    budget_constraints = dict()
    for component_name, cost in dict.items():
        budget_constraints[component_name] = cost * budget
    return budget_constraints


def first_lower_estimate(budget: int, component_priorities: dict):
    budget_constraints = _get_budget_constraints(budget, component_priorities)

    objective_func = ObjectiveFunctionUseDict(component_priorities)

    cpus = CPU.objects.filter(price__lt=budget_constraints['CPU']).order_by(maximize_component[0])  # 'price'
    for cpu in cpus:
        # TODO add using difference between component cost and component max cost

        # For configure only desktops supported_memory_form_factor='DIMM'
        # TODO add filter motherboard.ram_min_frequency < cpu.ram_max_frequency
        mother = motherboard.objects.filter(price__lt=budget_constraints['motherboard'],
                                            socket__iexact=cpu.socket,
                                            supported_memory_form_factor__iexact='DIMM'
                                            ).order_by(maximize_component[2]).first()

        gpu = GPU.objects.filter(price__lt=budget_constraints['GPU']).order_by(maximize_component[1]).first()  # 'price'

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
        hard1 = hard35.objects.filter(price__lt=budget_constraints['hard_35']).order_by('hdd_capacity').first()

        ssd1 = SSD.objects.filter(price__lt=budget_constraints['ssd']).order_by('drive_volume').first()

        # TODO uncomment next row, when change db attributes to integer
        # summary_tdp = cpu.heat_dissipation_tdp + gpu.maximum_power_consumption + 5 + 20 + 9 + 6 + 3
        powersupply1 = powersupply.objects.filter(price__lt=budget_constraints['powersupply'],
                                                  # TODO uncomment next row, when change db attributes to integer
                                                  # power_nominal__gt=summary_tdp,
                                                  ).order_by('power_nominal').first()

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
        return objective_func.calculate(configurate)


def auto_configure(budget, budget_constraints: dict, component_priorities):
    # TODO: write checking normalise var 'component_priorities'
    cpus = CPU.objects.filter(price__lt=budget_constraints['CPU'])
    gpus = GPU.objects.filter(price__lt=budget_constraints['GPU'])
    mothers = motherboard.objects.filter(price__lt=budget_constraints['motherboard'])
    rams = RAM.objects.filter(price__lt=budget_constraints['RAM'])
    coolers = cooler.objects.filter(price__lt=budget_constraints['cooler'])
    hards = hard35.objects.filter(price__lt=budget_constraints['hard_35'])
    ssds = SSD.objects.filter(price__lt=budget_constraints['ssd'])
    powersupplies = powersupply.objects.filter(price__lt=budget_constraints['powersupply'])


def find_configure(r):  # Ммм, хуита
    budget = 250000
    cpus = CPU.objects.filter(price__lt=budget)
    gpus = GPU.objects.filter(price__lt=budget)
    mothers = motherboard.objects.filter(price__lt=budget)
    rams = RAM.objects.filter(price__lt=budget)
    coolers = cooler.objects.filter(price__lt=budget)
    hards = hard35.objects.filter(price__lt=budget)
    ssds = SSD.objects.filter(price__lt=budget).union(ssd_m2.objects.filter(price__lt=budget))
    powersupplies = powersupply.objects.filter(price__lt=budget)

    cgs = [tuple([c] + [g]) for c in cpus for g in gpus]
    print(len(cgs))

    bad_confs = set()  # cpu and gpu
    for cg in cgs:
        if (summary_price(cg) > budget):
            bad_confs.add(cg)
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
                convert_to_int(cgmr[3].number_of_modules_included) > convert_to_int(cgmr[2].number_of_memory_slots) or
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

    return HttpResponse("23")


if __name__ == '__main__':
    find_configure(10000)
