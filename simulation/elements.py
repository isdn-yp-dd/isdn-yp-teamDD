import random
import numpy as np
import datahandling  # self-defined module

### const ###
BUS_CYCLE = 7*60
MAX_TIME = 5000
enqueue_weight = [0.2,0.4,0.7,1.2,1.5,
                  1.6,1.3,1,0.8,0.6,
                  0.6,0.9,1,0.6,0.4]

### functions ###
def getRandom(p) -> int :
  if (p == 0) :
    return 0
  return int(random.random() < (p / 100))  # 0 / 1

def getRange(x, y, start) -> list :  # helper function for generating the waiting time list
  # Y = -X + k, k = Y + X, k = x + y, Y = -X + x + y
  return list(range(x + y - start, y - 1, -1))

def loop(t) :
  datahandling.generate_dataset(t)

  for stop in Stop.list_obj :  # handle the queue
    stop.renege(t)
    stop.enqueue(t)

  for bus in Bus.list_obj :  # handle buses
    if (bus.end()) :
      continue
    elif (bus.position == 0) :  # waiting for start
      if (bus.get_on(Stop.list_obj[0], t)) :
        datahandling.handleBus(Bus.list_obj.index(bus), bus.empty_seats, 0, t)  # update seats
      if (t % BUS_CYCLE == 0) or (bus.empty_seats == 0) :  # if full or next bus arrive
        bus.position = 1  # start moving
        datahandling.handleBus(Bus.list_obj.index(bus), bus.empty_seats, 1, t)  # update state
        Stop.list_obj[0].update_waiting_num_bus()
      continue
    elif bus.position in Stop.list_location[1:] :  # if bus at bus stop
      i = Stop.list_location.index(bus.position)
      bus.arrive(Stop.list_obj[i], t)

    bus.position += 1  # move, for every bus
    if bus.position > Stop.list_location[-1] :  # after arrive last stop
      datahandling.handleBus(Bus.list_obj.index(bus), bus.empty_seats, 7, t)
      bus.position = -1

  if (t % BUS_CYCLE == 0) :  # start a new bus for each bus_cycle
    Bus(19)
    datahandling.handleBus(len(Bus.list_obj) - 1, 19, 0, t)  # new minibus
  for stop in Stop.list_obj :
    stop.update_waiting_time()  # waiting time ++

### classes ###
class Bus :  # simplify "minibus" to "bus"

  list_obj = [] # static list to store all minibus

  def __init__(self, capacity = 19) :
    self.position = 0  # current position of the bus
    self.capacity = capacity
    self.empty_seats = capacity
    Bus.list_obj.append(self)
  
  def arrive(self, stop, t) -> int:
    off = 0
    for i in range(self.capacity - self.empty_seats) :
      off += getRandom(stop.P_off)
    self.empty_seats += off
    if (Stop.list_obj[-1] != stop) :
      last = self.get_on(stop, t)
      stop.store_waiting_time(t, last, self.empty_seats)
      datahandling.handleBus(Bus.list_obj.index(self), self.empty_seats, Stop.list_obj.index(stop) + 1, t)
      stop.update_waiting_num_bus()
    return self.empty_seats
  
  def get_on(self, stop, t) :
    if self.empty_seats < len(stop.user_list) :
      on = self.empty_seats
    else :
      on = len(stop.user_list)
    self.empty_seats -= on
    last = None
    for i in range(on) :
      last = stop.dequeue()
    datahandling.handleStop(Stop.list_obj.index(stop), -on, t)
    return last
  
  def end(self) -> bool:
    return (self.position == -1)  # postion = -1 to indicate the minibus arrived the ending of the route
  
class Stop :

  list_obj = [] # a static list storing all stop
  list_location = [] # a static list to store the times
  P_leave = 0 # P(renege)

  def __init__(self, location = -1, P_queue = 0, P_off = 0) :
    self.location = location  # relative "location" of the stop at the route , how many sec needed to go to from the start(by real data)
    self.P_queue = P_queue/10  # P(how many ppl get in the queue per time)/1000
    self.P_off = P_off  # P(how many ppl get off the minibus per people in bus)/100
    self.user_list = []  # a list to store the people waiting at the queue
    self.waiting_time = np.array([])  # a list to store the waiting time of the people
    self.waiting_num_bus = np.array([])  # a list to store the waiting time of the people
    self.arrival_time = []  # a list to store the arrival time of the minibus; for stop[1:-1]
    self.x = 0  # len of waiting_time
    Stop.list_obj.append(self)
    Stop.list_location.append(location)

  def enqueue(self, t) -> int :  # enqueue with given P
    weight = enqueue_weight[t % len(enqueue_weight)]
    if (getRandom(self.P_queue * weight)) :
      self.user_list.append(User(t))
      datahandling.handleStop(Stop.list_obj.index(self), 1, t)
      return 1
    return 0
  
  def renege(self, t) -> int :  # dequeue without getting on the bus
    count = 0
    if (Stop.P_leave > 0) :
      for person in self.user_list :
        if (getRandom(Stop.P_leave)) :
          count += 1
          self.dequeue(person)
      datahandling.handleStop(Stop.list_obj.index(self), -count, t)
    return count
  
  def dequeue(self, person = None) :  # dequeue
    if (person == None) :
      person = self.user_list.pop(0)  # remove the first person if not specified
    else :
      self.user_list.remove(person)
    return person

  def update_waiting_time(self) -> None :
    for user in self.user_list :
      user.waiting_time += 1

  def update_waiting_num_bus(self) -> None :
    for user in self.user_list :
      user.waiting_num_bus += 1

  def store_waiting_time(self, t, last, seats) -> None :
    if (seats > 0) :
      temp = getRange(t, 0, self.x)
      self.waiting_time = np.append(self.waiting_time, temp)
      self.store_waiting_num_bus(t, t)
      self.x = t + 1
    elif (last != None) :  # there is passenger get on
      temp = getRange(last.enqueue_time - 1, last.waiting_time + 1, self.x)
      self.waiting_time = np.append(self.waiting_time, temp)
      self.store_waiting_num_bus(t, last.enqueue_time - 1)
      self.x = last.enqueue_time   

  def store_waiting_num_bus(self, t, tail) -> None :
    temp = self.x
    self.arrival_time.append(t)
    for a in self.arrival_time :
      if (temp > a) :
        continue
      if (a > tail) :
        self.waiting_num_bus = np.append(self.waiting_num_bus, [len(self.arrival_time) - self.arrival_time.index(a)]*(tail-temp+1))
      else :
        # it works, but why need to divide by 2????????
        self.waiting_num_bus = np.append(self.waiting_num_bus, [len(self.arrival_time) - self.arrival_time.index(a)]*(a-temp+1))
      temp = a + 1
    

class User :

  def __init__(self, t) :
    self.enqueue_time = t
    self.waiting_time = 0
    self.waiting_num_bus = 1  # 1 = able to get on the next bus