from django.shortcuts import render
from .forms import Configuration


def index(request):
    return render(request, "configure/index.html")


def auto(request):
    return render(request, "configure/auto.html")


def preauto(request):
    from configure.models import CPU, motherboard, GPU, powersupply, RAM, cooler
    # socket_cpus = [cpu.socket for cpu in CPU.objects.all().distinct('socket')]
    socket_cpus = CPU.objects.values_list('socket', flat=True).distinct()
    x = socket_cpus[0]
    context = {
        'socket_cpus': CPU.objects.values_list('socket', flat=True).distinct(),
        'count_cores_cpus': CPU.objects.values_list('number_of_cores', flat=True).distinct(),
        'memory_type_cpus': CPU.objects.values_list('memory_type', flat=True).distinct(),
        'socket_mbs': motherboard.objects.values_list('socket', flat=True).distinct(),
        'chipset_mbs': motherboard.objects.values_list('chipset', flat=True).distinct(),
        'form_factor_mbs': motherboard.objects.values_list('form_factor', flat=True).distinct(),
        'memory_slot_mbs': motherboard.objects.values_list('number_of_memory_slots', flat=True).distinct(),
        'memory_type_mbs': motherboard.objects.values_list('supported_memory_type', flat=True).distinct(),
        'm2_slots_mbs': motherboard.objects.values_list('number_of_m_2_slots', flat=True).distinct(),
        'video_memory_gpus': GPU.objects.values_list('video_memory_size', flat=True).distinct(),
        'memory_type_gpus': GPU.objects.values_list('memory_type', flat=True).distinct(),
        'pci_version_gpus': GPU.objects.values_list('pci_express_version', flat=True).distinct(),
        'form_factor_pss': powersupply.objects.values_list('form_factor', flat=True).distinct(),
        'memory_type_ram': RAM.objects.values_list('memory_type', flat=True).distinct(),
        'fan_connector_cls': cooler.objects.values_list('fan_connector', flat=True).distinct(),
        'rotation_speed_control_cls': cooler.objects.values_list('rotation_speed_control', flat=True).distinct(),
        'fan_backlight_type_cl': cooler.objects.values_list('fan_backlight_type', flat=True).distinct(),
        'fan_illumination_color_cl': cooler.objects.values_list('fan_illumination_color', flat=True).distinct(),
    }

    return render(request, "configure/preauto.html", context=context)

# def config(request):
#     return render(request, "configure/config.html")


