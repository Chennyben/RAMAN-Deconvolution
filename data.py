'''
Class dealing with the Raman data

'''
import numpy as np
import matplotlib.pyplot as plt

class DATA:
	def __init__(self):
		#constructor
		super(DATA, self).__init__()
		self.X = 0
		self.Y = 0
		self.baseline = 0
		self.noBaseline =0
		self.bsDegree = 0
		self.bsCoef = 0
		self.spikes=[]

	def loadData(self, path):
		#load data
		try:
			dt = np.loadtxt(path, skiprows =10)
		except OSError:
			print("File not found")
			return
		self.X = dt[:,0]
		self.Y = dt[:,1]

	def setLimits(self, limits):
		#set the limits for the loaded data and crop it
		if self.X[0]>limits.min:
			limits.min=self.X[0]
		if self.X[-1]<limits.max:
			limits.max=self.X[-1]
		low = np.argwhere(self.X>limits.min)[0][0]
		high = np.argwhere(self.X<limits.max)[-1][0]
		self.X = self.X[low:high]
		self.Y = self.Y[low:high]

	def fitBaseline(self, degree, limits):
		#Select the part without Raman peaks and fit a polynomial function
		self.limits = limits
		baselineX = np.append(self.X[:np.argwhere(self.X>self.limits.min)[0][0]],
			self.X[np.argwhere(self.X>self.limits.max)[0][0]:])
		baselineY = np.append(self.Y[:np.argwhere(self.X>self.limits.min)[0][0]],
			self.Y[np.argwhere(self.X>self.limits.max)[0][0]:])
		self.bsDegree = degree
		self.bsCoef = np.polyfit(baselineX,baselineY, self.bsDegree)
		fit = np.poly1d(self.bsCoef)
		self.baseline = fit(self.X)
		self.noBaseline = abs(self.Y-self.baseline)


	def plotBaseline(self):
		#plot the baseline and spikes
		plt.close("all")
		fig = plt.figure(figsize=(12,8))
		ax = fig.add_subplot(111)
		ax.plot(self.X, self.Y, label = 'Experimental data')
		if len(self.spikes):
			ax.plot(self.X[self.spikes], self.Y[self.spikes], 'ro', label='Spikes')
		ax.plot(self.X, self.baseline, 'r--', label = 'Baseline')
		ax.plot([self.limits.min, self.limits.min], [min(self.Y), max(self.Y)], 'r-')
		ax.plot([self.limits.max,self.limits.max],[min(self.Y), max(self.Y)], 'r-', label='Excluded region')
		ax.set_ylabel("Intensity")
		ax.set_xlabel("Raman shift, $cm^{-1}$")
		plt.legend()
		plt.grid()
		plt.tight_layout()
		plt.show(block=False)
		return fig

	def detectSpikes(self, threshold):
		#detect spikes
		self.spikes=[]
		for i in np.arange(0, len(self.Y)-2):
			previous = np.mean([self.Y[i], self.Y[i+1]])
			current = np.mean([self.Y[i+1], self.Y[i+2]])
			if abs(previous-current)/current>threshold:
				self.spikes= np.append(self.spikes, [i, i+1, i+2]).astype(int)
				self.spikes = np.unique(self.spikes)

	def removeSpikes(self):
		#remove spikes
		print("Removing the spikes")
		self.X = np.delete(self.X, self.spikes)
		self.Y = np.delete(self.Y, self.spikes )
		self.baseline= np.delete(self.baseline, self.spikes)
		self.noBaseline = np.delete(self.noBaseline, self.spikes)

