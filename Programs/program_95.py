import asyncio
import uuid

class Event:
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload

class EventBus:
    def __init__(self):
        self._queue = asyncio.Queue()
        self._subscribers = {}
    
    async def publish(self, event):
        await self._queue.put(event)

    def subscribe(self, event_type, handler, filter_func=None):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append({'handler': handler, 'filter': filter_func})

    async def run(self):
        while True:
            event = await self._queue.get()
            if event.event_type in self._subscribers:
                subscribers = self._subscribers[event.event_type]
                tasks = []
                for sub in subscribers:
                    if sub['filter'] is None or sub['filter'](event):
                        tasks.append(asyncio.create_task(sub['handler'](event)))
                await asyncio.gather(*tasks)
            self._queue.task_done()

async def email_sender(event):
    print(f"Sending email for user {event.payload['user_id']}")

async def logger(event):
    print(f"LOG: Event '{event.event_type}' received with payload {event.payload}")

def high_priority_filter(event):
    return event.payload.get('priority') == 'high'

async def main():
    bus = EventBus()
    
    bus.subscribe('user_created', email_sender)
    bus.subscribe('user_created', logger)
    bus.subscribe('user_activity', logger, high_priority_filter)
    
    runner = asyncio.create_task(bus.run())

    await bus.publish(Event('user_created', {'user_id': str(uuid.uuid4())}))
    await bus.publish(Event('user_activity', {'user_id': str(uuid.uuid4()), 'priority': 'low'}))
    await bus.publish(Event('user_activity', {'user_id': str(uuid.uuid4()), 'priority': 'high'}))

    await asyncio.sleep(1)
    runner.cancel()
    
if __name__ == '__main__':
    asyncio.run(main())