from django.db import models

class CPU(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField()
    price = models.IntegerField()
    socket = models.CharField(max_length=100, null=True)
    benchmark_mark = models.IntegerField()
    picture = models.URLField(null=True)
    guarantee = models.CharField(max_length=100, null=True)
    producing_country = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=70, null=True)
    generation_of_processors = models.CharField(max_length=70, null=True)
    manufacturer_code = models.CharField(max_length=50, null=True)
    release_year = models.IntegerField(null=True)
    cooling_system_included = models.CharField(max_length=100, null=True)
    thermal_interface_included = models.CharField(max_length=100, null=True)
    core = models.CharField(max_length=70, null=True)
    technical_process = models.CharField(max_length=100, null=True)
    number_of_cores = models.IntegerField(null=True)
    maximum_number_of_threads = models.CharField(max_length=50, null=True)
    l1_cache_instructions = models.CharField(max_length=100, null=True)
    l1_cache_data = models.CharField(max_length=100, null=True)
    l2_cache_size = models.CharField(max_length=100, null=True)
    l3_cache_size = models.CharField(max_length=100, null=True)
    cpu_base_frequency = models.CharField(max_length=10, null=True)
    maximum_frequency_in_turbo_mode = models.CharField(max_length=10, null=True)
    factor = models.IntegerField(null=True)
    free_multiplier = models.CharField(max_length=100, null=True)
    memory_type = models.CharField(max_length=10, null=True)
    maximum_supported_memory = models.CharField(max_length=100, null=True)
    number_of_channels = models.IntegerField(null=True)
    minimum_frequency_of_ram = models.CharField(max_length=100, null=True)
    maximum_frequency_of_ram = models.CharField(max_length=100, null=True)
    ecc_mode_support = models.CharField(max_length=14, null=True)
    heat_dissipation_tdp = models.CharField(max_length=100, null=True)
    configurable_tdp_ctdp = models.CharField(max_length=100, null=True)
    maximum_cpu_temperature = models.CharField(max_length=100, null=True)
    integrated_graphics_core = models.CharField(max_length=100, null=True)
    gpu_model = models.CharField(max_length=30, null=True)
    maximum_graphics_core_frequency = models.CharField(max_length=100, null=True)
    executive_blocks = models.IntegerField(null=True)
    stream_processors_shading_units = models.IntegerField(null=True)
    system_bus = models.CharField(max_length=10, null=True)
    bus_bandwidth = models.CharField(max_length=100, null=True)
    integrated_pci_express_controller = models.CharField(max_length=100, null=True)
    pci_express_lines = models.CharField(max_length=100, null=True)
    support_64_bit_instruction_set = models.CharField(max_length=100, null=True)
    multithreading = models.CharField(max_length=100, null=True)
    virtualization_technology = models.CharField(max_length=100, null=True)
    cpu_overclocking_technology = models.CharField(max_length=100, null=True)
    energy_saving_technology = models.CharField(max_length=100, null=True)
    a_set_of_instructions_and_commands = models.CharField(max_length=200, null=True)
    features_optional = models.CharField(max_length=100, null=True)


class motherboard(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField()
    price = models.IntegerField()
    socket = models.CharField(max_length=50, null=True)
    release_year = models.IntegerField(null=True)
    picture = models.URLField(null=True)
    guarantee = models.CharField(max_length=30, null=True)
    producing_country = models.CharField(max_length=70, null=True)
    model = models.CharField(max_length=30, null=True)
    form_factor = models.CharField(max_length=50, null=True)
    height = models.CharField(max_length=50, null=True)
    width = models.CharField(max_length=50, null=True)
    integrated_central_processing_unit = models.CharField(max_length=50, null=True)
    embedded_processor_model = models.CharField(max_length=50, null=True)
    chipset = models.CharField(max_length=50, null=True)
    bios = models.CharField(max_length=50, null=True)
    uefi_bios = models.CharField(max_length=50, null=True)
    sli_crossfire_support = models.CharField(max_length=50, null=True)
    supported_memory_form_factor = models.CharField(max_length=50, null=True)
    supported_memory_type = models.CharField(max_length=50, null=True)
    ecc_mode_support = models.CharField(max_length=50, null=True)
    number_of_memory_slots = models.CharField(max_length=50, null=True)
    minimum_memory_frequency = models.CharField(max_length=50, null=True)
    maximum_memory_frequency = models.CharField(max_length=50, null=True)
    number_of_memory_channels = models.CharField(max_length=50, null=True)
    maximum_memory = models.CharField(max_length=50, null=True)
    type_and_number_of_sata_ports = models.CharField(max_length=50, null=True)
    sata_express_ports_quantity = models.CharField(max_length=50, null=True)
    number_of_m_2_slots = models.CharField(max_length=50, null=True)
    nvme_support = models.CharField(max_length=50, null=True)
    sata_raid_operation_mode = models.CharField(max_length=50, null=True)
    msata_connector = models.CharField(max_length=50, null=True)
    ide_controller = models.CharField(max_length=50, null=True)
    number_of_pci_e_x16_slots = models.CharField(max_length=50, null=True)
    number_of_pci_e_x8_slots = models.CharField(max_length=50, null=True)
    number_of_pci_e_x4_slots = models.CharField(max_length=50, null=True)
    number_of_pci_e_x1_slots = models.CharField(max_length=50, null=True)
    modes_of_operation_of_several_pci_e_x16_slots = models.CharField(max_length=50, null=True)
    pci_express_version = models.CharField(max_length=50, null=True)
    number_of_pci_slots = models.CharField(max_length=50, null=True)
    internal_usb_connectors_on_board = models.CharField(max_length=50, null=True)
    number_and_type_of_usb_on_the_rear_panel = models.CharField(max_length=50, null=True)
    video_outputs = models.CharField(max_length=50, null=True)
    number_of_analog_audio_connectors = models.CharField(max_length=50, null=True)
    digital_audio_ports_s_pdif = models.CharField(max_length=50, null=True)
    ps_2_ports = models.CharField(max_length=50, null=True)
    other_connectors_on_the_rear_panel = models.CharField(max_length=50, null=True)
    number_of_network_ports_rj_45 = models.CharField(max_length=50, null=True)
    sound = models.CharField(max_length=50, null=True)
    sound_scheme = models.CharField(max_length=50, null=True)
    sound_adapter_chipset = models.CharField(max_length=50, null=True)
    network_adapter_chipset = models.CharField(max_length=50, null=True)
    network_adapter_speed = models.CharField(max_length=50, null=True)
    built_in_wi_fi_adapter = models.CharField(max_length=50, null=True)
    bluetooth = models.CharField(max_length=50, null=True)
    cpu_cooler_power_connector = models.CharField(max_length=50, null=True)
    four_pin_connectors_for_system_fans = models.CharField(max_length=50, null=True)
    three_pin_connectors_for_system_fans = models.CharField(max_length=50, null=True)
    main_power_connector = models.CharField(max_length=50, null=True)
    processor_power_connector = models.CharField(max_length=50, null=True)
    number_of_supply_phases = models.CharField(max_length=50, null=True)
    illumination_of_board_elements = models.CharField(max_length=50, null=True)
    three_pin_led_connector_5v_d_g = models.CharField(max_length=50, null=True)
    four_pin_led_connector_12v_g_r_b = models.CharField(max_length=50, null=True)
    lpt_interface = models.CharField(max_length=50, null=True)
    equipment = models.CharField(max_length=300, null=True)
    application_for_interacting_with_a_smartphone = models.CharField(max_length=50, null=True)
    features_optional = models.CharField(max_length=100, null=True)
    m_2_form_factor = models.CharField(max_length=50, null=True)
    m_2_storage_logical_interface = models.CharField(max_length=50, null=True)
    m_2_key_e = models.CharField(max_length=50, null=True)


class GPU(models.Model):
    name = models.CharField(max_length=300)
    link = models.URLField()
    price = models.IntegerField()
    picture = models.URLField(null=True)
    benchmark_mark = models.IntegerField()
    guarantee = models.CharField(max_length=30, null=True)
    producing_country = models.CharField(max_length=100, null=True)
    release_year = models.IntegerField(null=True)
    standards_and_technology_support = models.CharField(max_length=100, null=True)
    video_memory_size = models.CharField(max_length=100, null=True)
    memory_type = models.CharField(max_length=100, null=True)
    effective_memory_frequency = models.CharField(max_length=100, null=True)
    memory_bus_width = models.CharField(max_length=100, null=True)
    maximum_memory_bandwidth = models.CharField(max_length=100, null=True)
    microarchitecture = models.CharField(max_length=100, null=True)
    technical_process = models.CharField(max_length=100, null=True)
    nominal_frequency_of_the_video_chip = models.CharField(max_length=100, null=True)
    turbo_frequency = models.CharField(max_length=100, null=True)
    shader_alu = models.CharField(max_length=100, null=True)
    number_of_texture_units = models.CharField(max_length=100, null=True)
    number_of_rop_units = models.CharField(max_length=100, null=True)
    shader_version = models.CharField(max_length=100, null=True)
    maximum_processor_temperature_c = models.CharField(max_length=100, null=True)
    ray_tracing_support = models.CharField(max_length=100, null=True)
    video_connectors = models.CharField(max_length=100, null=True)
    maximum_resolution = models.CharField(max_length=100, null=True)
    number_of_simultaneously_connected_monitors = models.CharField(max_length=100, null=True)
    connection_interface = models.CharField(max_length=100, null=True)
    pci_express_version = models.CharField(max_length=100, null=True)
    support_for_multiprocessor_configuration = models.CharField(max_length=100, null=True)
    the_need_for_additional_food = models.CharField(max_length=100, null=True)
    auxiliary_power_connectors = models.CharField(max_length=100, null=True)
    maximum_power_consumption = models.CharField(max_length=100, null=True)
    recommended_power_supply = models.CharField(max_length=100, null=True)
    cooling_type = models.CharField(max_length=100, null=True)
    type_and_number_of_fans_installed = models.CharField(max_length=100, null=True)
    low_profile_card = models.CharField(max_length=100, null=True)
    number_of_occupied_expansion_slots = models.CharField(max_length=100, null=True)
    highlighting_the_elements_of_the_video_card = models.CharField(max_length=100, null=True)
    graphics_card_length = models.CharField(max_length=100, null=True)
    graphics_card_thickness = models.CharField(max_length=100, null=True)
    equipment = models.CharField(max_length=100, null=True)
    weight = models.CharField(max_length=100, null=True)
    features_optional = models.CharField(max_length=100, null=True)
    gpu_codename = models.CharField(max_length=100, null=True)
    peak_performance_of_chips_in_fp32 = models.CharField(max_length=100, null=True)
    rotation_speed_control = models.CharField(max_length=100, null=True)
    rgb_backlight_sync = models.CharField(max_length=100, null=True)
    lcd_display = models.CharField(max_length=100, null=True)
    bios_switch = models.CharField(max_length=100, null=True)


class RAM(models.Model):
    Гарантия: guarantee
    Страна - производитель: producing_country
    Модель: model
    Код
    производителя: manufacturer_code
    Год
    релиза: release_year
    Тип
    памяти: memory_type
    Форм - фактор
    памяти: memory_form_factor
    Регистровая
    память: register_memory
    ECC - память: ecc_memory
    Объем
    одного
    модуля
    памяти: the_volume_of_one_memory_module
    Количество
    модулей
    в
    комплекте: number_of_modules_included
    Тактовая
    частота: clock_frequency
    Пропускная
    способность: bandwidth
    Профили
    Intel
    XMP: intel_xmp_profiles
    Поддерживаемые
    режимы
    работы: supported_operating_modes
    CAS
    Latency(CL): cas_latency_cl
    RAS
    to
    CAS
    Delay(tRCD): ras_to_cas_delay_trcd
    Row
    Precharge
    Delay(tRP): row_precharge_delay_trp
    Наличие
    радиатора: the_presence_of_a_radiator
    Подсветка
    элементов
    платы: illumination_of_board_elements
    Высота: height
    Низкопрофильная(Low
    Profile): low_profile
    Напряжение
    питания: supply_voltage
    Название: name
    Ссылка: link
    Цена: price
    Изображение: picture
    Activate
    to
    Precharge
    Delay(tRAS): activate_to_precharge_delay_tras
    Ранговость: rank
    features_optional