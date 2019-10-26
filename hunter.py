import json 							# Egg Dictionary
import random 							# More complex behavior
import time								# Delay functions
import requests							# Fetching
from bs4 import BeautifulSoup			# Parsing
from robobrowser import RoboBrowser 	# Authentication

# ====================================== #
# =========== LOGIN AND AUTH =========== #
# ====================================== #
br = RoboBrowser()
br.open('https://dragcave.net/')
form = br.get_form()
print('======================')
form['username'] = input('Type In your Username: ')
form['password'] = input('Type In your Password: ')
print('======================')
br.submit_form(form)

# =====================================#
# =========== MODE STARTUP =========== #
# =====================================#
f = open('eggpedia.json', 'r')
eggpedia = json.load(f)
f.close()

biomeCodes = {
'Coast':'1',
'Desert':'2',
'Forest':'3',
'Jungle':'4',
'Alpine':'5',
'Volcano':'6'
}
biomes_choice = []

print('\n**CHOOSE THE DRAGONS YOU WANT TO SEARCH FOR, SEPARATED BY SPACES**')
choice = input("Here: ").split(' ')

desired = {}
for breed in choice:
	desired[eggpedia['dragons'][breed]['description']] = breed
	for biome in eggpedia['dragons'][breed]['biomes']:
		if biomeCodes[biome] not in biomes_choice:
			biomes_choice.append(biomeCodes[biome])

biomes_left = biomes_choice

# =========================================== #
# =========== H U N T E R STARTUP =========== #
# =========================================== #
while 1:
	if biomes_left == []:
		biomes_left = biomes_choice
	if len(biomes_left)-1 != 0:
		biome = biomes_left.pop(random.randrange(0,len(biomes_left)-1))
	else:
		biome = biomes_left.pop(0)
	br.open('https://dragcave.net/locations/' + biome)
	soup = BeautifulSoup(str(br.parsed()), "lxml")
	cave = (soup.find('div',class_='eggs')).findAll('div')

	# Searches for egg(s) in current biome.
	for egg in cave:
		eggLink = "https://dragcave.net" + egg.find("a").get('href')
		eggDescription = egg.find("span").text
		print(eggLink, eggDescription)

		# Default case: Chosen dragons.
		if eggDescription in desired:
			br.open(eggLink)
			print("\n**{} FOUND**\nEnding program...".format(desired[eggDescription]))
			exit()

		# Special case 1: Leetle Tree
		if eggDescription == "Oh my. There is a Leetle Tree among the eggs.":
			br.open(eggLink)
			print("\n**LEETLE TREE FOUND**\nEnding program...")
			exit()
		# Special case 2: Chicken Egg
		if eggDescription == "This egg is much smaller than the others.":
			br.open(eggLink)
			print("\n**CHICKEN EGG FOUND**\nEnding program...")
			exit()

		# Default Case:

	
	time.sleep(random.randrange(2,6))