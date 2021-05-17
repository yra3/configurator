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
                                    <div class="itmprice" style="margin-left: auto;">
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
