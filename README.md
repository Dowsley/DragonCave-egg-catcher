# Dragon Cave - Egg Catcher
## DISCLAIMER: This script isn't meant to endorse cheating. It was made just for fun, and because it's possible.
According to Dragon Cave's [terms and conditions](https://dragcave.net/terms), *the use of scripts that modify pages on the site in order to give users of said addons an advantage over other users* is objectively against the site's policies. Before you use this script, remember what is the game purpose, and how it is really intended to be played.

## Dependency Installation
With Python3 Installed, run:
```
pip3 install -r requirements.txt
```
Warning: Werkzeug must be of version 0.16.1, due to RoboBrowser's current broken state with version 1.0.0.

## Usage
### Credentials
Put your Dragon Cave credentials within secrets.json. Be careful not to break the JSON syntax.

Usage Example:
```
{
    "username": "NebulaLover",
    "password": "royalblue"
}
```

If you're wondering if it's safe, there's no better way to know than reading through the code yourself.

### Biomes
Put the habitats you want to search in habitats.txt, one habitat each line. Don't bother with lower or upper cases.

For example:
```
volcano
alpine
coast
```

If you want all biomes, you can just put a '*' within the file (with no quotes).

_NOTE: Holiday biomes aren't implemented yet._

### Egg-catching orders
In each line of eggs.txt, put a egg description followed by the number of times you want to catch that egg, both separated by a =.  Don't bother with lower or upper cases.

Watch the following format, in the example:
```
It’s bright. And pink.=1
This egg smells rather rancid.=1
```

MOTE: It's *recommended* to include the correct characters of the original description, including punctuation.

### Execution
Just execute the script, and the command line output will tell you when eggs are catched.