# Generated by Django 3.2 on 2021-04-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0004_alter_gpu_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='cooler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('socket', models.CharField(max_length=200, null=True)),
                ('maximum_air_flow', models.CharField(max_length=200, null=True)),
                ('power_dissipation', models.CharField(max_length=200, null=True)),
                ('construction_type', models.CharField(max_length=200, null=True)),
                ('base_material', models.CharField(max_length=200, null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('radiator_material', models.CharField(max_length=200, null=True)),
                ('number_of_heat_pipes', models.CharField(max_length=200, null=True)),
                ('nickel_plated', models.CharField(max_length=200, null=True)),
                ('fan_connector', models.CharField(max_length=200, null=True)),
                ('number_of_fans_included', models.CharField(max_length=200, null=True)),
                ('maximum_number_of_installed_fans', models.CharField(max_length=200, null=True)),
                ('dimensions_of_complete_fans', models.CharField(max_length=200, null=True)),
                ('maximum_rotation_speed', models.CharField(max_length=200, null=True)),
                ('minimum_rotation_speed', models.CharField(max_length=200, null=True)),
                ('rotation_speed_control', models.CharField(max_length=200, null=True)),
                ('maximum_noise_level', models.CharField(max_length=200, null=True)),
                ('fan_backlight_type', models.CharField(max_length=200, null=True)),
                ('fan_illumination_color', models.CharField(max_length=200, null=True)),
                ('illumination_source', models.CharField(max_length=200, null=True)),
                ('fan_color', models.CharField(max_length=200, null=True)),
                ('thermal_paste_included', models.CharField(max_length=200, null=True)),
                ('equipment', models.CharField(max_length=200, null=True)),
                ('height', models.CharField(max_length=200, null=True)),
                ('width', models.CharField(max_length=200, null=True)),
                ('length', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('additional_information', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hard25',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('hdd_capacity', models.IntegerField(null=True)),
                ('energy_consumption', models.CharField(max_length=200, null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('a_type', models.CharField(max_length=200, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('manufacturer_code', models.CharField(max_length=200, null=True)),
                ('hybrid_sshd_drive_ssd_buffer_capacity', models.CharField(max_length=200, null=True)),
                ('buffer_volume', models.CharField(max_length=200, null=True)),
                ('spindle_speed', models.CharField(max_length=200, null=True)),
                ('average_access_time_read', models.CharField(max_length=200, null=True)),
                ('interface', models.CharField(max_length=200, null=True)),
                ('interface_bandwidth', models.CharField(max_length=200, null=True)),
                ('impact_resistance_during_operation', models.CharField(max_length=200, null=True)),
                ('storage_shock_resistance', models.CharField(max_length=200, null=True)),
                ('noise_level_during_operation', models.CharField(max_length=200, null=True)),
                ('noise_level_at_idle', models.CharField(max_length=200, null=True)),
                ('standard_thickness', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('data_exchange_rate', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='hard35',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('hdd_capacity', models.IntegerField(null=True)),
                ('maximum_power_consumption', models.CharField(max_length=200, null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('manufacturer_code', models.CharField(max_length=200, null=True)),
                ('hybrid_sshd_drive_ssd_buffer_capacity', models.CharField(max_length=200, null=True)),
                ('cache_size', models.CharField(max_length=200, null=True)),
                ('spindle_speed', models.CharField(max_length=200, null=True)),
                ('maximum_baud_rate', models.CharField(max_length=200, null=True)),
                ('average_access_time_read', models.CharField(max_length=200, null=True)),
                ('average_access_time_recording', models.CharField(max_length=200, null=True)),
                ('average_latency', models.CharField(max_length=200, null=True)),
                ('ncq_support', models.CharField(max_length=200, null=True)),
                ('interface', models.CharField(max_length=200, null=True)),
                ('interface_bandwidth', models.CharField(max_length=200, null=True)),
                ('optimized_for_raid_arrays', models.CharField(max_length=200, null=True)),
                ('impact_resistance_during_operation', models.CharField(max_length=200, null=True)),
                ('noise_level_during_operation', models.CharField(max_length=200, null=True)),
                ('noise_level_at_idle', models.CharField(max_length=200, null=True)),
                ('helium_filled', models.CharField(max_length=200, null=True)),
                ('appointment', models.CharField(max_length=200, null=True)),
                ('smr_recording_technology', models.CharField(max_length=200, null=True)),
                ('width', models.CharField(max_length=200, null=True)),
                ('length', models.CharField(max_length=200, null=True)),
                ('thickness', models.CharField(max_length=200, null=True)),
                ('number_of_plates', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('eatures_optional', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='powersupply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('manufacturer_code', models.CharField(max_length=200, null=True)),
                ('color', models.CharField(max_length=200, null=True)),
                ('form_factor', models.CharField(max_length=200, null=True)),
                ('atx12v_version', models.CharField(max_length=200, null=True)),
                ('eps12v_support', models.CharField(max_length=200, null=True)),
                ('certificate_80_plus', models.CharField(max_length=200, null=True)),
                ('power_factor_corrector_pfc', models.CharField(max_length=200, null=True)),
                ('protection_technologies', models.CharField(max_length=200, null=True)),
                ('power_nominal', models.CharField(max_length=200, null=True)),
                ('power_on_the_12_v_line', models.CharField(max_length=200, null=True)),
                ('_12_v_line_current', models.CharField(max_length=200, null=True)),
                ('line_current_3_3_v', models.CharField(max_length=200, null=True)),
                ('line_current_5_v', models.CharField(max_length=200, null=True)),
                ('standby_current_5_v_standby', models.CharField(max_length=200, null=True)),
                ('line_current_12_v', models.CharField(max_length=200, null=True)),
                ('mains_input_voltage_range', models.CharField(max_length=200, null=True)),
                ('detachable_cables', models.CharField(max_length=200, null=True)),
                ('main_power_connector', models.CharField(max_length=200, null=True)),
                ('processor_cpu_power_connectors', models.CharField(max_length=200, null=True)),
                ('graphics_card_power_connectors_pci_e', models.CharField(max_length=200, null=True)),
                ('number_of_15_pin_sata_connectors', models.CharField(max_length=200, null=True)),
                ('number_of_4_pin_molex_connectors', models.CharField(max_length=200, null=True)),
                ('number_of_4_pin_floppy_connectors', models.CharField(max_length=200, null=True)),
                ('main_power_cable_length', models.CharField(max_length=200, null=True)),
                ('processor_power_cable_length', models.CharField(max_length=200, null=True)),
                ('cooling_system', models.CharField(max_length=200, null=True)),
                ('fan_dimensions', models.CharField(max_length=200, null=True)),
                ('backlight_type', models.CharField(max_length=200, null=True)),
                ('backlight_color', models.CharField(max_length=200, null=True)),
                ('wire_braid', models.CharField(max_length=200, null=True)),
                ('network_cable_included', models.CharField(max_length=200, null=True)),
                ('length', models.CharField(max_length=200, null=True)),
                ('width', models.CharField(max_length=200, null=True)),
                ('height', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('equipment', models.CharField(max_length=200, null=True)),
                ('sata_power_cable_length', models.CharField(max_length=200, null=True)),
                ('molex_power_cable_length', models.CharField(max_length=200, null=True)),
                ('features_of_the', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('number_of_modules_included', models.IntegerField(null=True)),
                ('the_volume_of_one_memory_module', models.IntegerField(null=True)),
                ('model', models.CharField(max_length=100, null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('clock_frequency', models.CharField(max_length=100, null=True)),
                ('guarantee', models.CharField(max_length=100, null=True)),
                ('producing_country', models.CharField(max_length=100, null=True)),
                ('manufacturer_code', models.CharField(max_length=100, null=True)),
                ('memory_type', models.CharField(max_length=100, null=True)),
                ('memory_form_factor', models.CharField(max_length=100, null=True)),
                ('register_memory', models.CharField(max_length=100, null=True)),
                ('ecc_memory', models.CharField(max_length=100, null=True)),
                ('bandwidth', models.CharField(max_length=100, null=True)),
                ('intel_xmp_profiles', models.CharField(max_length=100, null=True)),
                ('supported_operating_modes', models.CharField(max_length=100, null=True)),
                ('cas_latency_cl', models.CharField(max_length=100, null=True)),
                ('ras_to_cas_delay_trcd', models.CharField(max_length=100, null=True)),
                ('row_precharge_delay_trp', models.CharField(max_length=100, null=True)),
                ('the_presence_of_a_radiator', models.CharField(max_length=100, null=True)),
                ('illumination_of_board_elements', models.CharField(max_length=100, null=True)),
                ('height', models.CharField(max_length=100, null=True)),
                ('low_profile', models.CharField(max_length=100, null=True)),
                ('supply_voltage', models.CharField(max_length=100, null=True)),
                ('activate_to_precharge_delay_tras', models.CharField(max_length=100, null=True)),
                ('rank', models.CharField(max_length=100, null=True)),
                ('features_optional', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SSD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('manufacturer_code', models.CharField(max_length=200, null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('server', models.CharField(max_length=200, null=True)),
                ('drive_volume', models.IntegerField(null=True)),
                ('physical_interface', models.CharField(max_length=200, null=True)),
                ('nvme', models.CharField(max_length=200, null=True)),
                ('controller', models.CharField(max_length=200, null=True)),
                ('memory_chip_type', models.CharField(max_length=200, null=True)),
                ('bits_per_cell', models.CharField(max_length=200, null=True)),
                ('memory_structure', models.CharField(max_length=200, null=True)),
                ('maximum_sequential_write_speed', models.CharField(max_length=200, null=True)),
                ('maximum_sequential_read_speed', models.CharField(max_length=200, null=True)),
                ('resource_of_work', models.CharField(max_length=200, null=True)),
                ('data_encryption', models.CharField(max_length=200, null=True)),
                ('width', models.CharField(max_length=200, null=True)),
                ('length', models.CharField(max_length=200, null=True)),
                ('thickness_mm', models.CharField(max_length=200, null=True)),
                ('trim_command_support', models.CharField(max_length=200, null=True)),
                ('random_write_speed_4kb_files', models.CharField(max_length=200, null=True)),
                ('mtbf_mean_time_between_failures', models.CharField(max_length=200, null=True)),
                ('maximum_overload_shock_resistance', models.CharField(max_length=200, null=True)),
                ('equipment', models.CharField(max_length=200, null=True)),
                ('features_optional', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('buffer_memory', models.CharField(max_length=200, null=True)),
                ('random_read_speed_4kb_files', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ssd_m2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('link', models.URLField(null=True)),
                ('price', models.IntegerField(null=True)),
                ('picture', models.URLField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('guarantee', models.CharField(max_length=200, null=True)),
                ('producing_country', models.CharField(max_length=200, null=True)),
                ('model', models.CharField(max_length=200, null=True)),
                ('manufacturer_code', models.CharField(max_length=200, null=True)),
                ('server', models.CharField(max_length=200, null=True)),
                ('drive_volume', models.IntegerField(null=True)),
                ('form_factor', models.CharField(max_length=200, null=True)),
                ('logical_interface', models.CharField(max_length=200, null=True)),
                ('m_2_socket_key', models.CharField(max_length=200, null=True)),
                ('nvme', models.CharField(max_length=200, null=True)),
                ('controller', models.CharField(max_length=200, null=True)),
                ('memory_chip_type', models.CharField(max_length=200, null=True)),
                ('bits_per_cell', models.CharField(max_length=200, null=True)),
                ('memory_structure', models.CharField(max_length=200, null=True)),
                ('buffer_memory', models.CharField(max_length=200, null=True)),
                ('memory_chip_layout', models.CharField(max_length=200, null=True)),
                ('maximum_sequential_write_speed', models.CharField(max_length=200, null=True)),
                ('maximum_sequential_read_speed', models.CharField(max_length=200, null=True)),
                ('writing_random_blocks_4kb_qd1', models.CharField(max_length=200, null=True)),
                ('read_4kb_random_blocks_qd1', models.CharField(max_length=200, null=True)),
                ('interface_bandwidth', models.CharField(max_length=200, null=True)),
                ('resource_of_work', models.CharField(max_length=200, null=True)),
                ('mtbf_mean_time_between_failures', models.CharField(max_length=200, null=True)),
                ('maximum_overload_shock_resistance', models.CharField(max_length=200, null=True)),
                ('trim_command_support', models.CharField(max_length=200, null=True)),
                ('pci_e_to_m_2_adapter_included', models.CharField(max_length=200, null=True)),
                ('length', models.CharField(max_length=200, null=True)),
                ('width', models.CharField(max_length=200, null=True)),
                ('thickness', models.CharField(max_length=200, null=True)),
                ('weight', models.CharField(max_length=200, null=True)),
                ('random_block_write_4kb_qd32', models.CharField(max_length=200, null=True)),
                ('data_encryption', models.CharField(max_length=200, null=True)),
                ('nand_memory_interface', models.CharField(max_length=200, null=True)),
                ('read_random_4kb_blocks_qd32', models.CharField(max_length=200, null=True)),
                ('energy_consumption', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cpu',
            name='benchmark_mark',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gpu',
            name='benchmark_mark',
            field=models.IntegerField(default=0),
        ),
    ]
