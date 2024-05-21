import fastf1
from datetime import datetime
import pytz
from dateutil import tz

class Event:
    __utc = pytz.UTC
    current_date = __utc.localize(datetime.now())
    
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    current_date = current_date.replace(tzinfo=from_zone)
    
    def __init__(self, current_season = current_date.year):
        self.current_season = datetime.now().year
        self.schedule = fastf1.get_event_schedule(current_season)
        self.passed_events = []
        self.sessions = []
        for i in range(len(self.schedule)):
            if self.__utc.localize(self.schedule['EventDate'].iloc[i]) < self.current_date and self.schedule['EventFormat'].iloc[i] != 'testing':
                self.passed_events.append(self.schedule['EventName'].iloc[i])
                if i < len(self.schedule) and current_season == self.current_date.year:
                    self.upcoming_event = self.schedule['EventName'].iloc[i+1]
                    self.upcoming_event_date = self.schedule['Session5Date'].iloc[i+1].astimezone(self.to_zone)
                    self.remaining_time = (self.upcoming_event_date - self.current_date)
        self.lastest_event = self.passed_events[-1]
        self.get_sessions(self.lastest_event)

    def get_sessions(self, active_event, selected_drivers=[]):
        self.sessions = []
        sessions_dt = self.schedule.iloc[self.passed_events.index(active_event)][['Session1Date', 'Session2Date', 'Session3Date', 'Session4Date', 'Session5Date']]
        sessions_name = self.schedule.iloc[self.passed_events.index(active_event)][['Session1', 'Session2', 'Session3', 'Session4', 'Session5']]
        for i in range(len(sessions_dt)):
            if sessions_dt.iloc[i] < self.current_date and sessions_name.iloc[i] != None:
                self.sessions.append(sessions_name.iloc[i])
        return self.sessions
    
    def load_session(self, season, event, session):
        s = fastf1.get_session(season, event, session)
        s.load()
        return s
        