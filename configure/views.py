from django.http import HttpResponse
from django.shortcuts import render

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


def priority_calc(type: int, budget: int):
    return {
        "1": lambda x, y: {
            'CPU': 0.25,
            'GPU': 0.2,
            'motherboard': 0.1,
            'RAM': 0.1,
            'cooler': 0.05,
            'hard_35': 0.1,
            'ssd': 0.1,
            'powersupply': 0.1
        },
        '2': lambda x, y: {
            'CPU': 4.69532 * pow(10, -12) * y * y - 1.53484 * pow(10, -6) * y + 0.285049,
            'GPU': 1.87181 * pow(10, -16) * pow(y, 3) - 8.86215 * pow(10, -11) * y * y + 0.000012088 * y + 0.0458876,
            'motherboard': 2.39955 * pow(10, -12) * y * y - 8.70106 * pow(10, -7) * y + 0.153233,
            'RAM': -3.09443 * pow(10, -12) * y * y + 1.04014 * pow(10, -6) * y + 0.00444359,
            'cooler': -1.28803 * pow(10, -13) * y * y + 1.27392 * pow(10, -7) * y + 0.010703,
            'hard_35': 1.72394 * pow(10, -12) * y * y - 4.76713 * pow(10, -7) * y + 0.0915476,
            'ssd': 1.72394 * pow(10, -12) * y * y - 4.76713 * pow(10, -7) * y + 0.0915476,
            'powersupply': 1.15148 * pow(10, -12) - 2.98272 * pow(10, -7) * y + 0.0642154,
        },
        '3': lambda x, y: {
            'CPU': 0.45,
            'GPU': 0.15,
            'motherboard': 0.07,
            'RAM': 0.15,
            'cooler': 0.03,
            'hard_35': 0.05,
            'ssd': 0.05,
            'powersupply': 0.05,
        },
    }.get(type, -1)
    # TODO write priorities functions


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

def autopage(request):
    stroka = ''
    pri = int(request.POST['price'])
    tip = request.POST['answer']
    config = list(real_auto_configure(pri, tip))
    r = range(8)
    pics = []
    ans = []
    sum_price = 0
    for i in range(8):
        pics.append(config[i].picture)
        sum_price += config[i].price
        ans .append( \
    f''' <div class="itm" id='{ i }'>
                                    <div class="itmname">
                                        <h6 class="card-title" style="margin: 10px"><a href="/{ config[i].id }"
                                                                                       style="color: #17a2b8">
                                            { config[i].name }</a></h6>
                                    </div>
                                    <div class="itmprice">
                                        <h6 class="card-title" style="margin: 10px; color: aliceblue">{ config[i].price}'Р'</h6>
                                    </div>
                                </div>''')

    data = {
        'hm': ans,
        'rows': config,
        'nums': r,
        'pics': pics,
        'sum_price':sum_price,
    }
    return render(request, 'configure/config.html', context=data)


def real_auto_configure(budget: int, configure_type: int, hdd_ssd=2, is_banchmarck_mode=0):
    prioriti_calculator = prioriti_calculators[configure_type]
    priorities = prioriti_calculator(budget)
    from configure.StrictConstraintMethod import StrictConstraintMethod
    hdd_ssd = 2
    finder = StrictConstraintMethod(budget, priorities, hdd_ssd)

    return finder.find()


def half_auto_configure(budget: int, priorities, hdd_ssd=2, is_banchmarck_mode=0):
    from configure.BranchAndBoundMethod import BranchAndBoundMethod
    budget = 70000
    hdd_ssd = 2
    finder = BranchAndBoundMethod(budget, priorities, hdd_ssd)
    data = {
        'configuration': finder.find()
    }
    return render('configure.config', context=data)

