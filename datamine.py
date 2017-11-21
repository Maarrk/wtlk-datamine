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
    plane = {'name': titles[i].replace('_', ' ')}
    try:
        with urllib.request.urlopen('https://en.wikipedia.org/wiki/' + titles[i]) as response:
            html = response.read().decode('utf-8')
            # pprint(html)
            result = pat_firstflight.search(html)
            if result:
                firstflight = result.group(2)
                decade = re.search(r'\d\d\d\ds', firstflight)
                if decade:
                    dec_num = int(decade.group()[:-1])
                    print(Fore.YELLOW + titles[i] + ' ' + str(dec_num) + Fore.RESET)
                    plane['decade'] = dec_num
                else:
                    year = re.search(r'\d\d\d\d', firstflight)
                    if year:
                        y_num = int(year.group())
                        print(Fore.GREEN + titles[i] + ' ' + str(y_num) + Fore.RESET)
                        plane['year'] = y_num
                        plane['decade'] = y_num - y_num % 10
                    else:
                        print(Fore.RED + titles[i] + ' has no First flight / Introduction year or decade' + Fore.RESET)
            else:
                print(Fore.RED + titles[i] + ' has no First flight / Introduction data' + Fore.RESET)
    except UnicodeEncodeError:
        print(Fore.RED + titles[i] + ' has bad encoding' + Fore.RESET)
        plane['error'] = 'UnicodeEncodeError'

    planedata['planes'].append(plane)
    planefile = open('planes.json', 'w')
    planefile.write(json.dumps(planedata, indent=4))
    planefile.close()

