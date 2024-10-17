from threading import Thread
from queue import Queue
import time
import random


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        r = random.randint(3, 10)
        time.sleep(r)


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                for table in self.tables:
                    if table.guest is None:
                        table.guest = guest
                        guest.start()
                        print(f'{guest.name} сел(-а) за стол номер {table.number}')
                        break

            else:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
            if not self.queue.empty() and any(table.guest is None for table in self.tables):
                for table in self.tables:
                    if table.guest is None:
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f"{new_guest.name} вышел из очереди и сел за стол номер {table.number}")
                        new_guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
                'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra']
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
