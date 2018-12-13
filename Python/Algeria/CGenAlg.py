""" 遗传算法测试 """
from types import MethodType
import random
import copy

g_rightPoint = 2
g_leftPoiont = -2
g_MaxPerturbation = 0.02

CGenome = {
	'weights':[],
	'fites':0
	}
	
def Function(self,x):
	return 8-(x-0.6)**2

class CGenAlg(object):
	""" 算法引擎 """
	vecPop = []
	popSize = 0
	chromoLength = 0
	
	__totalFitness = 0
	__bestFitness = 0
	__averageFitness = 0
	__worstFitness = 99999999
	__fittestGenome = 0
#	__generation = 0		#代数计数器

	mutationRate = 0.05		#基因突变概率
	crossoverRate = 0.7		#基因交叉概率

	def __init__(self,popSize,genLenght,mutationRate,crossoverRate):
		""" 类初始化 """
		self.popSize = popSize
		self.chromoLength = genLenght		
		self.mutationRate = mutationRate
		self.crossoverRate = crossoverRate
		self.vecPop.clear()
		
		for i in range(self.popSize):
			Pop = copy.deepcopy(CGenome)
			for j in range(self.chromoLength):
				Pop['weights'].append(random.uniform(g_leftPoiont,g_rightPoint))
			self.vecPop.append(Pop)
		
	def GetChromoRoulette(self):		#适应值偏向大值
		""" 轮盘赌函数 """
		Slice = random.uniform(0,self.__totalFitness)
		FitnessSoFar = 0
		theChosenOne = CGenome
		
		for i in range(self.popSize):
			FitnessSoFar += self.vecPop[i]['fites']
			if FitnessSoFar >= Slice:
				theChosenOne = self.vecPop[i]
				break
			theChosenOne = self.vecPop[-1]
		# print(theChosenOne)
		# print(FitnessSoFar)
		# print(self.__totalFitness)
		# print(Slice)
		return theChosenOne

	def CalculateBestWorstAvTot(self):
		self.__totalFitness = 0
		self.__bestFitness = self.vecPop[0]['fites']
		self.__worstFitness = self.vecPop[0]['fites']
		for pop in self.vecPop:
			self.__totalFitness += pop['fites']
			if pop['fites'] < self.__bestFitness:
				self.__bestFitness = pop['fites']
			if pop['fites'] > self.__worstFitness:
				self.__worstFitness = pop['fites']
		self.__averageFitness = self.__totalFitness / self.popSize
	
	def Reset(self):
		self.__totalFitness = 0
		self.__bestFitness = 0
		self.__averageFitness = 0
		self.__worstFitness = 99999999
		self.__fittestGenome = 0

	def CalculateFites(self,*chromo):		#未完成，仅可用于单基因引擎
		if chromo:
			for i in range(len(chromo)):
				input = chromo[i]['weights'][0]
				try:
					output = self.Function(input)
				except AttributeError:
					print('请绑定函数。')
					return
				chromo[i]["fites"] = output
		else:
			for i in range(len(self.vecPop)):
				input = self.vecPop[i]['weights'][0]
				try:
					output = self.Function(input)
				except AttributeError:
					print('请绑定函数。')
					return
				self.vecPop[i]["fites"] = output

	def Mutate(self,chromo):
		for i in range(len(chromo['weights'])):
			if random.uniform(0,1) < self.mutationRate:
				chromo['weights'][i] = chromo['weights'][i] + random.uniform(-1,1)*g_MaxPerturbation
				if chromo['weights'][i] < g_leftPoiont:
					chromo['weights'][i] = g_leftPoiont
				elif chromo['weights'][i] > g_rightPoint:
					chromo['weights'][i] = g_rightPoint
		self.CalculateFites(chromo)
					
	def Cross(self,Gendad,Genmum):
		pass

	def Epoch(self):
		""" 生成新种群方法 """
		self.Reset()
		self.CalculateFites()
		self.CalculateBestWorstAvTot()
		vecPopNext = []
		vecPopNext.clear()
		
		while len(vecPopNext) < self.popSize:
			Genmum = self.GetChromoRoulette()
			Gendad = self.GetChromoRoulette()
			baby1 = Genmum		#省略交叉基因步骤
			baby2 = Gendad		#省略交叉基因步骤
			
			self.Mutate(baby1)
			self.Mutate(baby2)
			vecPopNext.append(baby1)
			vecPopNext.append(baby2)
		
		if len(vecPopNext) != len(self.vecPop):		#代码作用存疑
			print('人口数目是单数。')
			return
		self.vecPop = vecPopNext[:]
		

#测试代码
testCGenALg = CGenAlg(180,1,0.05,0.7)
print(testCGenALg.vecPop)

testCGenALg.Function = MethodType(Function,CGenAlg)
for i in range(200):
	testCGenALg.Epoch()
	print('the %d`s range :'%(i))
	print(testCGenALg.vecPop)			#结果匹配用正则表达式：
	print()								#\S*\s\S(-?[0-9].[0-9]+)], 'fites': (-?[0-9].?[0-9]+)\S*
print('End')
