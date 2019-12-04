import json
import random 
import time
import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

# ====================================== #
# =========== LOGIN AND AUTH =========== #
# ====================================== #
br = RoboBrowser()
br.open('https://dragcave.net/')
form = br.get_form()
print('==================')
form['username'] = input('Username: ')
form['password'] = input('Password: ')
print('==================')
br.submit_form(form)

# =====================================#
# =========== MODE STARTUP =========== #
# =====================================#
f = open('eggpedia.json', 'r')
eggpedia = json.load(f)
f.close()

biome_codes = {
'Coast':'1',
'Desert':'2',
'Forest':'3',
'Jungle':'4',
'Alpine':'5',
'Volcano':'6'
}
biomes_choice = []

print('\n**Choose your dragons separated by comma (,)**')
choice = input("Here: ").split(',')

desired = {}
for breed in choice:
	desired[eggpedia['dragons'][breed]['description']] = breed
	for biome in eggpedia['dragons'][breed]['biomes']:
		if biome == "All Habitats":
			biomes_choice = [1,2,3,4,5,6]
		elif biome == "No Habitat":
			print("ERROR: {} is currently not found in any habitat.".format(breed))
		elif biome_codes[biome] not in biomes_choice:
			biomes_choice.append(biome_codes[biome])

biomes_left = list(biomes_choice)

# =========================================== #
# =========== H U N T E R STARTUP =========== #
# =========================================== #
while 1:
	if biomes_left == []:
		print("Biomes choice:", biomes_choice)
		biomes_left = list(biomes_choice)
		print("Reseting countdown!")
	
	if len(biomes_left) > 1:
		biome = biomes_left.pop(random.randrange(len(biomes_left)))
		print("Biomes choice:", biomes_choice)
		print("Biome chosen was {}, and now the list is {}".format(biome, biomes_left))
	
	elif len(biomes_left) == 1:
		biome = biomes_left.pop(0)
		print("Biomes choice:", biomes_choice)
		print("Biome chosen was {}, and now the list is {}".format(biome, biomes_left))
	
	br.open('https://dragcave.net/locations/' + str(biome))
	soup = BeautifulSoup(str(br.parsed()), "lxml")
	cave = (soup.find('div',class_='eggs')).findAll('div')

	# Searches for egg(s) in current biome.
	for egg in cave:
		eggLink = "https://dragcave.net" + egg.find("a").get('href')
		eggDescription = egg.find("span").text
		print(eggLink, eggDescription)

		# Catch dragon if it corresponds to desireds.
		if eggDescription in desired:
			br.open(eggLink)
			print("\n**{} FOUND**\n".format(desired[eggDescription]))
			desired.pop('key', None)
			
			# If dict empty, end the program.
			if desired ==  False:
				input("All desired dragons found, press enter to exit the program.")
				exit()

	time.sleep(random.randrange(2,10))