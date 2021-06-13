from django.http import HttpResponse
from django.shortcuts import render


def configuration_view(request, cpu, gpu, mother, ram, cooler, ssd ,hdd, ps):
    from configure import models
    config = {}
    r = range(8)
    config['Cpu'] = models.CPU.objects.filter(id=cpu)[0]
    config['Gpu'] = models.GPU.objects.filter(id=gpu)[0]
    config['Motherboard'] = models.motherboard.objects.filter(id=mother)[0]
    config['Ram'] = models.RAM.objects.filter(id=ram)[0]
    config['Cooler'] = models.cooler.objects.filter(id=cooler)[0]
    config['Hard35'] = models.hard35.objects.filter(id=hdd)[0]
    config['Ssd'] = models.SSD.objects.filter(id=ssd)[0]
    config['PowerSupply'] = models.powersupply.objects.filter(id=ps)[0]
    pics = []
    ans = []
    sum_price = 0
    for key, comp, i in zip(config.keys(), config.values(), range(8)):
        pics.append(comp.picture)
        sum_price += comp.price
        ans.append( \
            f''' <div class="itm" id='{i}'>
                                    <div class="itmname">
                                        <h6 class="card-title" style="margin: 10px"><a href="/configuration/{key}/{comp.id}"
                                                                                       style="color: #17a2b8">
                                            {comp.name}</a></h6>
                                    </div>
                                    <div class="itmprice" style="margin-left: auto;">
                                        <h6 class="card-title" style="margin: 10px; color: aliceblue">{comp.price}'Р'</h6>
                                    </div>
                                </div>''')

    data = {
        'hm': ans,
        'rows': config,
        'nums': r,
        'pics': pics,
        'sum_price': sum_price,
    }
    return render(request, 'configure/config.html', context=data)

def component(request, component_name, component_id):
    from configure import models
    if component_name == 'Cpu':
        component = models.CPU.objects.get(pk=component_id)
    elif component_name == 'Gpu':
        component = models.GPU.objects.get(pk=component_id)
    elif component_name == 'Motherboard':
        component = models.motherboard.objects.get(pk=component_id)
    elif component_name == 'Cooler':
        component = models.cooler.objects.get(pk=component_id)
    elif component_name == 'Ram':
        component = models.RAM.objects.get(pk=component_id)
    elif component_name == 'Hard35':
        component = models.hard35.objects.get(pk=component_id)
    elif component_name == 'Ssd':
        component = models.SSD.objects.get(pk=component_id)
    elif component_name == 'PowerSupply':
        component = models.powersupply.objects.get(pk=component_id)
    else:
        return HttpResponse('404')
    data = {'component_name': component.name.split('[')[0],
            'component_price': component.price,
            'component_photo': component.picture,
            'component_id': component_id,
            'component_type': component_name,
            }

    return render(request, template_name='configure/component.html', context=data)
