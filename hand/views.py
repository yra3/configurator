from django.shortcuts import render
from configure.models import *

component_names_list = {
        'Cpu': CPU,
        'Gpu': GPU,
        'Motherboard': motherboard,
        'Cooler': cooler,
        'Ram': RAM,
        'Hard35': hard35,
        'Ssd': SSD,
        'PowerSupply': powersupply,
    }
def configuration(request):
    component_names_list = {
        'Cpu': CPU,
        'Gpu': GPU,
        'Motherboard': motherboard,
        'Cooler': cooler,
        'Ram': RAM,
        'Hard35': hard35,
        'Ssd': SSD,
        'PowerSupply': powersupply,
    }
    data = {}
    for name, model in component_names_list.items():
        if name.lower() in request.COOKIES:
            id = request.COOKIES[name.lower()]
            component = model.objects.get(pk=id)
            data[name] = component
            data['is_' + name.lower()] = True
        else:
            data['is_' + name.lower()] = False

    if request.method == 'POST':
        if request.POST["method"] == "add":
            id = request.POST.get('component_id')
            name = request.POST.get('component_type')
            data['is_' + name.lower()] = True
            data[name] = component_names_list[name].objects.get(pk=id)
            response = render(request, template_name='configure/handled.html', context=data)
            response.set_cookie(name.lower(), id)
            return response

        if request.POST['method'] == 'delete':
            name = request.POST['component_type']
            data['is_' + name.lower()] = False
            response = render(request, template_name='configure/handled.html', context=data)
            response.delete_cookie(name.lower())
            return response

    response = render(request, template_name='configure/handled.html', context=data)
    return response


request_dict = {
            'Cpu': {
                'socket_cpu[]': 'socket',
                'cores_cpu[]': 'number_of_cores',
                'memory_type_cpu[]': 'memory_type',
                'integrated_graphics_core_cpu[]': 'integrated_graphics_core',
                'multithreaded_cpu[]': 'multithreading',
                'year_cpu[]': 'release_year',
                'techprocess_cpu[]': 'technical_process',
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


def catalog_cpu(request, component_name):
    # , context=data
    cpus = component_names_list[component_name].objects.all()
    data = {
        'values_list': [
            [
                'Количество ядер',
                'cores_cpu[]',
                'processor_manufacturer',
                CPU.objects.values_list('number_of_cores', flat=True).distinct()
            ],
            [
                'Производитель процессора',
                'manufacturer_cpu[]',
                'processor_socket',
                ['AMD', 'Intel']
            ],
            [
                'Сокет',
                'socket_cpu[]',
                'processor_cores',
                CPU.objects.values_list('socket', flat=True).filter(socket__isnull=False).distinct()
            ],
            [
                'Интегрированное графическое ядро',
                'integrated_graphics_core_cpu[]',
                'processor_integrated_graphics_core',
                CPU.objects.values_list('integrated_graphics_core', flat=True).filter(integrated_graphics_core__isnull=False).distinct()
            ],
            [
                'Многопоточность',
                'multithreaded_cpu[]',
                'processor_multithreaded',
                CPU.objects.values_list('multithreading', flat=True).filter(multithreading__isnull=False).distinct()
            ],
            [
                'Год релиза',
                'year_cpu[]',
                'processor_year',
                CPU.objects.values_list('release_year', flat=True).filter(release_year__isnull=False).distinct()
            ],
            [
                'Тип памяти',
                'memory_type_cpu[]',
                'processor_memory_type',
                CPU.objects.values_list('memory_type', flat=True).filter(memory_type__isnull=False).distinct()
            ],
            [
                'Базовая частота процессора (МГц)',
                'frequency_cpu',
                'processor_base_freq',
                ['Все', 'Менее 3000', '3001-4000', '4001 и более']
            ],
            [
                'Техпроцесс',
                'techprocess_cpu[]',
                'processor_techprocess',
                CPU.objects.values_list('technical_process', flat=True).filter(technical_process__isnull=False).distinct()
            ],
        ],
        'cpus': cpus,
        'component_name': component_name,
    }



    conditions = request_dict[component_name]
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
        cur = connection.cursor()
        and_conditions = []
        if component_name == 'Cpu':
            mfs = [f'name like "%{mf}%"' for mf in request.GET.getlist('manufacturer_cpu[]')]
            and_conditions.append('(' + ' or '.join(mfs) + ')')
            frequency_type = request.GET.get('frequency_cpu')
            if frequency_type == '1':
                and_conditions.append('(cpu_base_frequency < 1000)')
            elif frequency_type == '2':
                and_conditions.append('(cpu_base_frequency >= 1000 and cpu_base_frequency < 2000)')
            elif frequency_type == '3':
                and_conditions.append('(cpu_base_frequency >= 2000 and cpu_base_frequency < 3000)')
            elif frequency_type == '4':
                and_conditions.append('(cpu_base_frequency >= 3000 and cpu_base_frequency < 4000)')
            else:
                and_conditions.append('(cpu_base_frequency >= 4000)')
        # if component_name == 'PowerSupply':
        #     power_nominal_type = request.GET['power-ps']
        #     if power_nominal_type == '1':
        #         and_conditions.append('(power_nominal < 500)')
        #     elif power_nominal_type == '2':
        #         and_conditions.append('(power_nominal >= 500 and power_nominal < 1000)')
        #     else:
        #         and_conditions.append('(power_nominal >= 1000)')
        # if component_name == 'Ram':
            # frequency_type = request.GET['frequency-ram']
            # if frequency_type == '1':
            #     and_conditions.append('(clock_frequency < 1000)')
            # elif frequency_type == '2':
            #     and_conditions.append('(clock_frequency >= 1000 and clock_frequency < 2000)')
            # elif frequency_type == '3':
            #     and_conditions.append('(clock_frequency >= 2000 and clock_frequency < 3000)')
            # elif frequency_type == '4':
            #     and_conditions.append('(clock_frequency >= 3000 and clock_frequency < 4000)')
            # else:
            #     and_conditions.append('(clock_frequency >= 4000)')
        for c1, c2 in conditions.items():
            condition1 = request.GET.getlist(c1)
            or_conditions = [f'{c2}="{ccc}"' for ccc in condition1]
            and_conditions.append('(' + ' or '.join(or_conditions) + ')')
        while '()' in and_conditions:
            and_conditions.remove('()')
        if len(and_conditions) != 0:
            condition = 'where ' + ' and '.join(and_conditions)
        else:
            return render(request, template_name='configure/catalog.html', context=data)
        cur.execute(f"SELECT id FROM configure_{component_name.lower()} {condition}")
        components_hand = cur.fetchall()
        components_hand = [component[0] for component in components_hand]
        components = component_names_list[component_name].objects.all().filter(pk__in=components_hand).order_by('price')


    data['cpus'] = components
    response = render(request, template_name='configure/catalog.html', context=data)
    return response
