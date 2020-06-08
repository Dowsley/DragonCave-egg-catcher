from json import load
from random import randrange
from time import sleep
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser

HABITAT = {
    'coast': 1,
    'desert': 2,
    'forest': 3,
    'jungle': 4,
    'alpine': 5,
    'volcano': 6
}

# --- Retrieve credentials --- #
try:
    f = open('secrets.json', 'r')
    data = load(f)
    f.close()
    username = data['username']
    password = data['password']
except Exception as e:
    if type(e) == FileNotFoundError:
        print('ERROR: Secrets.json file not found.')
    else:
        print('ERROR: Failed to retrieve credentials. '
            + 'Check for syntax errors in your secrets.json.')
    exit(0)

# --- Retrieve habitats that are to be searched --- #
habitats = []
try:
    f = open('habitats.txt', 'r')
    lines = f.read().splitlines()
    f.close()

    # File must not be empty
    if len(lines) == 0:
        raise Exception('File Empty')
    for i in lines:
        h = i.lower().strip()
        # Case 1: All habitats
        if h == '*':
            habitats = list(HABITAT.keys())
            break
        # Case 2: Unknown habitat
        elif not (h in HABITAT.keys()):
            print('ERROR: Habitat "{}" not recognized.'.format(h))
            exit(0)
        # Case 3: Normal habitat
        habitats.append(h)
except Exception as e:
    if type(e) == FileNotFoundError:
        print('ERROR: habitats.txt file not found.')
    else:
        print('ERROR: Failed to retrieve the habitats. '
            + 'Check for errors in your habitats.txt.')
    exit(0)

# --- Retrieve egg descriptions --- #
eggs = {}
try:
    f = open('eggs.txt', 'r', encoding='utf8')
    lines = f.read().splitlines()
    f.close()

    # File must not be empty
    if len(lines) == 0:
        raise Exception('File Empty')
    for i in lines:
        d = i.lower().replace('.', '').strip().split('=')
        # Append to dictionary with the description as entry
        eggs[d[0]] = int(d[1])
except Exception as e:
    if type(e) == FileNotFoundError:
        print('ERROR: eggs.txt file not found.')
    else:
        print('ERROR: Failed to retrieve the egg descriptions. '
            + 'Check for errors in your descriptions.txt.')
    exit(0)

# --- Authentication --- #
try:
    browser = RoboBrowser()
    browser.open('https://dragcave.net/')
    form = browser.get_form()
    form['username'] = username
    form['password'] = password
    browser.submit_form(form)
    print("-- SUCCESSFUL AUTHENTICATION --")
except:
    print('Failed to authenticate. '
        + 'Check your credentials or Dragon Cave status')
    exit(0)

# -- Overview message -- #
print(
    'Starting with following entries:\n'
    + 'Habitats: {}\n'.format(', '.join(habitats))
    + 'Egg Orders:'
    )
for i in eggs.items():
    print('- {} ({})'.format(i[0], i[1]))

# --- Startup --- #
print('-- STARTING CATCHER --')
# Runs while the there are still orders
while eggs:
    for h in habitats:
        # Open and parse habitat
        browser.open(
            'https://dragcave.net/locations/' 
            + str(HABITAT[h])
        )
        soup = BeautifulSoup(str(browser.parsed()), features='html.parser')
        cave = (soup.find('div',class_='eggs')).findAll('div')

        # Search available egg(s) in current habitat.
        for egg in cave:
            eggLink = "https://dragcave.net" + egg.find('a').get('href')
            eggDesc = egg.find('span').text.lower().replace('.','')
            print(eggLink, eggDesc)

            # Catch dragon if it corresponds to a order.
            if eggDesc in eggs:
                browser.open(eggLink)
                print('-- EGG FOUND -- ')
                print('Description: {}'.format(eggDesc))
                eggs[eggDesc] -= 1 # Decrement count
                print('Left to catch: {}\n'.format(eggs[eggDesc]))
                # If no eggs left to catch, remove entry from orders.
                if eggs[eggDesc] == 0:
                    del eggs[eggDesc]
                    
        sleep(randrange(3))
print('-- EXECUTION FINISHED --')