#!/venv/bin/python

import configparser
import json
import logging
import random 
import sys

#Define config and logger.
CONFIG = configparser.ConfigParser()
CONFIG.read('conf/config.ini')
SECTION = 'battleship'

logging.basicConfig(filename=CONFIG[SECTION]['log'],\
                    level=CONFIG[SECTION]['level'],\
                    format='%(asctime)s::%(name)s::%(funcName)s::%(levelname)s::%(message)s',\
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(SECTION)

def show_sections():
    '''
    Output all options for given section
    '''

    conf_str = "\n\n"
    for sect in CONFIG.sections():
        conf_str += "[" + sect + "]\n"
        for var in list(CONFIG[sect]):
            conf_str += var + "\t\t=\t" + CONFIG[sect][var] + "\n"
    logger.info(conf_str)

class Ship:
    '''
    Create class
    '''

    def __init__(self, start, length, direction, map):
        self.start = start
        self.direction = direction
        self.length = length
        self.map = map

        self.direction, self.positions = self.set_direction()

    def set_direction(self):
        '''
        Check if direction is valid.
        '''

        positions = []

        if self.direction == "vertical":
            if self.start[1]+self.length-1 < self.map[1] and self.start[0]<self.map[0]:
                for x in range(self.length):
                    positions.append([self.start[0], self.start[1]+x])
            else:
                return None, None
        elif self.direction == "horizontal":
            if self.start[0]+self.length-1 < self.map[0] and self.start[1]<self.map[1]:
                for x in range(self.length):
                    positions.append([self.start[0]+x, self.start[1]])
            else:
                return None, None
        else:
            return None, None
        return self.direction, positions


    def __str__(self):
        '''
        stringify
        '''
        return json.dumps(vars(self), indent=2)

class Fleet:
    '''
    Create class
    '''

    def __init__(self):
        self.positions = []
        self.ships = []


    def add_ship(self, ship):
        '''
        Add ship to fleet.
        '''
        self.ships.append(ship)


    def get_positions(self):
        '''
        Return ship positions
        '''

        positions = []
        for ship in self.ships:
            positions += ship.positions
        
        return positions

    def __str__(self):
        '''
        stringify
        '''
        return json.dumps(vars(self), indent=2)

def build_ship(map_dims):
    '''
    Generate a ship object with random params.
    '''

    length = random.randint(1,3)
    direction = ["vertical", "horizontal"][random.randint(0,1)]
    start = [random.randint(0,map_dims[0]), random.randint(0,map_dims[1])]

    return Ship(start, length, direction, map_dims)

def check_map(ship_pos, fleet_pos):
    '''
    Check if ship is on any of the existing positions
    '''

    for x in ship_pos:
        if x in fleet_pos:
            print("Overlapping ship.")
            return True
    return False

def main():
    '''
    Main function.
    '''
    logger.info("####################STARTING####################")

    if CONFIG[SECTION]['level'] == "DEBUG":
        show_sections()

    map_dims = [50,14]

    fleet_human = Fleet()
    counter = 0
    while True:
        ship = build_ship(map_dims) # Ship([0, 0], 2, 'vertical', map_dims)
        if not ship.positions or check_map(ship.positions, fleet_human.get_positions()):
            del ship
            print("object destroyed")
        else:
            counter+= 1
            fleet_human.add_ship(ship)
        if counter > 4:
            break

    for x in reversed(range(map_dims[1])):
        for y in range(map_dims[0]):
            if [y, x] in fleet_human.get_positions():
                print("x", end="")
            else:
                print("*", end="")
            # print(x, end="")
        print()
        # print(y)

    # print("ship coords: ")
    # print(fleet_human.get_positions())
    # print(fleet_human.ships)

if __name__ == "__main__":
    main()
