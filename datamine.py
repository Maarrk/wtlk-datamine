#!/usr/bin/env python3

# pylint: disable=C0103

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
pat_capacity = re.compile(r'<li><b>Capacity:</b>(.*?)</li>')
pat_length = re.compile(r'<li><b>Length:</b>(.*?)\D([0-9|\.]*?)&#160;m')
pat_wingspan = re.compile(r'<li><b>Wingspan:</b>(.*?)\D([0-9|\.]*?)&#160;m')
pat_emptyweight = re.compile(r'<li><b>Empty weight:</b>(.*?)\D([0-9|\.]*?)&#160;kg')
pat_grossweight = re.compile(r'<li><b>Gross weight:</b>(.*?)\D([0-9|\.]*?)&#160;kg')

try:
    for i in range(len(titles)):
        plane = {'name': titles[i].replace('_', ' ')}
        try:
            with urllib.request.urlopen('https://en.wikipedia.org/wiki/' + titles[i]) as response:
                html = response.read().decode('utf-8')
                plane['htmllength'] = len(html)
                # pprint(html)

                # First flight:
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

                # Capacity:
                result = pat_capacity.search(html)
                if result:
                    plane['capacity'] = result.group(1)

                # Length:
                result = pat_length.search(html)
                if result:
                    try:
                        plane['length'] = float(result.group(2))
                    except:
                        pass

                # Wingspan:
                result = pat_wingspan.search(html)
                if result:
                    try:
                        plane['wingspan'] = float(result.group(2))
                    except:
                        pass

                # Empty weight:
                result = pat_emptyweight.search(html)
                if result:
                    try:
                        plane['emptyweight'] = float(result.group(2))
                    except:
                        pass

                # Gross weight:
                result = pat_grossweight.search(html)
                if result:
                    try:
                        plane['grossweight'] = float(result.group(2))
                    except:
                        pass

        except UnicodeEncodeError:
            print(Fore.RED + titles[i] + ' has bad encoding' + Fore.RESET)
            plane['error'] = 'UnicodeEncodeError'

        planedata['planes'].append(plane)

except KeyboardInterrupt:
    print('Saving to JSON file...')
    planefile = open('planes.json', 'w')
    planedata['meta'] = {'planecount': len(planedata['planes'])}
    planefile.write(json.dumps(planedata, indent=4, sort_keys=True))
    planefile.close()
    print(Fore.GREEN + 'JSON file saved' + Fore.RESET)
