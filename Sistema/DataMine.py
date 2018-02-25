from collections import Counter
from itertools import combinations
from itertools import count
from math import log
import re

def init_pass(T):
	print("init_pass")
	tipos = set()
	numLine = 0
	for line in T:
		tipos = tipos.union(set(line.split()))
		numLine += 1
	T.seek(0)
	return list(tipos), numLine

def countTokens(T):
	tf = dict()
	idf = dict()

	print("countTokens")
	wordCount = Counter()
	docCount = Counter()
	for line in T:
		for token in line.split():
			wordCount[token] += 1
		if token in line.split():
			docCount[token] += 1


	for token in docCount:
		if docCount[token] >= 200 or docCount[token] < 5:
			del wordCount[token]
	return wordCount

def sup(xuy, n=None):
	if n == None:
		return xuy
	return xuy/n

def candidate_gen(Fk, k):
	for f in combinations(Fk, 2):
		c = f[0].union(f[1])
		for i in combinations(list(c), k):
			if set(i) not in Fk:
				break
		else:
			yield frozenset(c)

def apriori(archivo, support=sup, MAX_K=-1):
	with open(archivo, "r", encoding="utf8") as T:
		F = list()
		F_datos = list()
		k = 1
		c, total = init_pass(T)
		wordCount = countTokens(T)
		finalCand = set()
		for f in c:
			if support(wordCount[f], total) < MIN_SUPPORT:
				c.pop(c.index(f))
				del wordCount[f]
		F.append(c)
		for f in F[0]:
			F[0][F[0].index(f)] = {f}
		F_datos.append(list(wordCount.items()))
		#Empezamos con el while
		while F[-1] and k < MAX_K:
			wordCount = Counter()
			c = candidate_gen(F[-1], k)
			print("Contando candidatos...")
			for candidate in c:
				if candidate not in wordCount:
					T.seek(0)
					for transaction in T:
						if candidate.issubset(set(transaction.split())):
							wordCount[candidate] += 1
			print("terminamos transacciones")
			c = list(wordCount.keys())
			for f in c:
				if support(wordCount[f], total) < MIN_SUPPORT:
					del wordCount[f]
			F.append(list(wordCount.keys()))
			F_datos.append(list(wordCount.items()))
			k += 1
	print("Fin!---------------")
	return F, F_datos

def aprioryDB(tokens, data, support=sup, MAX_K=1):
	tokenCount = len(tokens)
	
