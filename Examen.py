import datetime
import time


class Task:
    def __init__(self, name, job, is_interruptible, execution_time, period, content, needed, priority, type):
        self.name = name
        self.job = job
        self.is_interruptible = is_interruptible
        self.execution_time = execution_time
        self.period = period
        self.content = content
        self.current_content = 0
        self.needed = needed
        self.priority = priority
        self.type = type
        self.deadline = datetime.datetime.now() + datetime.timedelta(seconds=self.period)
        self.run_at = datetime.datetime.now()
        self.finished = 0

    def can_be_run(self):
        if datetime.datetime.now() >= self.run_at:
            return True
        return False

    def will_be_wasted(self):
        global tank_current_content
        global max_tank
        if self.type == 'pump' and (tank_current_content + self.content > max_tank):
            return True
        return False

    def check_priority(self):
        global tank_current_content
        global can_produce
        global type_priority

        if tank_current_content >= can_produce:
            type_priority = 'machine'
        else:
            type_priority = 'pump'

    def set_pump_priority(self):
        for each in task_list:
            if each.type == "pump":
                each.priority = 2
        self.priority = 1

    def run(self):
        global tank_current_content
        global nbr_motor
        global nbr_wheel
        if self.type == 'pump':
            print(str(timer) + "\tTask " + self.name + " done")
            self.run_at = self.run_at + datetime.timedelta(seconds=self.period)
            self.deadline = self.run_at + datetime.timedelta(seconds=self.period)
            time.sleep(self.execution_time)
            tank_current_content+=self.content
            print("Tank : " + str(tank_current_content))
        if self.type == 'machine':
            print(str(timer) + "\tTask " + self.name + " done")
            self.run_at = self.run_at + datetime.timedelta(seconds=self.period)
            self.deadline = self.run_at + datetime.timedelta(seconds=self.period)
            time.sleep(self.execution_time)
            tank_current_content -= self.content
            print("Tank : " + str(tank_current_content))
            self.current_content+=self.content
            if self.name=='Machine 1':
                nbr_motor+=1
                print("Un moteur créé")
            if self.name=='Machine 2':
                nbr_wheel+=1
                print("Une roue créée")


if __name__ == "__main__":

    # Definition des tâches et ses instantiations
    task_list = [
        Task('Pump 1', job='Produce 10 oil', is_interruptible=False, execution_time=2, period=5, content=10, needed=0, priority=2, type='pump'),
        Task('Pump 2', job='Produce 20 oil', is_interruptible=False, execution_time=3, period=15, content=20, needed=0, priority=1, type='pump'),
        Task('Machine 1', job='Produce 1 motor each 25 oil', is_interruptible=True, execution_time=5, period=5, content=25, needed=1, priority=0, type='machine'),
        Task('Machine 2', job='Produce 1 wheel each 5 oil', is_interruptible=True, execution_time=3, period=5, content=5, needed=4, priority=0, type='machine')
    ]

    global can_produce
    can_produce = 0
    global type_priority
    type_priority = 'pump'
    global max_tank
    max_tank = 50
    global nbr_motor
    nbr_motor = 0
    global nbr_wheel
    nbr_wheel = 0
    global tank_current_content
    tank_current_content = 0
    global number_engine
    number_engine = 0

    for each in task_list:
        if each.type == "machine":
            can_produce=can_produce + (each.content*each.needed)

    global timer
    timer = -1

    while (True):
        timer+=1
        task_to_run = None
        task_priority = 0
        for current_task in task_list:
            current_task.check_priority()
            if current_task.will_be_wasted():
                type_priority = 'machine'
            if current_task.type == type_priority:
                if type_priority == 'pump':
                    task_to_run = current_task
                if type_priority == 'machine':
                    temp = nbr_wheel / 4
                    if temp >= nbr_motor:
                        task_to_run = task_list[2]
                    if temp < nbr_motor:
                        task_to_run = task_list[3]

        if task_to_run == None:
            time.sleep(1)
            print("\tIdle")
        else:
            task_to_run.run()
            if task_to_run.type == 'pump':
                task_to_run.set_pump_priority()

        print("\tNbr motor " + str(nbr_motor))
        print("\tNbr roue " + str(nbr_wheel))
        if nbr_motor > 0:
            print("\tNbr engine " + str(nbr_wheel/nbr_motor))