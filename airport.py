from random import seed, uniform, randint, choice
from time import sleep

def sort_planes(planes):
    for j in range(len(planes)):
        for k in range(j+1, len(planes)):
            if planes[k].status < planes[j].status:
                planes[k], planes[j] = planes[j], planes[k]

def int2ordinal(num):
    ordinal_dict = {1: "st", 2: "nd", 3: "rd"}
    q, mod = divmod(num, 10)
    suffix = q % 10 != 1 and ordinal_dict.get(mod) or "th"
    return f"{num}{suffix}"


class Line():

    def __init__(self, number, is_busy, busy_by, busy_time):
        self.__number = number
        self.__is_busy = is_busy
        self.__busy_by = busy_by
        self.__busy_time = busy_time

    @property
    def number(self):
        return self.__number

    @property
    def is_busy(self):
        return self.__is_busy
    
    @property
    def busy_by(self):
        return self.__busy_by
    
    @property
    def busy_time(self):
        return self.__busy_time
    
    @number.setter
    def number(self, number):
        self.__number = number
    
    @is_busy.setter
    def is_busy(self, is_busy):
        self.__is_busy = is_busy

    @busy_by.setter
    def busy_by(self, busy_by):
        self.__busy_by = busy_by

    @busy_time.setter
    def busy_time(self, busy_time):
        self.__busy_time = busy_time

    def __str__(self):
        return f"Line {self.number}"

    
class PlaneType():

    def __init__(self, name, boarding_time):
        self.__name = name
        self.__boarding_time = boarding_time

    @property
    def name(self):
        return self.__name
    
    @property
    def boarding_time(self):
        return self.__boarding_time
    
    @name.setter
    def name(self, name):
        self.__name = name

    @boarding_time.setter
    def boarding_time(self, boarding_time):
        self.__boarding_time = boarding_time

    
class Plane(PlaneType):

    def __init__(self, name, boarding_time, series_number, fuel, status, land_or_fly):
        super().__init__(name, boarding_time)
        self.__series_number = series_number
        self.__fuel = fuel
        self.__status = status        
        self.__land_or_fly = land_or_fly

    @property
    def series_number(self):
        return self.__series_number
    
    @property
    def fuel(self):
        return self.__fuel
    
    @property
    def status(self):
        return self.__status
    
    @property
    def land_or_fly(self):
        return self.__land_or_fly
    
    @series_number.setter
    def series_number(self, series_number):
        self.__series_number = series_number

    @fuel.setter
    def fuel(self, fuel):
        self.__fuel = fuel

    @status.setter
    def status(self, status):
        self.__status = status

    @land_or_fly.setter
    def land_or_fly(self, land_or_fly):
        self.__land_or_fly = land_or_fly

    def take_line(self, line):
        line.is_busy = True
        line.busy_by = Plane(self.name, self.boarding_time, self.series_number, self.fuel, self.status, self.land_or_fly)
        line.busy_time = self.boarding_time

    def fill_fuel(self):
        self.fuel = self.fuel + (100 - self.fuel)

    def take_off(self, line):
        self.fill_fuel()
        self.take_line(line)

    def land(self, line):
        self.take_line(line)

    
class Airport(Line, Plane):

    def __init__(self, lines, landed_planes=[], to_land=[], to_fly=[]):
        self.__lines = lines
        self.__landed_planes = landed_planes
        self.__to_land = to_land
        self.__to_fly = to_fly

    @property
    def lines(self):
        return self.__lines
    
    @property
    def landed_planes(self):
        return self.__landed_planes
    
    @property
    def to_land(self):
        return self.__to_land
    
    @property
    def to_fly(self):
        return self.__to_fly
    
    def airport_work(self):
        while True:
            seed()
            for line in self.lines.keys():
                if not (self.landed_planes or self.to_fly or self.to_land):
                    continue
                if line.busy_time > 0:
                    line.busy_time -= 1
                else:
                    if line.busy_by != "Free":
                        if line.busy_by.land_or_fly == "land":
                            self.landed_planes.append(line.busy_by)
                            line.busy_by = "Free"
                            line.is_busy = False
                        elif line.busy_by.land_or_fly == "fly":
                            line.busy_by = "Free"
                            line.is_busy = False
            
            if self.to_land:
                sort_planes(self.to_land)
                for plane in self.to_land:
                    flag = True
                    for line in self.lines:
                        if not line.is_busy:
                            self.lines[line] = plane
                            self.to_land[0].take_line(line)
                            del self.to_land[0]
                            flag = False
                            break
                    if flag:
                        plane.status -= 0.01
                        plane.fuel -= 1

            if self.to_fly:
                sort_planes(self.to_fly)
                for plane in self.to_fly:
                    flag = True
                    for line in self.lines:
                        if not line.is_busy:
                            self.to_fly[0].take_line(line)
                            del self.to_fly[0]
                            flag = False
                            break
                    if flag:
                        plane.status -= 0.01

            land_probability = randint(0, 1)
            if land_probability:
                plane_name = choice(["Swallow", "Dragonfly", "Ravencroft", "Nightingale", "Morning Star", "Seagull"])
                match plane_name:
                    case "Swallow":
                        plane_boarding_time = 1
                    case "Dragonfly":
                        plane_boarding_time = 2
                    case "Ravencroft":
                        plane_boarding_time = 3
                    case "Nightingale":
                        plane_boarding_time = 4
                    case "Morning Star":
                        plane_boarding_time = 5
                    case "Seagull":
                        plane_boarding_time = 6
                plane_series_number = randint(0, 1000000)
                plane_status = round(uniform(0.01, 1), 2)
                if plane_status == 0:
                    plane_status += 0.1
                if plane_status == 1:
                    plane_status -= 0.1
                plane_fuel = randint(1, 100)
                plane = Plane(plane_name, plane_boarding_time, plane_series_number, plane_fuel, plane_status, "land")
                self.to_land.append(plane)
            
            fly_probability = randint(0, 1)
            if fly_probability and self.landed_planes:
                plane = choice(self.landed_planes)
                plane.fill_fuel()
                plane.status = 1
                plane.land_or_fly = "fly"
                self.to_fly.append(plane)
                del self.landed_planes[self.landed_planes.index(plane)]

            print(f"lines - {self.lines}")
            print(f"landed - {self.landed_planes}")
            print(f"to land - {self.to_land}")
            print(f"to fly - {self.to_fly}")
            print('-'*30)

            sleep(1)

lines = dict.fromkeys([Line(int2ordinal(i+1), False, "Free", 0) for i in range(11)])
airport = Airport(lines)
airport.airport_work()
