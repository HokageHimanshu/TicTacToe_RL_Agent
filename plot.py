import numpy as np
import matplotlib.pyplot as plt

def plotLineGraph(stat,iterations):
	x = np.arange(iterations)
	plt.plot(x,stat[:,0])
	plt.plot(x,stat[:,1])
	plt.plot(x,stat[:,2])
	plt.legend([str(stat[-1,0])+' Games Won By Bot 1', str(stat[-1,1])+' Games Won By Bot 2', str(stat[-1,2])+' Games Draw'], loc='upper left')
	plt.suptitle('Training of Bot 1 (playing with bot 2)')
	plt.title('Training after '+str(iterations)+' iterations')
	plt.savefig("TrainingHistory.png") # save as png
	plt.show()