class EventManager:
    def __init__(self):
        self.listeners = {} # event_type: [list of callables (listeners)]

    def subscribe(self, event_type, listener):
        """Registers a listener for a specific event type."""
        if not callable(listener):
            raise ValueError("Listener must be a callable function or method.")
        self.listeners.setdefault(event_type, []).append(listener)
        print(f"Subscribed '{listener.__name__}' to event '{event_type}'")

    def unsubscribe(self, event_type, listener):
        """Unsubscribes a listener from an event type."""
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)
            print(f"Unsubscribed '{listener.__name__}' from event '{event_type}'")

    def trigger(self, event_type, **event_data):
        """Triggers an event, calling all subscribed listeners."""
        print(f"\n--- Triggering event: '{event_type}' with data: {event_data} ---")
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                try:
                    listener(event_type=event_type, **event_data)
                except Exception as e:
                    print(f"Error calling listener '{listener.__name__}' for event '{event_type}': {e}")
        else:
            print(f"No listeners registered for event type '{event_type}'")

# Example Usage:

# Define some listener functions
def log_event(event_type, message, **kwargs):
    print(f"[LOG] Event '{event_type}': {message}. Extra data: {kwargs}")

def send_notification(event_type, user_id, message, **kwargs):
    print(f"[NOTIFY] User {user_id}: {message}")

class AnalyticsReporter:
    def process_data(self, event_type, data, **kwargs):
        print(f"[ANALYTICS] Processing data for '{event_type}': {data}")

# Create an event manager
event_manager = EventManager()

# Create an instance of the reporter
reporter = AnalyticsReporter()

# Subscribe listeners
event_manager.subscribe("user_login", log_event)
event_manager.subscribe("user_login", send_notification)
event_manager.subscribe("data_updated", log_event)
event_manager.subscribe("data_updated", reporter.process_data)
event_manager.subscribe("order_placed", log_event)

# Trigger events
event_manager.trigger("user_login", user_id=123, message="User logged in successfully.", ip_address="192.168.1.1")
event_manager.trigger("data_updated", data={"item_id": "ABC", "new_value": 150}, timestamp=time.time())
event_manager.trigger("order_placed", order_id="X123", amount=99.99, currency="USD")
event_manager.trigger("unknown_event", info="This event has no listeners.")

# Unsubscribe a listener and trigger again
event_manager.unsubscribe("user_login", send_notification)
event_manager.trigger("user_login", user_id=456, message="Another user login.")