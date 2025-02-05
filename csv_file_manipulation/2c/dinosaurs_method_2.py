"""
 Write a program to read in the data files from disk, then print the names of only the bipedal dinosaurs from fastest to slowest.

speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)
Where g = 9.8 m/s^2 (gravitational constant)
"""

# read file individually -> save info to dict -> if sufficient info -> calcualate

import csv
from collections import defaultdict

dino_info = defaultdict(list)

with open('./dinosaurs.csv', 'r') as r1, open('./dinosaurs_strides.csv', 'r') as r2:

    reader1 = csv.DictReader(r1)
    reader2 = csv.DictReader(r2)

    for line in reader1:

        dino = line['NAME']
        leg_len = line['LEG_LENGTH']

        dino_info[dino].append(leg_len)

    for line in reader2:

        dino = line['NAME']
        stride_len = line['STRIDE_LENGTH']

        dino_info[dino].append(stride_len)

g = 9.8

dino_speeds = defaultdict(int)

for k, v in dino_info.items():

    if len(v) != 2:
        continue

    leg_len, stride_len = float(v[0]), float(v[1])

    speed = ((stride_len / leg_len) - 1) * (leg_len ** g)
    
    dino_speeds[k] = round(speed, 2)

dino_speeds = sorted(dino_speeds.items(), reverse=True, key= lambda x: x[1])

for k, v in dino_speeds:
    print(k, v)

"""
Tyrannosaurus 61347.77
Allosaurus 19517.22
Velociraptor 8609.75
Stegosaurus 952.78
Struthiomimus 616.27
Triceratops 222.86
Euoplocephalus 31.99
"""