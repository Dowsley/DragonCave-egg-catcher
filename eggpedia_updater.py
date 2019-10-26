import json
import requests
from bs4 import BeautifulSoup

index = 0
FORBIDDEN = [36, 37, 51, 52, 95, 96, 97, 110, 111, 112, 130, 131, 133, 134, 155, 156, 157, 158, 159, 160, 162]
dic = {"year-round":{}, "two-headed":{}, "pygmies":{}, "drakes":{}, "non-dragons":{}}
json_categories = ["year-round", "two-headed", "pygmies", "drakes", "non-dragons"]

link = 'https://dragcave.fandom.com/wiki/Which_egg_is_which%3F'
soup = BeautifulSoup(requests.get(link).text, "lxml")
tables = soup.findAll('table', class_='article-table')

for table in tables:
	eggs = table.findAll('tr')
	eggs.pop(0)
	
	eggnumber = 0
	for egg in eggs:
		print(eggnumber)
		if eggnumber == 162:
			break
		if eggnumber not in FORBIDDEN:
			elements = egg.findAll('td')
			
			print(elements[2].text)
			eggBreed = elements[2].text

			if eggBreed not in dic:
				print(elements[1].text)
				eggDescription  = elements[1].text

				eggBiomes = []
				for biome in elements[3].findAll('a'):
					eggBiomes.append(biome.text)
				print(eggBiomes)
				dic[json_categories[index]][eggBreed] = {'description': eggDescription, 'biomes': eggBiomes}

		eggnumber += 1
	break
	index += 1


print(dic)
with open('eggpedia.json', 'w') as file:
	json.dump(dic, file)