import numpy as np
import plot as pt
from Player import Player

class GameState:

	def __init__(self,p1,p2,n):
		self.n=n
		self.board =np.zeros((self.n,self.n))
		self.p1 = p1
		self.p2 = p2
		self.gameWonByp1 =0
		self.gameWonByp2 =0
		self.gameDraw=0
		self.isGameOver = False


	def giveAvailaibleOptions(self):
		options =[]
		l,b = self.board.shape
		for i in range(l):
			for j in range(b):
				if self.board[i][j]==0:
					options.append((i,j))
		return options

	def giveWinner(self):
		l,b=self.board.shape
		for i in range(l):
			rowsum=sum(self.board[i,:])
			if abs(rowsum)==3:
				self.isGameOver=True
				if rowsum==3:
					return 1
				else: 
					return -1
		for i in range(b):
			colsum=sum(self.board[:,i])
			if abs(colsum)==3:
				self.isGameOver=True
				if colsum==3:
					return 1
				else: 
					return -1
		sumdiagonal=sum([self.board[i, i] for i in range(l)])
		if abs(sumdiagonal)==3:
			self.isGameOver=True
			if sumdiagonal==3:
				return 1
			else: 
				return -1
		sumdiagonal=sum([self.board[i,l-i-1] for i in range(l)])
		if abs(sumdiagonal)==3:
			self.isGameOver=True
			if sumdiagonal==3:
				return 1
			else: 
				return -1
		if(len(self.giveAvailaibleOptions()))==0:
			self.isGameOver=True
			return 0
		return None

	def giveReward(self):
		winner = self.giveWinner()
		if winner == 1:
			self.p1.reward(1)
			self.p2.reward(-1)
			self.gameWonByp1 +=1
		elif winner ==-1:
			self.p1.reward(-1)
			self.p2.reward(1)
			self.gameWonByp2 +=1
		else :
			self.p1.reward(0.5)
			self.p2.reward(0.5)
			self.gameDraw +=1

	def showBoard(self):
		# player 1 is  x 
		# player 2 is  o
		l,b=self.board.shape
		for i in range(l):
			print('-------------')
			out = '| '
			for j in range(b):
				if self.board[i][j]==1:
				    token = 'x'
				elif self.board[i][j]==-1:
				    token = 'o'
				else :
				    token = ' '
				out += token + ' | '
			print(out)
		print('-------------')

	def reset(self):
		l,b=self.board.shape
		self.board=np.zeros((l,b))
		self.p1.reset()
		self.p2.reset()
		self.p1.stateSequence.append(str(self.board.reshape(l*b)))
		self.p1.stateSequence.append(str(self.board.reshape(l*b)))
		self.isGameOver=False

	def play(self,iterations,human,epsilon1,epsilon2):
		print('Training.......')
		stat=np.zeros((iterations,3))
		l,b=self.board.shape
		for i in range(iterations):
			self.reset()
			# print(i)
			# print(self.p1.stateValues)
			while(not self.isGameOver):
				#player1
				options =self.giveAvailaibleOptions()
				action = self.p1.makeAMove(options,self.board,epsilon1)
				self.board[action[0]][action[1]]=self.p1.id
				self.p1.stateSequence.append(str(self.board.reshape(l*b)))
				win=self.giveWinner()
				if win!=None:
					self.giveReward()
					self.p1.updateStateValues()
					self.p2.updateStateValues()
				else:
					#player2
					options =self.giveAvailaibleOptions()
					action = self.p2.makeAMove(options,self.board,epsilon2)
					self.board[action[0]][action[1]]=self.p2.id
					self.p2.stateSequence.append(str(self.board.reshape(l*b)))
					win=self.giveWinner()
					if win!=None:
						self.giveReward()
						self.p2.updateStateValues()
						self.p1.updateStateValues()

			stat[i][0]=self.gameWonByp1
			stat[i][1]=self.gameWonByp2
			stat[i][2]=self.gameDraw
			
		pt.plotLineGraph(stat,iterations)
		self.reset()
		# human=Player(-1,'Viswanathan Anand',0.5,0.9)
		# print(len(self.p1.stateValues))
		self.p2=human
		self.gameWonByp1 =0
		self.gameWonByp2 =0
		self.gameDraw=0
		play=True
		while play:
			print('Let\'s play mate .......')
			self.playwithHuman()
			s=input('Wanna play again ? (y/n) ')
			if not (s =='y'):
				play=False

		print('Thanks for playing !')


	def playwithHuman(self):
		print('Training.......')
		l,b=self.board.shape
		self.reset()
		self.showBoard()
		while(not self.isGameOver):
			#player1
			print(self.p1.name+ ' Bot makes a move')
			options =self.giveAvailaibleOptions()
			action = self.p1.makeAMove(options,self.board,0)
			self.board[action[0]][action[1]]=self.p1.id
			self.p1.stateSequence.append(str(self.board.reshape(l*b)))
			self.showBoard()
			win=self.giveWinner()
			if win!=None:
				if win==0:
					print('Draw, woah! It was a tough match')
				else:
					self.giveReward()
					self.p1.updateStateValues()
					print(self.p1.name+', the AI bot won.....This Bot is no ordinary')
			else:
				#player2 is human
				options =self.giveAvailaibleOptions()
				action = self.p2.humanMakeMove(options)
				self.board[action[0]][action[1]]=self.p2.id
				# self.p2.stateSequence.append(str(self.board.reshape(l*b)))
				win=self.giveWinner()
				self.showBoard()
				if win!=None:
					if win==0:
						print('Draw, woah! It was a tough match')
					else:
						self.giveReward()
						self.p1.updateStateValues()
						print(self.p2.name+' ...wow... U won')
						# self.p2.updateStateValues()
		print('Exiting the game')	