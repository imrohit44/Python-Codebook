from collections import defaultdict

class State:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<State: {self.name}>"

class Event:
    def __init__(self, name, payload=None):
        self.name = name
        self.payload = payload

    def __repr__(self):
        return f"<Event: {self.name}>"

class FSM:
    def __init__(self, initial_state):
        self._states = {}
        self._transitions = defaultdict(dict)
        self._current_state = initial_state

    def add_state(self, state, on_enter=None, on_exit=None):
        self._states[state.name] = {
            'state': state,
            'on_enter': on_enter,
            'on_exit': on_exit
        }

    def add_transition(self, from_state_name, event_name, to_state_name):
        self._transitions[from_state_name][event_name] = to_state_name

    def dispatch(self, event):
        from_state_name = self._current_state.name
        
        if event.name in self._transitions[from_state_name]:
            to_state_name = self._transitions[from_state_name][event.name]
            
            if self._states[from_state_name]['on_exit']:
                self._states[from_state_name]['on_exit'](self._states[from_state_name]['state'], event)
            
            self._current_state = self._states[to_state_name]['state']

            if self._states[to_state_name]['on_enter']:
                self._states[to_state_name]['on_enter'](self._states[to_state_name]['state'], event)

            return True
        return False

def on_enter_on(state, event):
    print(f"Entering {state.name}, triggered by {event.name}")

def on_exit_on(state, event):
    print(f"Exiting {state.name}, triggered by {event.name}")

def on_enter_off(state, event):
    print(f"Entering {state.name}, triggered by {event.name}")

if __name__ == "__main__":
    on_state = State("on")
    off_state = State("off")
    
    fsm = FSM(off_state)
    fsm.add_state(off_state, on_enter=on_enter_off)
    fsm.add_state(on_state, on_enter=on_enter_on, on_exit=on_exit_on)

    fsm.add_transition("off", "POWER_ON", "on")
    fsm.add_transition("on", "POWER_OFF", "off")

    fsm.dispatch(Event("POWER_ON"))
    fsm.dispatch(Event("POWER_OFF"))
    fsm.dispatch(Event("POWER_OFF"))