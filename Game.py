"""
    File:               Game.py
    Associated Files:   Robot.py, %PLAYERNAME%Robot.py
    Packages Needed:    time, os, random, abc
    Date Created:       7/8/2020
    Author:             John Lukowski
    Date Modified:      7/9/2020 by John Lukowski
    Modified By:        John Lukowski
    License:            CC-BY-SA-4.0

    Purpose:            Take actions from a user-made Robot to try to move laundry to a hamper
                        Gives rewards, can be used to teach reinforced learning
"""

# Imports
import time, os, random

"""
    Class:      Game
    Purpose:    Run a laundry collection game for a student made robot class
    Methods:    __printRoom, __takeAction, __left, __right, __up, __down, __collect, __place, __runGame
"""
class Game:
    def __init__(self, size, iterations, print):
        self.__delay = .2
        self.__print = print
        self.__size = size if size > 1 else 2
        if self.__size > 20:    self.__size = 20
        self.__iterations = iterations if iterations > 0 else 1
        if self.__iterations > 12000000:    self.__iterations = 12000000
        self.__hamper = (random.randint(0,self.__size-1),random.randint(0,self.__size-1))
        self.__laundry = (random.randint(0,self.__size-1),random.randint(0,self.__size-1))
        while self.__laundry == self.__hamper:
            self.__laundry = (random.randint(0, self.__size - 1), random.randint(0, self.__size - 1))
        self.__robot = (random.randint(0, self.__size - 1), random.randint(0, self.__size - 1))
        self.__hamperReward = 15 * int(self.__size/2)
        self.__laundryReward = 5 * int(self.__size/2)
        self.__laundryDropReward = -2 * int(self.__size / 2)
        self.__score = 0
        self.__robotHasLaundry = False
        self.__actions = {'left': self.__left,
                          'right': self.__right,
                          'up': self.__up,
                          'down': self.__down,
                          'collect': self.__collect,
                          'place': self.__place}
        self.__runGame()

    """
        Function:   __printRoom
        Params:     
        Purpose:    display the room grid with the robot, laundry pile and hamper
        Returns:    
    """
    def __printRoom(self):
        for row in range(self.__size):
            for col in range(self.__size):
                if (row,col) == self.__robot:
                    print('R',end=' ')
                elif (row,col) == self.__hamper:
                    print('H', end=' ')
                elif (row,col) == self.__laundry:
                    print('L', end=' ')
                else:
                    print('*', end=' ')
            print()

    """
        Function:   __takeAction
        Params:     action(string from actions)
        Purpose:    let the robot interact with the game
        Returns:    reward the robot for that action
    """
    def __takeAction(self,action):
        if action in self.__actions:
            return self.__actions[action]()
        return 0

    """
        Function:   __left
        Params:     
        Purpose:    if the robot can, move it to the left
        Returns:    reward the robot for that action
    """
    def __left(self):
        if self.__robot[1] > 0:
            self.__robot = (self.__robot[0],self.__robot[1]-1)
        return 0

    """
        Function:   __right
        Params:     
        Purpose:    if the robot can, move it to the right
        Returns:    reward the robot for that action
    """
    def __right(self):
        if self.__robot[1] < self.__size-1:
            self.__robot = (self.__robot[0],self.__robot[1]+1)
        return 0

    """
        Function:   __up
        Params:     
        Purpose:    if the robot can, move it to up
        Returns:    reward the robot for that action
    """
    def __up(self):
        if self.__robot[0] > 0:
            self.__robot = (self.__robot[0]-1, self.__robot[1])
        return 0

    """
        Function:   __down
        Params:     
        Purpose:    if the robot can, move it down
        Returns:    reward the robot for that action
    """
    def __down(self):
        if self.__robot[0] < self.__size - 1:
            self.__robot = (self.__robot[0]+1, self.__robot[1])
        return 0

    """
        Function:   __collect
        Params:     
        Purpose:    if the robot is over the laundry pile, pick up one piece
        Returns:    reward the robot for that action
    """
    def __collect(self):
        if not self.__robotHasLaundry and self.__robot == self.__laundry:
            self.__robotHasLaundry = True
            if self.__print:
                print('Successfully collected laundry')
            return self.__laundryReward
        return 0

    """
        Function:   __place
        Params:     
        Purpose:    drop held laundry(if holding)
        Returns:    reward the robot for that action
    """
    def __place(self):
        if self.__robotHasLaundry and self.__robot == self.__hamper:
            self.__robotHasLaundry = False
            if self.__print:
                print('Successfully deposited laundry')
            return self.__hamperReward
        elif self.__robotHasLaundry:
            self.__robotHasLaundry = False
            if self.__print:
                print('Incorrectly deposited laundry')
            return self.__laundryDropReward
        return 0

    """
        Function:   __runGame
        Params:     
        Purpose:    run the game loop for the given number of iterations
        Returns:    
    """
    def __runGame(self):
        robot = input('Input name of Robot class to run:\n> ')
        try:
            # Have the user give File/Class name for a Robot
            robot = getattr(__import__(robot),robot)
            # Check to make sure it is a child of Robot
            if str(robot.__bases__) != "(<class 'Robot.Robot'>,)":
                raise Exception('Not a Robot class')
            # Create the robot object with the default game properties
            robot = robot(self.__robot,self.__robotHasLaundry,self.__size,list(self.__actions.keys()))
        except Exception as e:
            raise e

        # Run the game loop
        print('Running ...')
        for turn in range(1,self.__iterations+1):
            # If printing, print out turn/game stats and the board
            if self.__print:
                print('Iteration: ' + str(turn) + '/' + str(self.__iterations))
                print('Score:', self.__score)
                self.__printRoom()
            # Get an action from the robot
            action = robot.getAction()
            if action not in self.__actions:
                raise Exception('Invalid Robot action:',action)
            # Perform the Robot's action
            reward = self.__takeAction(action)
            self.__score += reward
            # Call all the Robot's helper methods to update it for the next turn
            robot.rewarded(action, reward)
            robot.setStats(self.__robot, self.__robotHasLaundry, self.__score)
            # If printing, delay the screen, then clear it
            if self.__print:
                print('Action Taken:', action)
                print()
                time.sleep(self.__delay)
                os.system('cls' if os.name=='nt' else 'clear')
        # Game is over, let the robot know
        robot.finished()
# END OF GAME CLASS

# Run the game with a given size, iterations and print-step/not print
try:
    game = Game(int(input('Input size of room (2-20):\n> ')),
                int(input('Input iterations to run (1-12000000):\n> ')),
                input('Would you like to print the room? (printing drastically slows program)\n(y/n) > ')=='y')
except Exception as e:
    print('Game Exited With Error:',e)