from F1Data.classes.event import Event
#from event import Event

class Drivers:
    __drivers_info = {}
    def __init__(self, session) -> None:
        self.__drivers_info = {}
        drivers = session.drivers
        for driver in drivers:
            d = session.get_driver(driver)
            self.__drivers_info[driver] = {'Abb': d['Abbreviation'], 'Color': d['TeamColor']}

    def get_drivers_info(self):
        return self.__drivers_info
    
    def get_driver_abb(self, driver):
        return self.__drivers_info[driver]['Abb']
    
    def get_driver_color(self, driver):
        return self.__drivers_info[driver]['Color']


if __name__ == '__main__':
    ev = Event()
    session = ev.load_session(2024, 'Miami Grand Prix', 'Q')
    drivers = Drivers(session)
    drivers_info = drivers.get_drivers_info()
    print(drivers_info)
    print()
    for driver in drivers_info:
        print(drivers.get_driver_abb(driver), session.laps.pick_driver(driver).pick_fastest()['LapTime'], session.laps.pick_driver(driver).pick_fastest()['Compound'], session.laps.pick_driver(driver).pick_fastest()['TyreLife'])
    