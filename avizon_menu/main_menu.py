import numpy as np
from crontab import CronTab
from os import system, path
from avizon_core import database
from avizon_menu import udp_submenu, display, network_submenu
from avizon_core.network import get_size


def reload_avizon_service():
    if path.isfile('/var/www/avizon/range_ips'):
        database.set_parameter('range_ips', open('/var/www/avizon/range_ips').read())
    else:
        system('cp /var/www/avizon/else/range_ips /var/www/avizon/range_ips')
        database.set_parameter('range_ips', open('/var/www/avizon/range_ips').read())
    system('systemctl restart avizon.service')

def cron_setter():
    display.banner()
    print(f"\n{display.cornsilk_color}Enter the number of minutes you want avizon to run per hour (muss be <= 30).\n")
    selection = int(input("\nNumber of minutes per hour?"))
    
    if 0 < selection <= 30:
        cron = cron_remover()
        start_mins = np.linspace(0, 58, selection, dtype=int)
        stop_mins = start_mins + 1
        for start, end in zip(start_mins, stop_mins):
            job = cron.new(command='systemctl start avizon.service')
            job.setall(f'{start} * * * *')
            job = cron.new(command='systemctl stop avizon.service')
            job.setall(f'{end} * * * *')
        cron.write()
        return menu()
    elif selection == 0:
        return menu()
    else:
        return cron_setter()

def cron_remover():
    cron = CronTab(user=True)
    iter = cron.find_command('avizon')
    for job in iter:
        cron.remove(job)
    cron.write()
    return cron

def menu():
    display.banner()
    database.set_parameter('in_submenu', False)
    print(
        f"\n\n\n\n\n\n\n"
        f"{display.gold_color}--------------{display.magenta_color}Control menu{display.gold_color}-------------\n\n"
        f"{display.cornsilk_color}[1] - Fake udp uploader menu : "

        f"settings: {udp_submenu.fake_udp_uploader_running_status() + display.cornsilk_color} / "
        f"{display.cyan_color + str(database.get_parameter('coefficient_buffer_size')) + display.cornsilk_color} / "
        f"{display.cyan_color + str(database.get_parameter('coefficient_uploader_threads_count'))}"
        f"{display.cornsilk_color} / {display.cyan_color}"
        f"{str(database.get_parameter('coefficient_buffer_sending_speed')) + display.cornsilk_color}\n\n"
        f"[2] - network menu : "
        f"(Σ Upload= "
        f"{display.cyan_color + str(get_size(database.get_parameter('total_upload_cache'))) + display.cornsilk_color} "
        f"|| Σ Download= "
        f"{display.cyan_color + str(get_size(database.get_parameter('total_download_cache'))) + display.cornsilk_color}"
        f")\n\n"
        f"{display.cornsilk_color}[3] - Add cron commands\n"
        f"{display.cornsilk_color}[4] - Remove cron commands\n\n"
        f"{display.cornsilk_color}[9] - Reload\n"
        f"[0] - Exit\n\n"
        f"ENTER YOUR SELECTION: \n")
    user_choice = input()
    if user_choice == '1':
        database.set_parameter('in_submenu', True)
        return udp_submenu.menu()
    elif user_choice == '2':
        database.set_parameter('in_submenu', True)
        return network_submenu.menu()
    elif user_choice == '9':
        reload_avizon_service()
        return menu()
    elif user_choice == '0':
        database.set_parameter('in_submenu', None)
        print(display.reset_color)
        return exit()
    elif user_choice == '3':
        return cron_setter()
    elif user_choice == '4':
        cron_remover()
        return menu()
    else:
        return menu()
