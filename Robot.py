"""
    File:               Robot.py
    Associated Files:   Game.py, %PLAYERNAME%Robot.py
    Packages Needed:    time, os, random, abc
    Date Created:       7/8/2020
    Author:             John Lukowski
    Date Modified:      7/9/2020 by John Lukowski
    Modified By:        John Lukowski
    License:            CC-BY-SA-4.0

    Purpose:            Built as an abstract class for users to extend.
                        Used to give actions to the laundry game and receive updates/rewards
"""

# Imports
from abc import ABC,abstractmethod

"""
    Class:              Robot, abstract class
    Purpose:            Template for users to extend and create a Robot for the laundry game
    Methods:            setStats, getPosition, hasLaundry, getRoomSize, getActions
    Abstract Methods:   created, getAction, rewarded, updated, finished
"""
class Robot(ABC):
    def __init__(self, position, laundry, roomSize, actions):
        self.__position = position
        self.__laundry = laundry
        self.__roomSize = roomSize
        self.__actions = actions
        self.__score = 0
        self.created()

    """
        Function:   setStats
        Params:     position (int,int), laundry (bool), score (int)
        Purpose:    called by Game, updates the Robot's stats, tells the Robot it has been updated
        Returns:    
    """
    def setStats(self, position, laundry, score):
        self.__score = score
        self.__position = position
        self.__laundry = laundry
        self.updated()

    """
        Function:   getScore
        Params:     
        Purpose:    called by child class, gets the current game score
        Returns:    score (int)
    """
    def getScore(self):
        return self.__score

    """
        Function:   getPosition
        Params:     
        Purpose:    called by child class, gets the current position of the robot
        Returns:    position (int, int)
    """
    def getPosition(self):
        return self.__position

    """
        Function:   hasLaundry
        Params:     
        Purpose:    called by child class, gets whether the robot is holding laundry (True/False)
        Returns:    score (bool)
    """
    def hasLaundry(self):
        return self.__laundry

    """
        Function:   getRoomSize
        Params:     
        Purpose:    called by child class, gets the room's dimension
        Returns:    size (int)
    """
    def getRoomSize(self):
        return self.__roomSize

    """
        Function:   getActions
        Params:     
        Purpose:    called by child class, gets the list of all possible actions
        Returns:    actions (list of strings)
    """
    def getActions(self):
        return self.__actions

    """
        Function:   created
        Params:     
        Purpose:    called by Game when the Robot is created
        Returns:    
    """
    @abstractmethod
    def created(self):  pass

    """
        Function:   getAction
        Params:     
        Purpose:    called by Game, requests action from the Robot
        Returns:    action (string from action list in getActions)
    """
    @abstractmethod
    def getAction(self):   pass

    """
        Function:   rewarded
        Params:     action (string), reward (double)
        Purpose:    called by Game, gives the reward for the last executed action
        Returns:    
    """
    @abstractmethod
    def rewarded(self, action, reward): pass

    """
        Function:   updated
        Params:     
        Purpose:    called by Game at the end of the turn, means that the Robot's state is fully updated
        Returns:    
    """
    @abstractmethod
    def updated(self): pass

    """
        Function:   finished
        Params:     
        Purpose:    called by Game when the Game has finished (gone through all iterations)
        Returns:    
    """
    @abstractmethod
    def finished(self): pass
# END OF ROBOT CLASS