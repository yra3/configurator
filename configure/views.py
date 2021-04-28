from django.http import HttpResponse
from django.shortcuts import render
from configure.models import *


def summary_price(configure:list):
    sum = 0
    for bit in configure:
        sum += bit.price
    return sum


def remove_over_budget(configurates:list, budget):
    for configure in configurates:
        if summary_price(configure) > budget:
            configurates.remove(configure)
# budget: int, priorities: list


def find_configure(r):  # Ммм, хуита
    budget = 10000
    cpus = CPU.objects.filter(price__lt=budget)
    gpus = GPU.objects.filter(price__lt=budget)
    mothers = motherboard.objects.filter(price__lt=budget)
    cgs = [[c, g] for c in cpus for g in gpus]
    print(len(cgs))

    remove_over_budget(cgs, budget)


    cgs.sort(key=lambda x: summary_price(x))
    cgpumother = [cg+[mother] for cg in cgs for mother in mothers]
    print(len(cgs))

    print(len(cgpumother))
    remove_over_budget(cgpumother, budget)
    print(len(cgpumother))
    for cgm in cgpumother:
        if cgm[0].socket != cgm[2].socket:
            cgpumother.remove(cgm)
    print(len(cgpumother))

    for cgm in cgpumother:
        if cgm[0].socket != cgm[2].socket:
            cgpumother.remove(cgm)

    return HttpResponse(cgs)



if __name__=='__main__':
    find_configure(10000)