import threading
import time

NUM_PHILOSOPHERS = 5

class Philosopher(threading.Thread):
    def __init__(self, index, left_fork, right_fork):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        
    def run(self):
        for _ in range(3):
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.index} is thinking.")
        time.sleep(random.uniform(0.5, 1.5))

    def eat(self):
        first_fork, second_fork = sorted([self.left_fork, self.right_fork], key=lambda x: x.name)
        
        with first_fork:
            print(f"Philosopher {self.index} picked up {first_fork.name}.")
            with second_fork:
                print(f"Philosopher {self.index} picked up {second_fork.name} and is EATING.")
                time.sleep(random.uniform(0.5, 1.5))
                print(f"Philosopher {self.index} finished eating.")

if __name__ == '__main__':
    forks = [threading.Lock() for i in range(NUM_PHILOSOPHERS)]
    for i, fork in enumerate(forks):
        fork.name = f"Fork-{i}"

    philosophers = [
        Philosopher(i, forks[i], forks[(i + 1) % NUM_PHILOSOPHERS])
        for i in range(NUM_PHILOSOPHERS)
    ]

    for p in philosophers:
        p.start()
    for p in philosophers:
        p.join()