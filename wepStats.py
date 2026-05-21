import random
import pygame
from pygame import mixer

from pprint import pprint
from inspect import getmembers
from types import FunctionType

#from pygamelib import engine, board_items
#from pygamelib.assets import graphics 
#from pygamelib.gfx import core
import time
from itertools import cycle

class Gatling:
	def __init__(self):
		self.name = 'Gatling'
		self.desc = 'High power kinetic weapon designed by Nerv corp.'
		self.draw = [']),,___,', '\\UV=//']
		self.types = ['kinetic']

		self.maxDamage = 100
		self.rawDamage = random.randint(1, self.maxDamage)

		if 'kinetic' in self.types:
			self.kDamage = self.rawDamage/(len(self.types))
		else:
			self.kDamage = 0
		if 'explosive' in self.types:
			self.eDamage = self.rawDamage/(len(self.types))
		else:
			self.eDamage = 0
		if 'thermal' in self.types:
			self.tDamage = self.rawDamage/(len(self.types))
		else:
			self.tDamage = 0

		self.maxAP = 20 
		self.AP = random.randint(1, self.maxAP)

		self.maxCritC = 50
		self.critC = random.randint(1, self.maxCritC)

		self.maxCritD = 2
		#self.critD = (1 / 100) * random.randint(0, (self.maxCritD * 100))
		self.critD = round(random.uniform(1, self.maxCritD), 2)
		
		self.shots =  random.randint(2, 3)

def wepStats(obj):
	print(obj.name)
	print(obj.desc)
	print('-'*15)
	print(f'Damage Types:	{obj.types}')
	print(f'Raw Damage: 	{obj.rawDamage}/{obj.maxDamage}')
	print()
	print(f'Kinetic DMG: 	{obj.kDamage}')
	print(f'Explosive DMG:	{obj.eDamage}')
	print(f'Thermal DMG:	{obj.tDamage}')
	print()
	print(f'Armor Piercing:	{obj.AP}/{obj.maxAP}')
	print()
	print(f'Crit Chance:	{obj.critC}/{obj.maxCritC}')
	print(f'Crit Damage:	{obj.critD}/{obj.maxCritD}')
	print()
	print(f'Shots Ammount:	{obj.shots}')
	print()

heads = ['  /R','  /@','  /7','  /#']
cores = [[' []0[]',' \\I|I/','  TIT'], [' ()1()',' \\\\;//','  T@T'], [' {}2{}',' \\\\[(/','  \\^/'], [' []3[]',' \\[I]/','  |T|']]
legs = [[' [] []', ' )) ))', ' :L :L'], [' []^[]', ' }} }}', ' /l /l'], [' []^[]', ' )) ))', ' \'l \'l'], [' [] []', ' }} }}', ' `L `L']]


mechchoice = [2, 1, 1]




gun1 = Gatling()
#wepStats(gun1)
#print_attributes(obj)

print()
print(heads[mechchoice[0]])
print(f'{cores[mechchoice[1]][0]}{gun1.draw[0]}\n{cores[mechchoice[1]][1]}{gun1.draw[1]}\n{cores[mechchoice[1]][2]}')
print(f'{legs[mechchoice[2]][0]}\n{legs[mechchoice[2]][1]}\n{legs[mechchoice[2]][2]}')



'''   
  /R       
 []0[]     
 \I|I/     
  TIT      
 [] []     
 )) ))     
 :L :L     

   /@
 ()1()
 \\;//
  T@T
 [] []   
 }} }}   
 /l /l

  /7               
 {}2{}     
 \\[(/     
  \^/      
 [] []     
 )) ))     
 'l 'l     

   /#        
 []3[]
 \[I]/
  |T|
 [] []
 }} }}
 `L `L
'''