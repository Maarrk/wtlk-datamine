#!/usr/bin/env python3

import re
import json
# import wikipedia
import urllib.request
from colorama import init as colorinit, Fore
from pprint import pprint

colorinit()

petfile = open('petscan.json', 'r')
# planefile = open('planes.json', 'w')

petdata = json.load(petfile)
titles = [page['title'] for page in petdata['*'][0]['a']['*']]
# titles = [p['title'].replace('_', ' ') for p in jdata['*'][0]['a']['*']]

planedata = {'planes':[]}

for i in range(100):
    # print('Getting page: ' + titles[i])
    # html = wikipedia.page(titles[i]).html()
    try:
        with urllib.request.urlopen('https://en.wikipedia.org/wiki/' + titles[i]) as response:
            html = response.read().decode('utf-8')
            # pprint(html)
            # print('Got: ' + titles[i])
            # result = re.search(r'First flight\n</th>\n<td>(.*?)\n', html)  # wikipedia
            result = re.search(r'First flight</th>\n<td>(.*?)<', html)  # urllib
            if result:
                if len(result.group(1)) == 4:
                    print(Fore.GREEN + titles[i] + ' ' + result.group(1) + Fore.RESET)
                else:
                    print(Fore.YELLOW + titles[i] + ' ' + result.group(1) + Fore.RESET)

                plane = {'name': titles[i].replace('_', ' '), 'firstflight': result.group(1)}
                planedata['planes'].append(plane)
                planefile = open('planes.json', 'w')
                json.dump(planedata, planefile)
                planefile.close()
            else:
                print(Fore.RED + titles[i] + ' has no First flight data' + Fore.RESET)
    except UnicodeEncodeError:
            print(Fore.RED + titles[i] + ' has bad encoding' + Fore.RESET)
            continue

