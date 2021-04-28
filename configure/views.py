from django.http import HttpResponse
from django.shortcuts import render
from configure.models import *


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


# budget: int, priorities: list


def inner_join(configure_list: list, component_list):
    return [tuple(list(configure) + [component]) for configure in configure_list for component in component_list]


def find_configure(r):  # Ммм, хуита
    budget = 250000
    cpus = CPU.objects.filter(price__lt=budget)
    gpus = GPU.objects.filter(price__lt=budget)
    mothers = motherboard.objects.filter(price__lt=budget)
    rams = RAM.objects.filter(price__lt=budget)
    coolers = cooler.objects.filter(price__lt=budget)
    hards = hard35.objects.filter(price__lt=budget)
    # hards = hard25.objects.filter(price__lt=budget).union(hard35.objects.filter(price__lt=budget))
    ssds = SSD.objects.filter(price__lt=budget).union(ssd_m2.objects.filter(price__lt=budget))
    powersupplies = powersupply.objects.filter(price__lt=budget)

    cgs = [tuple([c]+ [g]) for c in cpus for g in gpus]
    print(len(cgs))

    bad_confs = set() #cpu and gpu
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

    # cgmrchs = [tuple(list(conf) + [component]) for conf in cgmrcs for component in hards]
    # bad_confs = set()
    # for cgmrch in cgmrchs:
    #     if summary_price(cgmrch) > budget:
    #         bad_confs.add(cgmrch)
    # cgmrchs = set(cgmrchs).difference(bad_confs)
    # print(len(cgmrchs))

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
