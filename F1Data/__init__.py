import os
from flask import Flask, render_template, request
from F1Data.classes.event import Event
from F1Data.classes.drivers import Drivers
lastest_event = Event()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def index(selected_drivers = [], active_season=lastest_event.current_season, event=lastest_event.lastest_event, upcoming_event = lastest_event.upcoming_event, session = lastest_event.sessions[-1]):
        season = list(range(lastest_event.current_season, 2017, -1))
        season.remove(int(active_season))
        if lastest_event.lastest_event in lastest_event.passed_events:
            lastest_event.passed_events.remove(lastest_event.lastest_event)
        sessions = lastest_event.sessions[::-1]
        sessions.remove(sessions[0])
        sess = lastest_event.load_session(lastest_event.current_season, lastest_event.lastest_event, lastest_event.sessions[-1])
        d = Drivers(sess)
        drivers_info = d.get_drivers_info()
        if request.method == 'POST':
            print(active_season, event, sess)
            if (request.get_json()['selected'] == True):
                selected_drivers.append(request.get_json()['driver'])
            else:
                selected_drivers.remove(request.get_json()['driver'])
        return render_template('index.html', drivers = d, drivers_info=drivers_info, season=season, active_season=active_season, event=event, upcoming_event=lastest_event.upcoming_event, remaining_time=str(lastest_event.remaining_time), events=lastest_event.passed_events[::-1], len = len(lastest_event.passed_events), sessions=sessions, session = lastest_event.sessions[-1], upcoming_race_date=lastest_event.upcoming_event_date)
    
    @app.route('/')
    @app.route('/<active_season>', methods=['GET', 'POST'])
    def get_season(active_season, selected_drivers=[]):
        #selected_drivers = []
        ev = Event(int(active_season))
        season = list(range(ev.current_season, 2017, -1))
        if request.method == 'POST':
            if (request.get_json()['selected'] == True):
                selected_drivers.append(request.get_json()['driver'])
            else:
                if selected_drivers != [] and request.get_json()['driver'] in selected_drivers:
                    selected_drivers.remove(request.get_json()['driver'])
                else:
                    selected_drivers.clear()
        season.remove(int(active_season))
        events = ev.passed_events
        sessions = ev.get_sessions(ev.lastest_event)[::-1]
        events.remove(ev.lastest_event)        
        sessions.remove(sessions[0])
        sess = ev.load_session(int(active_season), ev.lastest_event, ev.sessions[-1])
        d = Drivers(sess)
        drivers_info = d.get_drivers_info()
        return render_template('index.html', drivers=d, drivers_info=drivers_info, season=season, active_season=active_season, event=ev.lastest_event, upcoming_event=lastest_event.upcoming_event, remaining_time=str(lastest_event.remaining_time), events=events[::-1], len = len(events), sessions=sessions, session = ev.sessions[-1], upcoming_race_date=lastest_event.upcoming_event_date)

    
    
    @app.route('/')
    @app.route('/<active_season>/<active_event>', methods=['GET', 'POST'])
    def get_event(active_season, active_event, selected_drivers=[]):
        ev = Event(int(active_season))
        events = ev.passed_events
        season = list(range(ev.current_season, 2017, -1))
        if request.method == 'POST':
            if (request.get_json()['selected'] == True):
                selected_drivers.append(request.get_json()['driver'])
            else:
                if selected_drivers != [] and request.get_json()['driver'] in selected_drivers:
                    selected_drivers.remove(request.get_json()['driver'])
                else:
                    selected_drivers.clear()
        sessions=ev.get_sessions(active_event)[::-1]
        season.remove(int(active_season))
        events.remove(active_event)
        sessions.remove(sessions[0])
        sess = ev.load_session(int(active_season), active_event, ev.sessions[-1])
        d = Drivers(sess)
        drivers_info = d.get_drivers_info()
        return render_template('index.html', drivers=d, drivers_info=drivers_info, season=season, active_season=active_season, event=active_event, upcoming_event=lastest_event.upcoming_event, remaining_time=str(lastest_event.remaining_time), events=ev.passed_events[::-1], len = len(ev.passed_events), sessions=sessions, session = ev.sessions[-1], upcoming_race_date=lastest_event.upcoming_event_date)
    
    @app.route('/')
    @app.route('/<active_season>/<active_event>/<active_session>', methods=['GET', 'POST'])
    def get_session(active_season, active_event, active_session, selected_drivers=[]):
        # NEED TO FIX: pre-season testing sessions NaTType error (no datetimes) -> event.py
        ev = Event(int(active_season))
        events = ev.passed_events
        season = list(range(ev.current_season, 2017, -1))
        if request.method == 'POST':
            if (request.get_json()['selected'] == True):
                selected_drivers.append(request.get_json()['driver'])
            else:
                if selected_drivers != [] and request.get_json()['driver'] in selected_drivers:
                    selected_drivers.remove(request.get_json()['driver'])
                else:
                    selected_drivers.clear()
        print(selected_drivers)
        sessions = ev.get_sessions(active_event)[::-1]
        season.remove(int(active_season))
        events.remove(active_event)
        sessions.remove(active_session)
        sess = ev.load_session(int(active_season), active_event, active_session)
        d = Drivers(sess)
        drivers_info = d.get_drivers_info()
        return render_template('index.html', drivers=d, drivers_info=drivers_info, season=season, active_season=active_season, event=active_event, upcoming_event=lastest_event.upcoming_event, remaining_time=str(lastest_event.remaining_time), events=ev.passed_events[::-1], len = len(ev.passed_events), sessions=sessions, session = active_session, upcoming_race_date=lastest_event.upcoming_event_date)

    return app