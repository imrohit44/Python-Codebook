class Event:
    def __init__(self, name):
        self.name = name
        self._propagation_stopped = False

    def stop_propagation(self):
        self._propagation_stopped = True
    
    @property
    def stopped(self):
        return self._propagation_stopped

class Element:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.listeners = {}
    
    def add_listener(self, event_name, handler):
        self.listeners.setdefault(event_name, []).append(handler)
        
    def dispatch_event(self, event_name):
        event = Event(event_name)
        target = self
        
        while target and not event.stopped:
            print(f"Event '{event_name}' bubbling on {target.name}")
            
            if event_name in target.listeners:
                for handler in target.listeners[event_name]:
                    handler(event)
                    if event.stopped:
                        print(f"Propagation stopped by handler on {target.name}")
                        return
            target = target.parent
        print(f"Event '{event_name}' propagation finished.")

if __name__ == '__main__':
    root = Element("Window")
    container = Element("Container", root)
    button = Element("Button", container)
    
    def container_handler_stop(event):
        print("Container handled event and STOPPED.")
        event.stop_propagation()

    def root_handler(event):
        print("Window handled event.")

    container.add_listener("click", container_handler_stop)
    root.add_listener("click", root_handler)
    
    button.dispatch_event("click")