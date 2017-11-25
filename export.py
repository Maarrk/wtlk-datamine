#!/usr/bin/env python3

# pylint: disable=C0103

import json
from copy import copy

planefile = open('planes_all.json', 'r')
planedata = json.load(planefile)
planefile.close()

columns = ['name', 'year', 'decade', 'crew', 'capacity',
           'length', 'wingspan', 'wingarea',
           'emptyweight', 'grossweight',
           'maxspeed', 'cruisespeed', 'stallspeed',
           'range', 'fuelcapacity', 'power']
row = []

with open('planes_export.txt', 'w') as txt_file:
    text = '; '.join([str(cell) for cell in columns]) + '\n'
    txt_file.write(text)

    for pln in planedata['planes']:
        row.clear()
        for col in columns:
            if col in pln:
                row.append(pln[col])
            else:
                row.append('UNKNOWN')

        text = '; '.join([str(cell) for cell in row]) + '\n'
        txt_file.write(text)
