
from cmath import inf
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):
    #print(gameState.getNumAgents())
    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)



class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def maxagent(self, gameState, depth):
    canbe = gameState.getLegalActions(0)
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    ret = [None, -inf]
    for dir in canbe:
      successor = gameState.generateSuccessor(0, dir)
      succinfo = self.minagent(successor, depth, 1)
      if ret[1] < succinfo[1]:
        ret[0] = dir
        ret[1] = succinfo[1]
    #print("max", ret[0])
    return ret

  def minagent(self, gameState, depth, agentidx):
    canbe = gameState.getLegalActions(agentidx)

    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    ret = [None, inf]
    for dir in canbe:
      successor = gameState.generateSuccessor(agentidx, dir)
      agentnum = gameState.getNumAgents()
      if agentidx == agentnum-1:
        succinfo = self.maxagent(successor, depth+1)
      else:
        succinfo = self.minagent(successor, depth, agentidx+1)
      if ret[1] > succinfo[1]:
        ret[0] = dir
        ret[1] = succinfo[1]
    #print("min", ret[0])
    return ret

  def Action(self, gameState):
  ####################### Write Your Code Here ################################
    ret = self.maxagent(gameState, 0)
    return ret[0]

    raise Exception("Not implemented yet")
    ############################################################################




class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBetaAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def maxagent(self, gameState, depth, alpha, beta):
    canbe = gameState.getLegalActions(0)
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    ret = [None, -inf]
    for dir in canbe:
      successor = gameState.generateSuccessor(0, dir)
      succinfo = self.minagent(successor, depth, 1, alpha, beta)
      if ret[1] < succinfo[1]:
        ret[0] = dir
        ret[1] = succinfo[1]
        if ret[1] > alpha:
          alpha = ret[1]
        if ret[1] >= beta:
          return ret
    #print("max", ret[0])
    return ret

  def minagent(self, gameState, depth, agentidx, alpha, beta):
    canbe = gameState.getLegalActions(agentidx)

    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    ret = [None, inf]
    for dir in canbe:
      successor = gameState.generateSuccessor(agentidx, dir)
      agentnum = gameState.getNumAgents()
      if agentidx == agentnum-1:
        succinfo = self.maxagent(successor, depth+1, alpha, beta)
      else:
        succinfo = self.minagent(successor, depth, agentidx+1, alpha, beta)
      if ret[1] > succinfo[1]:
        ret[0] = dir
        ret[1] = succinfo[1]
        if ret[1] < beta:
          beta = ret[1]
        if ret[1] <= alpha:
          return ret
    #print("min", ret[0])
    return ret

  def Action(self, gameState):
  ####################### Write Your Code Here ################################
    ret = self.maxagent(gameState, 0, -inf, inf)
    return ret[0]

    raise Exception("Not implemented yet")
    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] ExpectimaxAgent의 Action을 구현하시오.
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def maxagent(self, gameState, depth):
    canbe = gameState.getLegalActions(0)
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    ret = [None, -inf]
    for dir in canbe:
      successor = gameState.generateSuccessor(0, dir)
      succinfo = self.minagent(successor, depth, 1)
      if ret[1] < succinfo[1]:
        ret[0] = dir
        ret[1] = succinfo[1]
    #print("max", ret[0])
    return ret

  def minagent(self, gameState, depth, agentidx):
    canbe = gameState.getLegalActions(agentidx)
    cnt = len(canbe)
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
      return [None, self.evaluationFunction(gameState)]

    sum = 0
    for dir in canbe:
      successor = gameState.generateSuccessor(agentidx, dir)
      agentnum = gameState.getNumAgents()
      if agentidx == agentnum-1:
        succinfo = self.maxagent(successor, depth+1)
      else:
        succinfo = self.minagent(successor, depth, agentidx+1)
      sum += succinfo[1]
    ret = [None, sum/cnt]
    return ret

  def Action(self, gameState):
  ####################### Write Your Code Here ################################
    ret = self.maxagent(gameState, 0)
    return ret[0]

    raise Exception("Not implemented yet")
    ############################################################################
