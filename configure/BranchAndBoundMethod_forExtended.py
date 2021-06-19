import sys
from datetime import time

from django.db.models import F

from configure.Configuration import *
from webconf.settings import DEBUG
from multiprocessing import Process, Lock, cpu_count, Value, Array
from configure.BranchAndBoundMethod import BranchAndBoundMethod


def intersect_components(components_hand, component_lists):
    res = {}
    for k in component_lists:
        res[k] = []
        for i in component_lists[k]:
            for j in components_hand[k]:
                if j[0] == i.id:
                    res[k].append(i)
    return res


class BranchAndBoundMethodEx(BranchAndBoundMethod):
    def __init__(self, budget: int, component_priorities: dict, hdd_ssd_ssdhdd=2, is_benchmark_find=1, request=None):
        """:param: hdd_ssd_ssdhdd  hdd_mode - 0, ssd - 1, hdd and ssd - 2
        :param is_benchmark_find: 0 - use price of component, 1 - use benchmark"""
        self.budget = budget
        self.component_priorities = component_priorities
        self.hdd_ssd_ssdhdd = hdd_ssd_ssdhdd
        self.budget_constraints = self._get_budget_constraints()
        if is_benchmark_find == 0:
            self.maximize_component = ['-price', '-price']
        else:
            self.maximize_component = ['-benchmark_mark', '-g3d_mark']
        self.is_benchmark_find = is_benchmark_find
        self.set_types()
        self.lower_estimate = 0
        self.request = request

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

        gpus = models.GPU.objects.filter(price__lte=budget_constraints['GPU'],
                                         maximum_power_consumption__isnull=False).order_by(self.maximize_component[1])
        # maximized attribute selected in Configuration.Cpu.__init__
        cpus = models.CPU.objects.filter(price__lte=budget_constraints['CPU'], socket__isnull=False,
                                         maximum_frequency_of_ram__isnull=False,
                                         minimum_frequency_of_ram__isnull=False,
                                         heat_dissipation_tdp__isnull=False, ).order_by(self.maximize_component[0])
        if self.is_benchmark_find == 0:
            cpus = [Cpu(cpu, self.component_priorities['CPU'], cpu.price) for cpu in cpus]  # create list of not Model cpu objects
            gpus = [Gpu(gpu, self.component_priorities['GPU'], gpu.price) for gpu in gpus]  # create list of not Model gpu objects
        else:
            cpus = models.CPU.objects.filter(benchmark_mark__isnull=False).order_by(self.maximize_component[0])
            gpus = models.GPU.objects.filter(g3d_mark__isnull=False).order_by(self.maximize_component[1])
            cpus = [Cpu(cpu, self.component_priorities['CPU'], cpu.benchmark_mark) for cpu in cpus]  # create list of not Model cpu objects
            gpus = [Gpu(gpu, self.component_priorities['GPU'], gpu.g3d_mark) for gpu in gpus]  # create list of not Model gpu objects
        # maximized attribute selected in Configuration.Gpu.__init__


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

        request_dict = {
            'socket_cpu[]': 'socket',
            'count_cores_cpu[]': 'number_of_cores',
            'memory_type_cpus[]': 'memory_type',
        }
        request_dict = {
            'Cpu': {
                'socket_cpu[]': 'socket',
                'count_cores_cpu[]': 'number_of_cores',
                'memory_type_cpus[]': 'memory_type',
            },
            'Motherboard': {
                'chipset_mb[]': 'chipset',
                'form-factor-mb[]': 'form_factor',
                'memory-slots-mb[]': 'number_of_memory_slots',
                'memory-type-mb[]': 'supported_memory_type',
                'haswifi-mb[]': 'built_in_wi_fi_adapter',
                'm2-slots-mb[]': 'number_of_m_2_slots',
            },
            'Gpu': {
                'video-memory-gpu[]': 'video_memory_size',
                'memory-type-gpu[]': 'memory_type',
                'pci-version-gpu[]': 'pci_express_version',
            },
            'PowerSupply': {
                'form-factor-ps[]': 'form_factor',
            },
            'Ram': {
                'memory-type-ram[]': 'memory_type',
                'color-ram[]': 'illumination_of_board_elements',
            },
            'Cooler': {
                'fan-connector-cl[]': 'fan_connector',
                'rotation-speed-control-cl[]': 'rotation_speed_control',
                'fan-backlight-type-cl[]': 'fan_backlight_type',
                'fan-illumination-color-cl[]': 'fan_illumination_color',
            },
            'Ssd': {},
            'Hard35': {},
        }
        from pymysql import connect, cursors
        try:
            connection = connect(
                host='127.0.0.1',
                user='django',
                password='qwerty',
                db='config',
                charset='utf8mb4',
                cursorclass=cursors.Cursor)
        except RuntimeError:
            print('Ошибка. Не удалось подключится к базе данных')
        with connection:
            cur = connection.cursor()  # , benchmark_mark, thread_mark
            components_hands = {}
            for component_name, conditions in request_dict.items():
                and_conditions = []
                if component_name == 'Cpu':
                    mfs = [f'name like "%{mf}%"' for mf in self.request.GET.getlist('manufacturer_cpu[]')]
                    and_conditions.append('(' + ' or '.join(mfs) + ')')
                if component_name == 'PowerSupply':
                    power_nominal_type = self.request.GET['power-ps']
                    if power_nominal_type == '1':
                        and_conditions.append('(power_nominal < 500)')
                    elif power_nominal_type == '2':
                        and_conditions.append('(power_nominal >= 500 and power_nominal < 1000)')
                    else:
                        and_conditions.append('(power_nominal >= 1000)')
                if component_name == 'Ram':
                    frequency_type = self.request.GET['frequency-ram']
                    if frequency_type == '1':
                        and_conditions.append('(clock_frequency < 1000)')
                    elif frequency_type == '2':
                        and_conditions.append('(clock_frequency >= 1000 and clock_frequency < 2000)')
                    elif frequency_type == '3':
                        and_conditions.append('(clock_frequency >= 2000 and clock_frequency < 3000)')
                    elif frequency_type == '4':
                        and_conditions.append('(clock_frequency >= 3000 and clock_frequency < 4000)')
                    else:
                        and_conditions.append('(clock_frequency >= 4000)')
                for c1, c2 in conditions.items():
                    condition1 = self.request.GET.getlist(c1)
                    or_conditions = [f'{c2}="{ccc}"' for ccc in condition1]
                    and_conditions.append('('+' or '.join(or_conditions)+')')
                while '()' in and_conditions:
                    and_conditions.remove('()')
                if len(and_conditions) != 0:
                    condition = 'where ' + ' and '.join(and_conditions)
                else:
                    condition = ''
                cur.execute(f"SELECT id FROM configure_{component_name.lower()} {condition}")
                components_hand = cur.fetchall()

                components_hands[component_name] = components_hand
            component_lists = intersect_components(components_hands, component_lists)


        return component_lists

