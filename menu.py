from threading import Thread
from avizon_menu.monitor import system_usage
from avizon_menu.main_menu import menu as main_menu

Thread(target=system_usage).start()
Thread(target=main_menu).start()
