from django.shortcuts import render


def configuration(request):
    if request.method == 'POST':
        pass
    is_cpu = False
    if "cpu_id" in request.COOKIES:
        is_cpu = True
        x = request.COOKIES["cpu_id"]

    data = {
        'is_cpu': is_cpu,
        'is_gpu': True
    }
    return render(request, template_name='configure/handled.html', context=data)
    # die monkey

