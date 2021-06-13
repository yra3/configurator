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
