import numpy as np
from TicTacToe import GameState
from Player import Player


# board = np.zeros((3,3))
iterations =10000
learningRate1=0.5
learningRate2=0.5
decayRate1=0.9
decayRate2=0.9
epsilon1=0.4
epsilon2=0.4

p1=Player(1,'Himanshu',learningRate1,decayRate1)
p2=Player(-1,'Vinod',learningRate2,decayRate2)
# learning rate and decay rate is rate is irrelevant here 
human=Player(-1,'Viswanathan Anand',0,0)
g = GameState(p1,p2,3)
g.play(iterations,human,epsilon1,epsilon2)