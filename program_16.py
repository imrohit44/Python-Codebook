from abc import ABC, abstractmethod

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError("Observer must be an instance of an Observer subclass.")
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Subject: Attached observer {observer.__class__.__name__}")

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Subject: Detached observer {observer.__class__.__name__}")

    def notify(self, event_type, data):
        print(f"\nSubject: Notifying observers about event '{event_type}' with data: {data}")
        for observer in self._observers:
            # Apply the observer's filter before updating
            if observer.filter_func and not observer.filter_func(event_type, data):
                print(f"  Observer {observer.__class__.__name__}: Filtered out event '{event_type}'.")
                continue
            observer.update(event_type, data)

class Observer(ABC):
    def __init__(self, filter_func=None):
        """
        Args:
            filter_func (callable, optional): A function that takes (event_type, data)
                                              and returns True if the event should be processed,
                                              False otherwise.
        """
        self.filter_func = filter_func

    @abstractmethod
    def update(self, event_type, data):
        """Receives update from the subject."""
        pass

class LoggerObserver(Observer):
    def update(self, event_type, data):
        print(f"Logger: Event '{event_type}' received. Logging data: {data}")

class NotifierObserver(Observer):
    def __init__(self, notification_threshold=None, filter_func=None):
        super().__init__(filter_func)
        self.notification_threshold = notification_threshold

    def update(self, event_type, data):
        if self.notification_threshold and isinstance(data, dict) and 'value' in data:
            if data['value'] > self.notification_threshold:
                print(f"Notifier: ALERT! Event '{event_type}' with value {data['value']} exceeds threshold {self.notification_threshold}!")
            else:
                print(f"Notifier: Notification for '{event_type}'. Value: {data['value']}.")
        else:
            print(f"Notifier: Basic notification for '{event_type}'. Data: {data}")

# Custom filter functions
def high_priority_filter(event_type, data):
    return isinstance(data, dict) and data.get('priority', 'low') == 'high'

def payment_event_filter(event_type, data):
    return event_type == 'payment_received'

# Example Usage:
if __name__ == "__main__":
    subject = Subject()

    # Create observers with and without filters
    logger_all = LoggerObserver()
    logger_high_priority = LoggerObserver(filter_func=high_priority_filter)
    
    notifier_all = NotifierObserver()
    notifier_critical_value = NotifierObserver(notification_threshold=100)
    notifier_payment = NotifierObserver(filter_func=payment_event_filter)

    subject.attach(logger_all)
    subject.attach(logger_high_priority)
    subject.attach(notifier_all)
    subject.attach(notifier_critical_value)
    subject.attach(notifier_payment)

    # Trigger various events
    subject.notify("user_activity", {"user": "Alice", "action": "login", "priority": "low"})
    subject.notify("system_alert", {"component": "DB", "message": "High CPU usage", "value": 120, "priority": "high"})
    subject.notify("data_update", {"record_id": 1, "value": 75})
    subject.notify("payment_received", {"transaction_id": "T101", "amount": 250.75, "currency": "USD"})
    subject.notify("low_value_event", {"item": "widget", "value": 50})

    # Detach an observer and trigger again
    subject.detach(notifier_all)
    subject.notify("user_activity", {"user": "Bob", "action": "logout", "priority": "medium"})