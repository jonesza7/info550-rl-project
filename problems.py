'''
This file will contain your the code for your problems. 
'''

import numpy as np
import cv2
import time
import random
from collections import deque


moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def stepCell(cell, move):
   dr, dc = moves[move]
   return (cell[0] + dr, cell[1] + dc)


def manhattan(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Gridworld:
   """n x n grid where state is agent's cell with row,col"""

   def __init__(self, size=8, obstacleDensity=0.15, seed=0, stepReward=-0.01, goalReward=1.0):
      self.size = size
      self.start = (0, 0)
      self.goal = (size - 1, size - 1)
      self.stepReward = stepReward
      self.goalReward = goalReward
      self.maxSteps = 4 * size * size
      self.obstacles = self.makeObstacles(obstacleDensity, random.Random(seed))
      self.state = self.start

   def inBounds(self, cell):
      return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size
   
   def isOpen(self, cell):
      return self.inBounds(cell) and cell not in self.obstacles

   def pathExists(self, obstacles):
      seen = {self.start}
      queue = deque([self.start])

      while queue:
         cell = queue.popleft()
         if cell == self.goal:
            return True
         
         for move in moves:
            nxt = stepCell(cell, move)
            if self.inBounds(nxt) and nxt not in obstacles and nxt not in seen:
               seen.add(nxt)
               queue.append(nxt)
      return False
   
   def makeObstacles(self, density, rng):
      cells = [(r, c) for r in range(self.size) for c in range(self.size)
               if (r, c) not in (self.start, self.goal)]
      cnt = int(density * self.size * self.size)
      while True:
         obstacles = frozenset(rng.sample(cells, cnt))
         if self.pathExists(obstacles):
            return obstacles

   def reset(self):
      self.state = self.start
      return self.state
   
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      return [move for move in moves if self.isOpen(stepCell(state, move))]

   def getSuccessor(self, move, state):
      return stepCell(state, move)
   
   def getReward(self, state, nextState):
      if nextState == self.goal:
         return self.goalReward
      return self.stepReward
   
   def isTerminal(self, state=None):
      if state is None:
         state = self.state
      return state == self.goal
   
   def doMove(self, move):
      nextState = self.getSuccessor(move, self.state)
      reward = self.getReward(self.state, nextState)
      self.state = nextState
      return reward
   
   def getScore(self, state=None):
      if state is None:
         state = self.state
      return 1 if state == self.goal else 0

   def showState(self,state=None):
      if state is None:
         state = self.state
      for r in range(self.size):
         row = []
         for c in range(self.size):
            cell= (r,c)
            if cell == state:
               row.append("A")
            elif cell == self.goal:
               row.append("G")
            elif cell in self.obstacles:
               row.append("#")
            else:
               row.append(".")
         print(" ".join(row))
      print()

class Snake:
    """n x n Snake; State is like (body, food, alive); body is a tuple of cells and head first."""

    def __init__(self, size=5, seed=0, foodReward=1.0, deathReward=-1.0, stepReward=-0.01):
        self.size = size
        self.foodReward = foodReward
        self.deathReward = deathReward
        self.stepReward = stepReward
        self.maxSteps = 20 * size * size
        self.rng = random.Random(seed)
        self.reset()

    def inBounds(self, cell):
        return 0 <= cell[0] < self.size and 0 <= cell[1] < self.size

    def placeFood(self, body):
        free = [(r, c) for r in range(self.size) for c in range(self.size) if (r, c) not in body]
        return self.rng.choice(free) if free else None

    def reset(self):
        mid = self.size // 2
        body = ((mid, mid), (mid, mid - 1))
        self.state = (body, self.placeFood(body), True)
        return self.state

    def nextBody(self, body, food, move):
        head = stepCell(body[0], move)
        if head == food:
            return (head,) + body
        return (head,) + body[:-1]

    def isFatal(self, body, food, move):
        head = stepCell(body[0], move)
        if not self.inBounds(head):
            return True
        blocking = set(body) if head == food else set(body[:-1])
        blocking.add(body[1])
        return head in blocking

    def getLegalMoves(self, state=None):
        if state is None:
            state = self.state
        body, food, alive = state
        safe = [move for move in moves if not self.isFatal(body, food, move)]
        return safe if safe else list(moves)

    def getSuccessor(self, move, state):
        body, food, alive = state
        if self.isFatal(body, food, move):
            return (body, food, False)
        newBody = self.nextBody(body, food, move)
        if newBody[0] == food:
            food = self.placeFood(newBody)
        return (newBody, food, True)

    def getReward(self, state, nextState):
        if not nextState[2]:
            return self.deathReward
        if len(nextState[0]) > len(state[0]):
            return self.foodReward
        return self.stepReward

    def isTerminal(self, state=None):
        if state is None:
            state = self.state
        body, food, alive = state
        return not alive or food is None

    def doMove(self, move):
        nextState = self.getSuccessor(move, self.state)
        reward = self.getReward(self.state, nextState)
        self.state = nextState
        return reward

    def getScore(self, state=None):
        if state is None:
            state = self.state
        return len(state[0]) - 2

    def showState(self, state=None):
        if state is None:
            state = self.state
        body, food, alive = state
        for r in range(self.size):
            row = []
            for c in range(self.size):
                cell = (r, c)
                if cell == body[0]:
                    row.append("H" if alive else "X")
                elif cell in body:
                    row.append("o")
                elif cell == food:
                    row.append("*")
                else:
                    row.append(".")
            print(" ".join(row))
        print()

class Game:
    def __init__(self, problem, pZero, pOne,verbose=True):
      self.problem = problem      
      self.players = [pZero,pOne]   
      self.verbose = verbose   
      if self.verbose:
         self.problem.showState()               
    def playGame(self):
      pCur=0
      while self.problem.isTerminal()==False:
         move = self.players[pCur].getMove(self.problem)           
         self.problem.doMove(move)
         if self.verbose:
            self.problem.showState()
            print(f"Move {self.problem.ticks}:")
            print(self.problem.state)
         pCur = np.abs(pCur-1)
        
      wIndex = self.problem.getWinner()
      winner = self.players[wIndex]
      if wIndex == -1:
         winner = "DRAW"
      #display final state
      print(f"The Winner is {winner} ({wIndex})!")
      if self.verbose:
         self.problem.showState(4000)
      return wIndex

class SinglePlayerGame:
   "Runs one game of a 1 player problem (gridworld or snake)"

   def __init__(self, problem, player, verbose=True, maxMoves=None, delay=0.0, stopAtScore=None):
      self.problem = problem
      self.player = player
      self.verbose = verbose
      self.maxMoves = maxMoves if maxMoves is not None else problem.maxSteps
      self.delay = delay
      self.stopAtScore = stopAtScore

   def playGame(self):
      self.problem.reset()
      totalReward = 0.0
      moves = 0
      if self.verbose:
         self.problem.showState()
      while not self.problem.isTerminal() and moves < self.maxMoves:
         if self.stopAtScore is not None and self.problem.getScore() >= self.stopAtScore:
            break
         move = self.player.getMove(self.problem)
         move = self.player.getMove(self.problem)
         totalReward += self.problem.doMove(move)
         moves += 1
         if self.verbose:
            print(f"Move {moves}: {move}")
            self.problem.showState()
            time.sleep(self.delay)
      score = self.problem.getScore()
      if self.verbose:
         print(f"{self.player} finished after {moves} moves. Score {score}, total reward: {totalReward:.2f}")
      return score, totalReward, moves



class TicTacToe:
   def __init__(self):
      self.state = np.zeros((3,3))      
      self.ticks=-1      
   def getLegalMoves(self, state=None):
      if state is None:
         state = self.state
      moves = []
      mark = 1
      if np.sum(np.abs(state))%2!=0:
         mark = -1       
      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==0:
               moves.append((mark,(i,j)))
      return moves             
   def getSuccessor(self, move, state):
      mark = move[0]
      loc = move[1]
      state[loc] = mark
      return state
   def doMove(self,move):
      self.state = self.getSuccessor(move,self.state)
      self.ticks+=1
   def isTerminal(self, state=None):
      if state is None:
         state = self.state         
      terminal = False
      val = self.evalTerminal(state)      
      if val ==0 and np.sum(np.abs(state))==9:
         terminal = True
      if val!=0:
         terminal = True
      return terminal
   def evalTerminal(self, state=None):
      if state is None:
         state = self.state
      val = 0      
      
      pZeroWins = [np.max(np.sum(state,0))==3,np.max(np.sum(state,1))==3,np.trace(state)==3,np.trace(state[:,::-1])==3]
      pOneWins = [np.min(np.sum(state,0))==-3,np.min(np.sum(state,1))==-3,np.trace(state)==-3,np.trace(state[:,::-1])==-3]

      if np.any(pZeroWins):
         val = 1
      if np.any(pOneWins):
         val = -1
      return val
   def getWinner(self, state=None):
      if state is None:
         state = self.state
      val = self.evalTerminal(state)
      if val==1:
         return 0 
      elif val==-1:
         return 1
      else:
         return -1
   def showState(self, ms = 1000,state=None):
      if state is None:
         state = self.state  

      screen = np.zeros((150,150)).astype(np.uint8)         
      screen = cv2.line(screen,(0,49),(149,49),255) 
      screen = cv2.line(screen,(0,99),(149,99),255)
      screen = cv2.line(screen,(49,0),(49,149),255) 
      screen = cv2.line(screen,(99,0),(99,149),255)

      for i in range(state.shape[0]):
         for j in range(state.shape[1]):
            if state[i,j]==1:
               screen = cv2.line(screen,(5 +j*50,5+i*50),(44+j*50,44+i*50),255,2,cv2.LINE_AA) 
               screen = cv2.line(screen,(44+j*50,5+i*50),(5 +j*50,44+i*50),255,2,cv2.LINE_AA) 
            if state[i,j]==-1:
               screen = cv2.circle(screen, (25 +j*50,25+i*50), 20, 255, 2,cv2.LINE_AA) 
               
      cv2.imshow('TicTacToe',screen)
      cv2.waitKey(ms)
