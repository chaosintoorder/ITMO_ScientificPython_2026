from datetime import datetime
!pip install openmeteo_requests

import openmeteo_requests

class IncreaseSpeed():
  '''
  Iterator for increasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h
    max_speed: a maximum possible value, km/h
    step: a parameter to vary the value to increase by

  Make sure your iterator is not exceeding the maximum allowed value
  '''

  def __init__(self, current_speed: int, max_speed: int, step = 10):
    pass
  def __iter__(self):
    pass
  def __next__(self, step = 10):
    pass

class DecreaseSpeed():
  '''
  Iterator for decreasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h

  Make sure your iterator is not going below zero
  '''

  def __init__(self, current_speed: int, min_speed: int, step=10):
    pass

  def __iter__(self):
    pass

  def __next__(self):
    pass    

class Car():
  '''
  Car class.
  Has a class variable for counting total amount of cars on the road (increased by 1 upon instance initialization).

  Constructor params:
    max_speed: a maximum possible speed, km/h
    current_speed: current speed, km/h (0 by default)
    state: reflects if the Car is in the parking or on the road

  Methods:
    accelerate: increases the speed using IncreaseSpeed() iterator either once or gradually to the upper_border
    brake: decreases the speed using DecreaseSpeed() iterator either once or gradually to the lower_border
    parking: if the Car is not already in the parking, removes the Car from the road
    total_cars: show the total amount of cars on the road
    show_weather: shows the current weather conditions
  '''

  def __init__(self, max_speed: int, current_speed=0):
    pass


  def accelerate(self, upper_border=None, step=10):
    # check for state
    # create an instance of IncreaseSpeed iterator
    # check if smth passed to upper_border and if it is valid speed value
    # if True, increase the speed gradually iterating over your increaser until upper_border is met
    # print a message at each speed increase
    # else increase the speed once
    # return the message with current speed
    pass


  def brake(self, lower_border=None, step=10):
    # create an instance of DecreaseSpeed iterator
    # check if smth passed to lower_border and if it is valid speed value
    # if True, decrease the speed gradually iterating over your decreaser until lower_border is met
    # print a message at each speed decrease
    # else increase the speed once
    # return the message with current speed
    pass

  # the next three functions you have to define yourself
  # one of the is class method, one - static and one - regular method (not necessarily in this order, it's for you to think)

  def parking(self):
    # gets car off the road (use state and class variable)
    # check: should not be able to move the car off the road if it's not there
    pass

  def total_cars(Car):
    # displays total amount of cars on the road
    pass

  def show_weather():
    # displays weather conditions
    pass