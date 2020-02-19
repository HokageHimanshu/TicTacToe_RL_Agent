import numpy as np

class Player:

	def __init__(self,id,name,learningRate,decay_gamma):
		self.id=id
		self.name=name
		self.stateSequence=[]
		self.stateValues={}
		self.learningRate=learningRate
		self.decay_gamma=decay_gamma
		self.rewardVal=0

	def humanMakeMove(self,availaiblePos):
		rightAction=True
		while rightAction:
			x = int(input('Enter row(0,1,2) = '))
			y = int(input('Enter col(0,1,2) = '))

			if (x,y) in availaiblePos:
				rightAction=False
			else:
				print('Invalid Move.....Enter Again')
		return (x,y)

	def reward(self,reward):
		self.rewardVal=reward

	def makeAMove(self,availaiblePos,board,epsilon):
		if np.random.uniform(0,1)<=epsilon:
			idx =np.random.choice(len(availaiblePos))
			action=availaiblePos[idx]
		else:
			maxvalue=0
			action=availaiblePos[0]
			l,b=board.shape
			for x,y in availaiblePos:
				tempBoard = board.copy()
				tempBoard[x,y]=self.id
				key=str(tempBoard.reshape(l*b))
				value =self.stateValues.get(key)
				if value!=None and value>maxvalue:
					maxvalue=value
					action = (x,y)
		return action

	def reset(self):
		self.stateSequence=[]

	def updateStateValues(self):
		l = len(self.stateSequence)
		sv = 0
		reward=self.rewardVal
		for i in range(l):
			s = self.stateSequence[l-i-1]
			if self.stateValues.get(s) is None:
				self.stateValues[s]=0
			self.stateValues[s] +=self.learningRate *(self.decay_gamma * reward - self.stateValues[s])
			reward = self.stateValues[s]