from MoveEnums import Moves
from board import Board, Snake, Pos
import random
import math

class Game:
  def __init__(self, board, you):
    self.board = Board(board)
    self.me = Snake(you)

  def get_move_str(self, moves: Moves):
    direction = None
    if Moves.UP == moves:
      direction =  "up"
    if Moves.DOWN == moves:
      direction =  "down"
    if Moves.LEFT == moves:
      direction =  "left"
    if Moves.RIGHT == moves:
      direction =  "right"
    return direction
 
  def move(self):
    m, s = self.logic()
    return {"move": self.get_move_str(m), "shout":s}


  def logic(self):
    print(self.me.head)
    choices = list(Moves)
    while True:
      new_direction = random.choice(choices)
      print(f"new direction is {new_direction.name}")
      new_pos = self.getNewPos(new_direction)
      is_safe = self.isNewPosSafe(new_pos)
      if is_safe or len(choices) == 1:
        break
      else:
        choices.remove(new_direction)
    return (new_direction, "Hi!")

  def getNewPos(self, new_direction: Moves):
    new_pos = None
    if new_direction.name == Moves.UP.name:
      new_pos = Pos(self.me.head.x, self.me.head.y + 1)
    elif new_direction.name == Moves.DOWN.name:
      new_pos = Pos(self.me.head.x, self.me.head.y - 1)
    elif new_direction.name == Moves.RIGHT.name:
      new_pos = Pos(self.me.head.x + 1, self.me.head.y)
    elif new_direction.name == Moves.LEFT.name:
      new_pos = Pos(self.me.head.x - 1, self.me.head.y)
    return new_pos

  def getNewPosFrom(self, pos: Pos, new_direction: Moves):
    new_pos = None
    if new_direction.name == Moves.UP.name:
      new_pos = Pos(pos.x, pos.y + 1)
    elif new_direction.name == Moves.DOWN.name:
      new_pos = Pos(pos.x, pos.y - 1)
    elif new_direction.name == Moves.RIGHT.name:
      new_pos = Pos(pos.x + 1, pos.y)
    elif new_direction.name == Moves.LEFT.name:
      new_pos = Pos(pos.x - 1, pos.y)
    return new_pos

  def isOutOfBounds(self, new_pos):
    outOfBounds = True
    if new_pos.x <= self.board.width-1 and new_pos.x >= 0 and new_pos.y <= self.board.height-1 and  new_pos.y >= 0:
      outOfBounds = False
    return outOfBounds

  def isOccupiedBySnake(self, new_pos):
    snakeThere = False
    for s in self.board.snakes:
      for b in s.body[:-1]:
          if new_pos.x == b.x and new_pos.y == b.y:
            snakeThere = True
            if snakeThere:
              break
    return snakeThere


  def isOccupiedByHazard(self, new_pos):
    hazardThere = False
    for h in self.board.hazards:
      if new_pos.x == h.pos.x and new_pos.y == h.pos.y:
        hazardThere = True
    return hazardThere

  def doesNewSquareHaveEscapeRoute(self, new_pos):
    escape_route = False
    square_around_new_pos = []
    square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.RIGHT))
    square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.LEFT))
    square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.UP))
    square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.DOWN))
    potential_problems = {}
    for s in square_around_new_pos:
      potential_problems[s] = self.isOccupiedByHazard(s)
      if not potential_problems[s]:
        potential_problems[s] = self.isOccupiedBySnake(s)
        if not potential_problems[s]:
          potential_problems[s] = self.isOutOfBounds(s)
        
    for key,value in potential_problems.items():
      print(f"doesNewSquareHaveEscapeRoute: {key} == {value}")
      if value == False:
        escape_route = True
        break
    return escape_route
  
  def isNewPosSafe(self, new_pos):
    print(f"checking position {new_pos}")
    posNotSafe = False
    posNotSafe = self.isOutOfBounds(new_pos)
    print(f"isOutofBounds {posNotSafe}")
    if posNotSafe == False:
      posNotSafe = self.isOccupiedBySnake(new_pos)
      print(f"isOccupiedBySnake {posNotSafe}")
      if posNotSafe == False:
        posNotSafe = self.isOccupiedByHazard(new_pos)
        print(f"isOccupiedByHazard {posNotSafe}")
        if posNotSafe == False:
          posNotSafe = not self.doesNewSquareHaveEscapeRoute(new_pos)
          print(f"doesNewSquareHaveEscapeRoute {posNotSafe}")
          # if posNotSafe == False we have an escape route 
    return not posNotSafe
  
  def isNewPosSafeThinkTank(self, new_pos):
    is_pos_safe = self.isNewPosSafe(new_pos)
    if is_pos_safe:
      square_around_new_pos = []
      square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.RIGHT))
      square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.LEFT))
      square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.UP))
      square_around_new_pos.append(self.getNewPosFrom(new_pos, Moves.DOWN))
      square_safety = {}
      for s in square_around_new_pos: 
        square_safety[s]=  self.isNewPosSafe(new_pos)

      for key,value in square_safety.items():
        print(f"isNewPosSafeThinkTank: {key} == {value}")
        if value == False:
          is_pos_safe = True
          break
    return is_pos_safe
    
    def EAT(self):
      distX = 100000000000000
      distY = 100000000000000
      for food in self.board.food:
          print(food)
          tmpdistX = abs(food.pos.x - self.me.head.x)
          tmpdistY = abs(food.pos.y - self.me.head.y)
          if abs(math.sqrt(tmpdistX + tmpdistY)) < abs(math.sqrt(distX + distY)):
            distX = tmpdistX
            distY = tmpdistY
            print("closer food found")
            self.closestFood = food

      distX = 100000000000000
      distY = 100000000000000
      for mmove in self.listOfLegalMove:
          print(mmove)
          newPos = self.findPoint(mmove)

          tmpdistX = abs(self.closestFood['x'] - newPos[0])
          tmpdistY = abs(self.closestFood['y'] - newPos[1])

          if abs(math.sqrt(tmpdistX + tmpdistY)) < abs(math.sqrt(distX + distY)):
            distX = tmpdistX
            distY = tmpdistY
            print("better move found")
            self.bestMove = mmove