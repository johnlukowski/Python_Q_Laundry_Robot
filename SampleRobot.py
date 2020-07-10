"""
    File:               SampleRobot.py
    Associated Files:   Game.py, Robot.py
    Packages Needed:    time, os, random, abc, matplotlib
    Date Created:       7/8/2020
    Author:             John Lukowski
    Date Modified:      7/9/2020 by John Lukowski
    Modified By:        John Lukowski
    License:            CC-BY-SA-4.0

    Purpose:            Built as a sample class extending Robot
                        Used to help teacher teach Q-Learning
"""

# Imports
from Robot import Robot
import random, matplotlib.pyplot as plt

"""
    Class:              Robot, abstract class
    Purpose:            Template for users to extend and create a Robot for the laundry game
    Methods:            created, getAction, rewarded, updated, finished, printQ, prettyPrintQ
    Inherited Methods:  setStats, getPosition, hasLaundry, getRoomSize, getActions
"""
class SampleRobot(Robot):
    """
        Function:   created (Overridden)
        Params:
        Purpose:    called by Game when the Robot is created
        Returns:
    """
    def created(self):
        # Initialize qTable for every position possible
        self.qTable = [[0 for i in range(self.getRoomSize())] for i in range(self.getRoomSize())]
        # Create a list of actions/rewards for each possible state at each position (2)
        for row in range(self.getRoomSize()):
            for col in range(self.getRoomSize()):
                self.qTable[row][col] = [{action: 0 for action in self.getActions()}, {action: 0 for action in self.getActions()}]
        # Initialize starting state of the robot
        self.state = (self.getPosition()[0],self.getPosition()[1],self.hasLaundry())
        self.lastState = (self.getPosition()[0], self.getPosition()[1], self.hasLaundry())
        self.lastAction = ''
        self.reward = 0

        # Set the Q learning parameters
        self.alpha = .5
        self.gamma = .5
        self.epsilon = 1
        self.deltaEpsilon = .00001/self.getRoomSize()
        self.minEpsilon = .2

        # set variable to keep track of the robot's score
        self.score = [self.getScore()]

    """
        Function:   printQ
        Params:     
        Purpose:    called to print out the Q table based on each state
        Returns:    
    """
    def printQ(self):
        for row in range(self.getRoomSize()):
            for col in range(self.getRoomSize()):
                # For each state in each position, print its action/reward table
                print((row,col,'No Laundry'),self.qTable[row][col][False])
                print((row, col, 'Has Laundry'), self.qTable[row][col][True])

    """
        Function:   prettyPrintQ
        Params:     
        Purpose:    visually print the best possible action found onto the map for each state
        Returns:    
    """
    def prettyPrintQ(self):
        print('No Laundry')
        for row in range(self.getRoomSize()):
            for col in range(self.getRoomSize()):
                actions = self.qTable[row][col][False]
                # Get the action for this state that gives the best reward
                action = max(actions, key=actions.get)
                if action == 'left':        print('<', end=' ')
                elif action == 'right':     print('>', end=' ')
                elif action == 'up':        print('^', end=' ')
                elif action == 'down':      print('v', end=' ')
                elif action == 'collect':   print('o', end=' ')
                elif action == 'place':     print('x', end=' ')
            print()
        print('Has Laundry')
        for row in range(self.getRoomSize()):
            for col in range(self.getRoomSize()):
                # Get the action for this state that gives the best reward
                actions = self.qTable[row][col][True]
                action = max(actions, key=actions.get)
                if action == 'left':        print('<', end=' ')
                elif action == 'right':     print('>', end=' ')
                elif action == 'up':        print('^', end=' ')
                elif action == 'down':      print('v', end=' ')
                elif action == 'collect':   print('o', end=' ')
                elif action == 'place':     print('x', end=' ')
            print()

    """
        Function:   getAction (Overridden)
        Params:     
        Purpose:    called by Game, requests action from the Robot
        Returns:    action (string from action list in getActions)
    """
    def getAction(self):
        # Lower Epsilon over time so that it starts to exploit rather than wander
        self.epsilon -= self.deltaEpsilon if self.epsilon > self.minEpsilon else 0
        if random.randint(0,100)/100 < self.epsilon:
            # Random action
            action = random.choice(self.getActions())
            """
            # Uncomment/Comment this chunk to allow for bounds checking(will slightly increase learning rate)
            while (action=='left' and self.getPosition()[1] <= 0) or (action=='right' and self.getPosition()[1] >= self.getRoomSize()-1) or \
                (action=='up' and self.getPosition()[0] <= 0) or (action=='down' and self.getPosition()[0] >= self.getRoomSize()-1):
                action = random.choice(self.getActions())
            """
            return action
        # If not wandering, get the best weighted action from this state and do it
        actions = self.qTable[self.state[0]][self.state[1]][self.state[2]]
        return max(actions, key=actions.get)

    """
        Function:   rewarded (Overridden)
        Params:     action (string), reward (double)
        Purpose:    called by Game, gives the reward for the last executed action
        Returns:    
    """
    def rewarded(self, action, reward):
        # Update our last state so that it can be used in the Q-Calculation
        self.lastState = (self.getPosition()[0], self.getPosition()[1], self.hasLaundry())
        self.lastAction = action
        self.reward = reward
        self.score.append(self.getScore())

    """
        Function:   updated (Overridden)
        Params:     
        Purpose:    called by Game at the end of the turn, means that the Robot's state is fully updated
        Returns:    
    """
    def updated(self):
        # Update our present state so that it can be used in the Q-Calculation
        self.state = (self.getPosition()[0], self.getPosition()[1], self.hasLaundry())

        # Q(lastState,action) = (1-alpha)*Q(lastState,action) + alpha*(reward+gamma*max(Q(state,anyAction)))
        self.qTable[self.lastState[0]][self.lastState[1]][self.lastState[2]][self.lastAction] = \
            (1-self.alpha) * self.qTable[self.lastState[0]][self.lastState[1]][self.lastState[2]][self.lastAction] + \
            self.alpha * (self.reward + self.gamma * max(list(self.qTable[self.state[0]][self.state[1]][self.state[2]].values())))

    """
        Function:   finished (Overridden)
        Params:     
        Purpose:    called by Game when the Game has finished (gone through all iterations)
        Returns:    
    """
    def finished(self):
        # Print out Q-Table, visual best action per state and a plot of the score vs iteration
        self.printQ()
        self.prettyPrintQ()
        plt.plot(range(len(self.score)),self.score)
        plt.show()