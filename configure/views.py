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
        'motherboard': 0.7,
        'RAM': 0.1,
        'cooler': 0.03,
        'hard_35': 0.05,
        'ssd': 0.05,
        'powersupply': 0.05,
    },
    '3': lambda x: {
        'CPU': 0.45,
        'GPU': 0.15,
        'motherboard': 0.7,
        'RAM': 0.15,
        'cooler': 0.03,
        'hard_35': 0.05,
        'ssd': 0.05,
        'powersupply': 0.05,
    },
}

def autopage(request):
    stroka = ''
    for component, id in zip(real_auto_configure(request.price, request.answer), range(8)):
        stroka += f'''
        <div class="itm" id='{ id }'>
            <div class="itmname">
                <h6 class="card-title" style="margin: 10px"><a href="/{ component.id }" style="color: #17a2b8">{ component.name }</a></h6>
            </div>
            <div class="itmprice">
                <h6 class="card-title" style="margin: 10px; color: aliceblue">{ component.price }'Р'</h6>
            </div>
        </div>
        '''
    data = {
        'rows': stroka,
    }
    return render('configure.configure', context=data)

def real_auto_configure(budget: int, configure_type: int, hdd_ssd=2, is_banchmarck_mode=0):
    configure_type = 'working'
    prioriti_calculator = prioriti_calculators[configure_type]
    priorities = prioriti_calculator(budget)
    from configure.BranchAndBoundMethod import BranchAndBoundMethod
    budget = 70000
    hdd_ssd = 2
    finder = BranchAndBoundMethod(budget, priorities, hdd_ssd)

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

