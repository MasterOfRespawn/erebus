from controller import Robot
import numpy as np
import struct

timeStep = 32            # Set the time step for the simulation

robot = Robot()

emitter = robot.getDevice("emitter")

while robot.step(timeStep) != -1:


    # '0': None/Unknown
    # '1': Walls
    # '2': Holes
    # '3': Swamps
    # '4': Checkpoints
    # '5': Starting tile
    # 'b': Connection tile from 1 to 2 (and vice versa)
    # 'p': Connection tile from 2 to 3 (and vice versa)
    # 'r': Connection tile from 3 to 4 (and vice versa)
    # 'g': Connection tile from 1 to 4 (and vice versa)
    # 'o': Connection tile from 1 to 3 (and vice versa)
    # 'y': Connection tile from 2 to 4 (and vice versa)
    # 'H': Harmed victim
    # 'S': Stable victim
    # 'U': Unharmed victim
    # 'F': Flammable Gas
    # 'P': Poison
    # 'C': Corrosive
    # 'O': Organic Peroxide
    # '*': Room 4

    
    """
    ## Test map array for world1.wbt
    subMatrix = np.array([
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['1', '5', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '5', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'S'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '1'],
        ['F', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', 'b', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', 'b', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', 'p', '0', 'p', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', 'p', '0', 'p', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', 'U', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', 'H', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '1'],
        ['P', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
    ])
    """
    

    """
    ## Test map array for world2.wbt
    subMatrix = np.array([
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', 'P', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
        ['1', '4', '0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '2', '0', '2', '1', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '1', '2', '0', '2', '1'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1'], 
        ['1', '4', '0', '4', '0', '0', '0', '0', 'C', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '1', '2', '0', '2', '1'], 
        ['1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1'], 
        ['1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', 'b', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', 'O', '0', '0', '0', '0', '0', '0', '0', '1'], 
        ['1', 'U', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', 'b', '0', 'b', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', 'p', '0', 'p', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', 'H', '0', '0', '0', '0', '0', '0', '0', '1', '5', '0', '5', '1'], 
        ['1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '1', '0', '0', '0', '1', 'p', '0', 'p', '1', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', '1', '0', '0', '0', '0', '0', '0', '0', '1', '5', '0', '5', '1'], 
        ['1', '1', '1', 'S', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '1', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'g', '0', 'g', '0', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'g', '0', 'g', '0', '0', '0', '0', '1'], 
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '4', '0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '4', '0', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1', '0', '0', '0', '0', 'r', '0', 'r', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '0', '0', '0', '0', '0', '1', '0', '0', '2', '0', '2', '1', '0', '0', '0', '0', 'r', '0', 'r', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'], 
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']
    ])
    """

    """
    ## Test map array for room4.wbt
    subMatrix = np.array([
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '5', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'g', '0', 'g', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '5', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'g', '0', 'g', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '1', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', 'H', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '4', '0', '4', '0', '0', '0', '0', 'O', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '4', '0', '4', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '0', '3', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
        ['1', 'b', '0', 'b', '1', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', '1', '0', '0', '0', '0', '0', '0', '0', '1', 'r', '0', 'r', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', 'b', '0', 'b', '1', '0', '0', '0', '0', '0', '0', '0', '0', '4', '0', '4', '1', '0', '0', '0', '0', '0', '0', '0', '1', 'r', '0', 'r', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'F', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', 'U', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'p', '0', 'p', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', 'p', '0', 'p', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '1', 'S', '1', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '2', '1'],
        ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
    ])
    """

    """
    ## Test map array for room4_small.wbt
    subMatrix = np.array([
        ['1', '1', '1', '1', '1', '1', '1', 'U', '1', 'H', '1', '1', '1', '1', '1', 'S', '1'],
        ['1', '5', '0', '5', '0', 'b', '0', 'b', '0', '0', '0', '0', '0', '3', '0', '3', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['1', '5', '0', '5', '0', 'b', '0', 'b', '0', '0', '0', '0', '0', '3', '0', '3', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1'],
        ['1', '0', '0', '0', '0', '2', '0', '2', '1', 'p', '0', 'p', '0', '4', '0', '4', '1'],
        ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['F', '0', '0', '0', '0', '2', '0', '2', '1', 'p', '0', 'p', '0', '4', '0', '4', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '1', '1', '1', '1', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '1', '0', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '1', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', 'P'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', 'r', '0', 'r', '0', '0', '0', '0', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '0', '0', '0', '1', '1', '0', 'C', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', 'r', '0', 'r', '0', '0', '1', '0', '1'],
        ['*', '*', '*', '*', '*', '*', '*', '*', '*', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ['*', '*', '*', '*', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    ])
    """
    
    # Test map array for NewPassages.wbt
    subMatrix = np.array([['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
        ['1','5','0','5','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','5','0','5','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','1','1','1','1','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','1','1','0','0','0','0','0','0','0','1','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','y','0','y','0','0','0','0','0','0','1','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','y','0','y','0','0','0','0','0','0','1','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','1','1','1','1','1','1','1','1','1','0','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','b','0','b','1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','b','0','b','1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
        ['1','1','1','1','1','1','1','1','1','0','0','0','1','1','1','1','1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','1','r','0','r','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','1'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','1','0','0','0','0','0','0','0','1','r','0','r','1','0','0','0','1'],
        ['1','1','1','1','1','0','0','0','0','0','0','0','1','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','1','1','1','1','0','0','0','0','0','1','1','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','0','0','0','0','0','0','0','0','o','0','o','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','1','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','o','0','o','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','0','0','0','0','1','1','1','1','1','1','1','1','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*'],
        ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*']
    ])
    

    # Get shape
    s = subMatrix.shape
    # Get shape as bytes
    s_bytes = struct.pack('2i',*s)

    # Flattening the matrix and join with ','
    flatMap = ','.join(subMatrix.flatten())
    # Encode
    sub_bytes = flatMap.encode('utf-8')

    # Add togeather, shape + map
    a_bytes = s_bytes + sub_bytes

    # Send map data
    emitter.send(a_bytes)
    # Send map evaluate request
    map_evaluate_request = struct.pack('c', b'M')
    emitter.send(map_evaluate_request)

    #########
    #Exit message
    exit_mes = struct.pack('c', b'E')
    emitter.send(exit_mes)

    break
