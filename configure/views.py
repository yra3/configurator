from django.http import HttpResponse
from django.shortcuts import render, redirect

from configure.StrictConstraintMethod import StrictConstraintMethod
from configure.models import *


def convert_to_int(string_value):
    return int(string_value.split(' ')[0])


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


class RegressionConfigurePrioritiesCalculator:
    def __init__(self, budget: int, purpose_of_computer):
        self.budget = budget
        self.purpose_of_computer = purpose_of_computer

    def get_priorities(self):
        ctype = self.purpose_of_computer
        if ctype == '1' or ctype == 1 or ctype == 'home':
            return self.get_home_priorities()
        if ctype == '2' or ctype == 2 or ctype == 'game':
            return self.get_game_priorities()
        if ctype == '3' or ctype == 3 or ctype == 'work':
            return self.get_work_priorities()

    def get_home_priorities(self):
        x = self.budget
        xx = x ** 2
        xxx = x ** 3
        return {
            'CPU': 7.35334 * pow(10, -17) * xxx - 3.91966 * pow(10, -11) * xx + 5.77059 * pow(10, -6) * x + 0.038136,
            'GPU': -2.43693 * pow(10, -12) * xx + 1.42841 * pow(10, -6) * x + 0.208638,
            'motherboard': 5.05664 * pow(10, -12) * xx - 1.68784 * pow(10, -6) * x + 0.203876,
            'RAM': 4.93807 * pow(10, -12) * xx - 1.61084 * pow(10, -6) * x + 0.200755,
            'cooler': -4.17194 * pow(10, -12) * xx + 7.22912 * pow(10, -7) * x + 0.00768568,
            'hard_35': 2.40797 * pow(10, -12) * xx - 1.05115 * pow(10, -6) * x + 0.210022,
            'ssd': 2.40797 * pow(10, -12) * xx - 1.05115 * pow(10, -6) * x + 0.210022,
            'powersupply': 4.14385 * pow(10, -12) * xx - 1.43206 * pow(10, -6) * x + 0.150924
        }

    def get_game_priorities(self):
        x = self.budget
        xx = x ** 2
        xxx = x ** 3
        return {
            'CPU': 4.69532 * pow(10, -12) * xx - 1.53484 * pow(10, -6) * x + 0.285049,
            'GPU': 1.87181 * pow(10, -16) * xxx - 8.86215 * pow(10, -11) * xx + 0.000012088 * x + 0.0458876,
            'motherboard': 2.39955 * pow(10, -12) * xx - 8.70106 * pow(10, -7) * x + 0.153233,
            'RAM': -3.09443 * pow(10, -12) * xx + 1.04014 * pow(10, -6) * x + 0.00444359,
            'cooler': -1.28803 * pow(10, -13) * xx + 1.27392 * pow(10, -7) * x + 0.010703,
            'hard_35': 1.72394 * pow(10, -12) * xx - 4.76713 * pow(10, -7) * x + 0.0915476,
            'ssd': 1.72394 * pow(10, -12) * xx - 4.76713 * pow(10, -7) * x + 0.0915476,
            'powersupply': 1.15148 * pow(10, -12) - 2.98272 * pow(10, -7) * x + 0.0642154,
        }

    def get_work_priorities(self):
        x = self.budget
        xx = x ** 2
        xxx = x ** 3
        return {
            'CPU': -7.72411 * pow(10, -12) * xx + 1.48088 * pow(10, -6) * x + 0.325251,
            'GPU': 1.75387 * pow(10, -12) * xx + 1.04826 * pow(10, -6) * x + 0.0104763,
            'motherboard': 2.47102 * pow(10, -12) * xx - 1.1073 * pow(10, -6) * x + 0.230359,
            'RAM': 5.35811 * pow(10, -17) * xxx - 2.20686 * pow(10, -11) * xx + 2.28215 * pow(10, -6) * x + 0.0747362,
            'cooler': -8.55621 * pow(10, -13) * xx + 2.36216 * pow(10, -7) * x + 0.0235645,
            'hard_35': 7.81749 * pow(10, -12) * xx - 2.40609 * pow(10, -6) * x + 0.201275,
            'ssd': 7.81749 * pow(10, 12) * xx - 2.40609 * pow(10, -6) * x + 0.201275,
            'powersupply': 2.57604 * pow(10, -12) * xx - 9.86143 * pow(10, -7) * x + 0.138944,
        }


prioriti_calculators = {
    '1': lambda x: {
        'CPU': 0.25,
        'GPU': 0.2,
        'motherboard': 0.1,
        'RAM': 0.1,
        'cooler': 0.05,
        'hard_35': 0.1,
        'ssd': 0.1,
        'powersupply': 0.1
    },
    '2': lambda x: {
        'CPU': 0.25,
        'GPU': 0.40,
        'motherboard': 0.07,
        'RAM': 0.1,
        'cooler': 0.03,
        'hard_35': 0.05,
        'ssd': 0.05,
        'powersupply': 0.05,
    },
    '3': lambda x: {
        'CPU': 0.45,
        'GPU': 0.15,
        'motherboard': 0.07,
        'RAM': 0.15,
        'cooler': 0.03,
        'hard_35': 0.05,
        'ssd': 0.05,
        'powersupply': 0.05,
    },
}


def simple_configure(request):
    import time
    tm = time.time()
    time.sleep(0.1)
    m2 = time.time()
    stroka = ''
    pri = int(request.POST['price'])
    tip = request.POST['answer']
    config = real_auto_configure(pri, tip)
    s = '/configuration/'
    for com in config.values() :
        s += str(com.id)+'/'
    return redirect(s)
    # r = range(8)
    # pics = []
    # ans = []
    # sum_price = 0
    # for key, comp, i in zip(config.keys(), config.values(), range(8)):
    #     pics.append(comp.picture)
    #     sum_price += comp.price
    #     ans .append( \
    # f''' <div class="itm" id='{ i }'>
    #                                 <div class="itmname">
    #                                     <h6 class="card-title" style="margin: 10px"><a href="{ key }/{ comp.id }"
    #                                                                                    style="color: #17a2b8">
    #                                         { comp.name }</a></h6>
    #                                 </div>
    #                                 <div class="itmprice" style="margin-left: auto;">
    #                                     <h6 class="card-title" style="margin: 10px; color: aliceblue">{ comp.price}'Р'</h6>
    #                                 </div>
    #                             </div>''')
    #
    # data = {
    #     'hm': ans,
    #     'rows': config,
    #     'nums': r,
    #     'pics': pics,
    #     'sum_price':sum_price,
    # }
    # return render(request, 'configure/config.html', context=data)

def sborka(request, cpu, gpu, mother, ram, cooler, ssd ,hdd, ps):
    from configure import models
    config = {}
    r = range(8)
    config['Cpu'] = models.CPU.objects.filter(id=cpu)[0]
    config['Gpu'] = models.GPU.objects.filter(id=gpu)[0]
    config['Motherboard'] = models.motherboard.objects.filter(id=mother)[0]
    config['Ram'] = models.RAM.objects.filter(id=ram)[0]
    config['Cooler'] = models.cooler.objects.filter(id=cooler)[0]
    config['Hard35'] = models.hard35.objects.filter(id=ssd)[0]
    config['Ssd'] = models.SSD.objects.filter(id=hdd)[0]
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


def real_auto_configure(budget: int, configure_type: int, hdd_ssd=2, is_banchmarck_mode=0):
    prioriti_calculator = RegressionConfigurePrioritiesCalculator(budget, configure_type)
    priorities = prioriti_calculator.get_priorities()
    from configure.BranchAndBoundMethod import BranchAndBoundMethod
    hdd_ssd = 2
    finder = BranchAndBoundMethod(budget, priorities, hdd_ssd)
    return finder.find()


def extended_configure(budget: int, priorities, hdd_ssd=2, is_banchmarck_mode=0):
    from configure.BranchAndBoundMethod import BranchAndBoundMethod
    budget = 70000
    hdd_ssd = 2
    finder = BranchAndBoundMethod(budget, priorities, hdd_ssd)
    data = {
        'configuration': finder.find()
    }
    return render(template_name='configure.config', context=data)


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
            }

    return render(request, template_name='configure/component.html', context=data)

