#!/usr/bin/env python3

import re
import json
# import wikipedia
import urllib.request
from colorama import init as colorinit, Fore
from pprint import pprint

colorinit()

petfile = open('petscan.json', 'r')

petdata = json.load(petfile)
titles = [page['title'] for page in petdata['*'][0]['a']['*']]

planedata = {'planes':[]}

# Patterns:
pat_firstflight = re.compile(r'(First flight|Introduction)</th>\n<td>(.*?)<')

for i in range(len(titles)):
    try:
        with urllib.request.urlopen('https://en.wikipedia.org/wiki/' + titles[i]) as response:
            html = response.read().decode('utf-8')
            # pprint(html)
            result = pat_firstflight.search(html)
            if result:
                firstflight = result.group(2)
                decade = re.search(r'\d\d\d\ds', firstflight)
                if decade:
                    print(Fore.YELLOW + titles[i] + ' ' + decade.group()[:-1] + Fore.RESET)
                else:
                    year = re.search(r'\d\d\d\d', firstflight)
                    if year:
                        print(Fore.GREEN + titles[i] + ' ' + year.group() + Fore.RESET)
                    else:
                        print(Fore.RED + titles[i] + ' has no First flight / Introduction year or decade' + Fore.RESET)

                plane = {'name': titles[i].replace('_', ' '), 'firstflight': result.group(2)}
                planedata['planes'].append(plane)
                planefile = open('planes.json', 'w')
                # json.dump(planedata, planefile)
                planefile.write(json.dumps(planedata, indent=4))
                planefile.close()
            else:
                print(Fore.RED + titles[i] + ' has no First flight / Introduction data' + Fore.RESET)
    except UnicodeEncodeError:
            print(Fore.RED + titles[i] + ' has bad encoding' + Fore.RESET)
            continue

