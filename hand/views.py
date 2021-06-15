from django.shortcuts import render
from configure.models import *


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


def catalog_cpu(request):
    # , context=data
    cpus = CPU.objects.all()
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
                CPU.objects.values_list('socket', flat=True).distinct()
            ],
            [
                'Интегрированное графическое ядро',
                'integrated_graphics_core_cpu[]',
                'processor_integrated_graphics_core',
                CPU.objects.values_list('integrated_graphics_core', flat=True).distinct()
            ],
            [
                'Многопоточность',
                'multithreaded_cpu[]',
                'processor_multithreaded',
                CPU.objects.values_list('multithreading', flat=True).distinct()
            ],
            [
                'Год релиза',
                'year_cpu[]',
                'processor_year',
                CPU.objects.values_list('release_year', flat=True).distinct()
            ],
            [
                'Тип памяти',
                'memory_type_cpu[]',
                'processor_memory_type',
                CPU.objects.values_list('memory_type', flat=True).distinct()
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
                CPU.objects.values_list('technical_process', flat=True).distinct()
            ],
            # [
            #     'Год релиза',
            #     'year_cpu[]',
            #     CPU.objects.values_list('release_year', flat=True).distinct()
            # ],
        ],
        'cpus': cpus,
    }
    response = render(request, template_name='configure/catalog.html', context=data)
    return response
